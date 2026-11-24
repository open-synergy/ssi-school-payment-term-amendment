# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolPaymentTermAmendment(models.Model):
    """Represents a payment term amendment document of one enrollment.

    A payment term amendment voids, reprices or adds payment term
    lines and payment terms of one enrollment (``open`` or ``done``),
    as long as the targeted term or line has not been invoiced yet.
    It is not a billing reduction: a voided line keeps its original
    ``price_unit`` and merely stops being billed. The change only
    takes effect once the document is approved.

    Confirm/Approve/Reject/Restart Approval/Cancel/Restart are gated
    by a ``policy.template`` (``policy_template/
    school_payment_term_amendment.xml``); there is no manual Done
    button (``_automatically_insert_done_button = False``) because
    ``_after_approved_method = "action_done"`` reaches ``done``
    automatically once approval completes. The prerequisites checked
    before Confirm and again before Done, and the amendment applied
    on Done, live in ``_check_amendment_prerequisites`` and
    ``_10_apply_amendment`` below. There is no reversal after Done.
    """

    _name = "school_payment_term_amendment"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.company_currency",
    ]
    _description = "School Payment Term Amendment"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Date this payment term amendment document was created.",
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        domain=[("state", "in", ["open", "done"])],
        help=(
            "The open or done enrollment whose not-yet-invoiced "
            "payment terms are amended. One document amends exactly "
            "one enrollment."
        ),
    )
    reason_id = fields.Many2one(
        string="Reason",
        comodel_name="school_payment_term_amendment_reason",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Why the payment terms of this enrollment are amended.",
    )
    note = fields.Text(
        string="Note",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Optional free-form explanation for this amendment.",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        related="enrollment_id.student_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The student being billed, taken from the enrollment.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        related="enrollment_id.academic_year_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The academic year of the enrollment.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        related="enrollment_id.academic_term_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The academic term of the enrollment.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="enrollment_id.currency_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="The billing currency, taken from the enrollment.",
    )
    line_ids = fields.One2many(
        string="Line",
        comodel_name="school_payment_term_amendment_line",
        inverse_name="amendment_id",
        copy=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The individual changes this amendment applies on Done.",
    )

    @api.model
    def _get_policy_field(self):
        """Extend the list of policy-controlled boolean fields.

        Adds every ``*_ok`` field contributed by the confirm/done/
        cancel workflow mixins, so ``mixin.policy._compute_policy``
        can assign them from the matching ``policy.template``
        (``policy_template/school_payment_term_amendment.xml``) --
        without this override the fields would never be assigned by
        their own compute method and Odoo would raise a cache error
        the first time a view reads them.

        :return: list of policy field names.
        """
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "done_ok",
            "cancel_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    def _raise_prerequisite_error(self, problem, solution):
        """Raise the structured error of a failed prerequisite.

        :param problem: translated sentence saying what is wrong.
        :param solution: translated sentence saying how to fix it.
        :raises UserError: always.
        """
        self.ensure_one()
        error_message = (
            _(
                """
Context: Confirm/Done payment term amendment
Database ID: %s
Problem: %s
Solution: %s
"""
            )
            % (self.id, problem, solution)
        )
        raise UserError(error_message)

    def _check_line_prerequisites(self, line):
        """Enforce the prerequisites of one amendment line.

        Checks that the targeted payment term belongs to the
        enrollment and has no customer invoice, and that the targeted
        detail belongs to that term, has no customer invoice line and
        is not voided. ``add_detail`` lines pointing at a term of the
        same document must point at an ``add_term`` line of this
        document.

        :param line: ``school_payment_term_amendment_line`` record.
        :raises UserError: a prerequisite is not met.
        :return: None
        """
        self.ensure_one()
        term = line.term_id
        if term:
            if term.enrollment_id != self.enrollment_id:
                self._raise_prerequisite_error(
                    _("Payment Term '%s' does not belong to Enrollment '%s'")
                    % (term.display_name, self.enrollment_id.display_name),
                    _("Select a payment term of the same enrollment"),
                )
            if term.customer_invoice_id:
                self._raise_prerequisite_error(
                    _("Payment Term '%s' already has a Customer Invoice")
                    % (term.display_name,),
                    _(
                        "Cancel this document; a term already invoiced "
                        "can no longer be amended"
                    ),
                )
        if line.type in ("void", "change_price"):
            detail = line.detail_id
            if detail.term_id != term:
                self._raise_prerequisite_error(
                    _("Detail '%s' does not belong to Payment Term '%s'")
                    % (detail.display_name, term.display_name),
                    _("Select a detail that belongs to the selected term"),
                )
            if detail.customer_invoice_line_id:
                self._raise_prerequisite_error(
                    _("Detail '%s' already has a Customer Invoice Line")
                    % (detail.display_name,),
                    _(
                        "Cancel this document; an already-invoiced line "
                        "can no longer be amended"
                    ),
                )
            if detail.voided:
                self._raise_prerequisite_error(
                    _("Detail '%s' is already voided") % (detail.display_name,),
                    _("Select a detail that is not already voided"),
                )
        if line.type == "add_detail" and line.new_term_line_id:
            new_term_line = line.new_term_line_id
            if new_term_line.amendment_id != self or new_term_line.type != "add_term":
                self._raise_prerequisite_error(
                    _("Line '%s' does not point at a New Term line of this document")
                    % (line.display_name,),
                    _("Select an Add Term line of this same document"),
                )

    def _check_amendment_prerequisites(self):
        """Enforce every prerequisite an amendment must meet to proceed.

        Shared by the ``pre_confirm_check`` and ``pre_done_check``
        hooks below -- the exact same checks run again right before
        ``done`` because a customer invoice may have been created on a
        targeted term (e.g. via Create Due Invoice) in the window
        between Confirm and Approve, after Confirm already passed.

        :raises UserError: the enrollment is not ``open``/``done``;
            ``line_ids`` is empty; a line prerequisite fails (see
            ``_check_line_prerequisites``); one detail appears on two
            ``void``/``change_price`` lines; or an ``add_term`` line is
            not referenced by any ``add_detail`` line.
        :return: None
        """
        self.ensure_one()
        if self.enrollment_id.state not in ("open", "done"):
            self._raise_prerequisite_error(
                _("Enrollment '%s' is neither Open nor Done")
                % (self.enrollment_id.display_name,),
                _("Select an enrollment in state Open or Done"),
            )
        if not self.line_ids:
            self._raise_prerequisite_error(
                _("Document has no line"),
                _("Add at least one line before continuing"),
            )
        for line in self.line_ids:
            self._check_line_prerequisites(line)

        touched = self.line_ids.filtered(
            lambda r: r.type in ("void", "change_price")
        ).mapped("detail_id")
        for detail in touched:
            lines = self.line_ids.filtered(
                lambda r, detail=detail: (
                    r.type in ("void", "change_price") and r.detail_id == detail
                )
            )
            if len(lines) > 1:
                self._raise_prerequisite_error(
                    _("Detail '%s' appears on more than one line")
                    % (detail.display_name,),
                    _("Keep only one Void/Change Price line per detail"),
                )

        referenced = self.line_ids.filtered(
            lambda r: r.type == "add_detail" and r.new_term_line_id
        ).mapped("new_term_line_id")
        for line in self.line_ids.filtered(lambda r: r.type == "add_term"):
            if line not in referenced:
                self._raise_prerequisite_error(
                    _("New term '%s' has no Add Detail line") % (line.term_name,),
                    _("Add at least one Add Detail line pointing at the new term"),
                )

    @ssi_decorator.pre_confirm_check()
    def _10_check_amendment_prerequisites_on_confirm(self):
        """Run the amendment prerequisites before Confirm.

        :return: None
        """
        self._check_amendment_prerequisites()

    @ssi_decorator.pre_done_check()
    def _10_check_amendment_prerequisites_on_done(self):
        """Re-run the amendment prerequisites before Done.

        Between Confirm and Approve someone else may run Create Due
        Invoice on a targeted term, so the same checks run again here
        -- see ``_check_amendment_prerequisites``.

        :return: None
        """
        self._check_amendment_prerequisites()

    @ssi_decorator.post_done_action()
    def _10_apply_amendment(self):
        """Apply the amendment once Done is reached.

        Runs in ``sudo()`` with ``bypass_addendum_lock`` in context --
        the only sanctioned way through the addendum lock of payment
        terms and details, and it only opens after approval. In
        order: (1) ``add_term`` lines create their payment term
        (locked); (2) ``add_detail`` lines create their detail
        (locked) on the target term; (3) ``change_price`` lines write
        the new ``price_unit``; (4) ``void`` lines set ``voided``.
        The ids created are kept on the line. Afterwards the product
        summaries of the enrollment are recomputed and a chatter
        message summarising the amendment is posted on it.

        :return: None
        """
        self.ensure_one()
        context_self = self.sudo().with_context(bypass_addendum_lock=True)
        term_model = context_self.env["school_enrollment_payment_term"]
        detail_model = context_self.env["school_enrollment_payment_term_detail"]
        lines = context_self.line_ids
        for line in lines.filtered(lambda r: r.type == "add_term"):
            term = term_model.create(line._prepare_term_vals())
            line.write({"created_term_id": term.id})
        for line in lines.filtered(lambda r: r.type == "add_detail"):
            detail = detail_model.create(line._prepare_detail_vals())
            line.write({"created_detail_id": detail.id})
        for line in lines.filtered(lambda r: r.type == "change_price"):
            line.detail_id.write({"price_unit": line.price_unit})
        for line in lines.filtered(lambda r: r.type == "void"):
            line.detail_id.write({"voided": True})
        # pylint: disable=protected-access
        context_self.enrollment_id._recompute_product_summaries()
        context_self.enrollment_id.message_post(
            body=context_self._prepare_amendment_notification(),
            message_type="notification",
            subtype_xmlid="mail.mt_note",
        )

    def _prepare_amendment_notification(self):
        """Build the chatter message posted on the enrollment on Done.

        Lists, per line, the operation and the term or detail it
        touched, and links back to this amendment document. The link
        is a plain ``/web#model=...`` backend URL rather than a mixin
        helper -- Odoo 14's ``mail.thread`` has no ``_get_html_link``.

        :return: HTML-safe message body.
        :raises ValueError: ``self`` is not a single record.
        """
        self.ensure_one()
        document_url = "/web#model=%s&id=%d&view_type=form" % (
            self._name,
            self.id,
        )
        document_link = '<a href="%s">%s</a>' % (document_url, self.display_name)
        type_labels = dict(self.line_ids._fields["type"].selection)
        lines_html = "".join(
            _("<li>%s: %s</li>")
            % (
                type_labels.get(line.type),
                line.detail_id.display_name
                or line.term_id.display_name
                or line.term_name
                or line.name,
            )
            for line in self.line_ids
        )
        return _("Payment term amendment %s applied the following:<ul>%s</ul>") % (
            document_link,
            lines_html,
        )

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        """Reconfigure the statusbar's visible states on the form view.

        ``insert_on_form_view`` hook fired while the form view is
        being assembled. Delegates to
        ``_reconfigure_statusbar_visible`` (from ``mixin.transaction``)
        so only the states listed in ``_statusbar_visible_label``
        ("draft,confirm,done") show on the status bar, hiding
        ``reject``/``cancel`` there -- the same boilerplate every
        model built on these mixins carries.

        :param view_arch: the form view architecture being assembled.
        :return: the (possibly modified) view architecture.
        """
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
