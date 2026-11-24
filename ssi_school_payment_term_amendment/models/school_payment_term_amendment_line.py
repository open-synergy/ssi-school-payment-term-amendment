# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolPaymentTermAmendmentLine(models.Model):
    """Represents one change applied by a payment term amendment.

    ``type`` selects the operation:

    * ``void`` -- ``detail_id`` stops being billed (``voided``), its
      ``price_unit`` stays untouched.
    * ``change_price`` -- ``detail_id`` gets ``price_unit`` as its new
      unit price (it may go up or down).
    * ``add_detail`` -- a new detail is created on ``term_id`` (a term
      of the enrollment) or on the term created by the ``add_term``
      line ``new_term_line_id`` of the same document.
    * ``add_term`` -- a new payment term is created; its details come
      from the ``add_detail`` lines pointing at this line.

    The product/account/UoM/tax fields come from
    ``mixin.product_line_account`` so an added detail behaves like any
    other payment term detail. They are only meaningful for
    ``add_detail``, hence ``name`` and ``account_id`` are not required
    on the field itself -- ``_check_type_requirements`` enforces them
    per ``type``.
    """

    _name = "school_payment_term_amendment_line"
    _description = "School Payment Term Amendment Line"
    _order = "sequence, id"
    _inherit = [
        "mixin.product_line_account",
        "mixin.many2one_configurator",
    ]

    amendment_id = fields.Many2one(
        string="Amendment",
        comodel_name="school_payment_term_amendment",
        required=True,
        ondelete="cascade",
        help="The payment term amendment document that owns this line.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="amendment_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, taken from the amendment document.",
    )
    name = fields.Char(required=False)
    account_id = fields.Many2one(required=False)
    type = fields.Selection(
        string="Operation",
        selection=[
            ("void", "Void Detail"),
            ("change_price", "Change Price"),
            ("add_detail", "Add Detail"),
            ("add_term", "Add Term"),
        ],
        required=True,
        default="void",
        help=(
            "What this line does on Done: void a detail, change the "
            "unit price of a detail, add a detail to a term, or add a "
            "new payment term."
        ),
    )
    allowed_term_ids = fields.Many2many(
        string="Allowed Payment Terms",
        comodel_name="school_enrollment_payment_term",
        compute="_compute_allowed_term_ids",
        store=False,
        compute_sudo=True,
        help=(
            "Payment terms of the enrollment that have no customer "
            "invoice yet, eligible as the target of this line."
        ),
    )
    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_enrollment_payment_term",
        help=(
            "The not-yet-invoiced payment term this line targets. "
            "Required for Void Detail and Change Price; for Add "
            "Detail either this or New Term must be set."
        ),
    )
    allowed_detail_ids = fields.Many2many(
        string="Allowed Details",
        comodel_name="school_enrollment_payment_term_detail",
        compute="_compute_allowed_detail_ids",
        store=False,
        compute_sudo=True,
        help=(
            "Detail lines of the selected term that are not invoiced "
            "and not voided, eligible for Void Detail/Change Price."
        ),
    )
    detail_id = fields.Many2one(
        string="Detail",
        comodel_name="school_enrollment_payment_term_detail",
        help=(
            "The payment term detail this line voids or reprices. "
            "Required for Void Detail and Change Price."
        ),
    )
    detail_product_id = fields.Many2one(
        string="Detail Product",
        comodel_name="product.product",
        related="detail_id.product_id",
        readonly=True,
        help="The product of the targeted detail, shown for reference.",
    )
    price_unit_before = fields.Monetary(
        string="Price Before",
        currency_field="currency_id",
        readonly=True,
        copy=False,
        help=(
            "Snapshot of the targeted detail's unit price at the "
            "moment it was selected, filled automatically by onchange, "
            "so the amendment keeps a trace of the previous price."
        ),
    )
    new_term_line_id = fields.Many2one(
        string="New Term",
        comodel_name="school_payment_term_amendment_line",
        ondelete="set null",
        help=(
            "The Add Term line of this same document whose new term "
            "receives this detail. The Add Term line has to be saved "
            "first."
        ),
    )
    term_name = fields.Char(
        string="New Term Name",
        help="Name of the payment term created by an Add Term line.",
    )
    term_sequence = fields.Integer(
        string="New Term Sequence",
        default=5,
        help="Order of the payment term created by an Add Term line.",
    )
    date_invoice = fields.Date(
        string="Estimated Invoice Date",
        help="Estimated invoice date of the term created by Add Term.",
    )
    date_due = fields.Date(
        string="Estimated Due Date",
        help="Estimated due date of the term created by Add Term.",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
        help="Products allowed on an added detail, per the payment template.",
    )
    created_term_id = fields.Many2one(
        string="Created Term",
        comodel_name="school_enrollment_payment_term",
        readonly=True,
        copy=False,
        help="The payment term created on Done by an Add Term line.",
    )
    created_detail_id = fields.Many2one(
        string="Created Detail",
        comodel_name="school_enrollment_payment_term_detail",
        readonly=True,
        copy=False,
        help="The detail created on Done by an Add Detail line.",
    )

    @api.depends("amendment_id.enrollment_id")
    def _compute_allowed_term_ids(self):
        """Compute the payment terms selectable as this line's target.

        Nothing is proposed until the owning document has an
        enrollment; otherwise the not-yet-invoiced payment terms of
        that enrollment are collected.

        :return: None
        """
        for record in self:
            result = False
            enrollment = record.amendment_id.enrollment_id
            if enrollment:
                result = (
                    self.env["school_enrollment_payment_term"]
                    .search(
                        [
                            ("enrollment_id", "=", enrollment.id),
                            ("customer_invoice_id", "=", False),
                        ]
                    )
                    .ids
                )
            record.allowed_term_ids = result

    @api.depends("term_id")
    def _compute_allowed_detail_ids(self):
        """Compute the details selectable on this line.

        Nothing is proposed until ``term_id`` is set; otherwise the
        details of that term with no customer invoice line that are
        not voided are collected.

        :return: None
        """
        for record in self:
            result = False
            if record.term_id:
                result = (
                    self.env["school_enrollment_payment_term_detail"]
                    .search(
                        [
                            ("term_id", "=", record.term_id.id),
                            ("customer_invoice_line_id", "=", False),
                            ("voided", "=", False),
                        ]
                    )
                    .ids
                )
            record.allowed_detail_ids = result

    @api.depends("amendment_id.enrollment_id.payment_template_id")
    def _compute_allowed_product_ids(self):
        """Compute the products selectable on an added detail.

        Resolves the Product Configuration of the payment template of
        the enrollment through ``_m2o_configurator_get_filter``,
        exactly like the payment term detail does. When the
        enrollment has no payment template the field is left empty.

        :return: None
        """
        for record in self:
            result = False
            template = record.amendment_id.enrollment_id.payment_template_id
            if template:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=template.product_selection_method,
                    manual_recordset=template.product_ids,
                    domain=template.product_domain,
                    python_code=template.product_python_code,
                )
            record.allowed_product_ids = result

    @api.onchange("type")
    def onchange_term_id(self):
        """Clear the target term when the line creates a new term."""
        if self.type == "add_term":
            self.term_id = False

    @api.onchange("type", "term_id")
    def onchange_detail_id(self):
        """Clear the target detail when it no longer fits the line.

        The detail is only used by Void Detail and Change Price and it
        has to belong to the selected term.
        """
        if self.type not in ("void", "change_price") or (
            self.detail_id and self.detail_id.term_id != self.term_id
        ):
            self.detail_id = False

    @api.onchange("type")
    def onchange_new_term_line_id(self):
        """Clear the New Term link unless the line adds a detail."""
        if self.type != "add_detail":
            self.new_term_line_id = False

    @api.onchange("detail_id")
    def onchange_price_unit_before(self):
        """Snapshot the targeted detail's unit price.

        Fills ``price_unit_before`` with the selected detail's
        ``price_unit``; zero when the detail is unset.
        """
        self.price_unit_before = self.detail_id.price_unit if self.detail_id else 0.0

    @api.onchange("detail_id")
    def onchange_price_unit_from_detail(self):
        """Propose the current unit price for a Change Price line.

        The user then edits ``price_unit`` into the new price.
        """
        if self.type == "change_price" and self.detail_id:
            self.price_unit = self.detail_id.price_unit

    @api.constrains(
        "type",
        "term_id",
        "detail_id",
        "new_term_line_id",
        "term_name",
        "product_id",
        "account_id",
        "uom_id",
    )
    def _check_type_requirements(self):
        """Require the fields each operation needs.

        * Void Detail / Change Price: ``term_id`` and ``detail_id``.
        * Add Detail: product, account and UoM, and exactly one of
          ``term_id`` / ``new_term_line_id``.
        * Add Term: ``term_name``.

        :raises ValidationError: a required field is empty or both
            targets of an Add Detail line are set.
        """
        for record in self.sudo():
            problem = False
            if record.type in ("void", "change_price"):
                if not record.term_id or not record.detail_id:
                    problem = _("Payment Term and Detail are required")
            elif record.type == "add_detail":
                if not (record.product_id and record.account_id and record.uom_id):
                    problem = _("Product, Account and UoM are required")
                elif bool(record.term_id) == bool(record.new_term_line_id):
                    problem = _("Set exactly one of Payment Term and New Term")
            elif record.type == "add_term" and not record.term_name:
                problem = _("New Term Name is required")
            if problem:
                error_message = (
                    _(
                        """
Context: Set payment term amendment line
Database ID: %s
Problem: %s
Solution: Fill the fields required by the selected operation
"""
                    )
                    % (record.id, problem)
                )
                raise ValidationError(error_message)

    @api.constrains("price_unit", "type")
    def _check_price_unit_not_negative(self):
        """Forbid a negative unit price on Change Price and Add Detail.

        :raises ValidationError: ``price_unit`` is negative.
        """
        for record in self.sudo():
            if record.type in ("change_price", "add_detail") and record.price_unit < 0:
                error_message = (
                    _(
                        """
Context: Set payment term amendment line price
Database ID: %s
Problem: Price Unit %s is negative
Solution: Enter a price greater than or equal to zero
"""
                    )
                    % (record.id, record.price_unit)
                )
                raise ValidationError(error_message)

    def _prepare_term_vals(self):
        """Build the payment term create values of an Add Term line.

        The new term is created locked: it is born on an enrollment
        that is already open/done.

        :return: dict of ``school_enrollment_payment_term`` values.
        """
        self.ensure_one()
        return {
            "enrollment_id": self.amendment_id.enrollment_id.id,
            "name": self.term_name,
            "sequence": self.term_sequence,
            "date_invoice": self.date_invoice,
            "date_due": self.date_due,
            "locked": True,
        }

    def _prepare_detail_vals(self):
        """Build the detail create values of an Add Detail line.

        The target term is ``term_id`` or, for a line pointing at an
        Add Term line, the term that line created earlier in the same
        Done run. The new detail is created locked.

        :return: dict of ``school_enrollment_payment_term_detail``
            values.
        """
        self.ensure_one()
        term = self.term_id or self.new_term_line_id.created_term_id
        return {
            "term_id": term.id,
            "product_id": self.product_id.id,
            "name": self.name or self.product_id.display_name,
            "account_id": self.account_id.id,
            "usage_id": self.usage_id.id,
            "analytic_account_id": self.analytic_account_id.id,
            "uom_id": self.uom_id.id,
            "uom_quantity": self.uom_quantity,
            "price_unit": self.price_unit,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "locked": True,
        }
