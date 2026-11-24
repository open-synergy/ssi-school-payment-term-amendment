# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolEnrollment(models.Model):
    """Adds the Amendments smart button to School Enrollment.

    Pure navigation: ``amendment_ids`` lists the payment term
    amendment documents that target this enrollment, and
    ``amendment_count`` backs the smart button opening them. No new
    action is added on the enrollment itself.
    """

    _name = "school_enrollment"
    _inherit = [
        "school_enrollment",
    ]

    amendment_ids = fields.One2many(
        string="Payment Term Amendments",
        comodel_name="school_payment_term_amendment",
        inverse_name="enrollment_id",
        help="Payment term amendment documents that target this enrollment.",
    )
    amendment_count = fields.Integer(
        string="Payment Term Amendment Count",
        compute="_compute_amendment_count",
        help="Number of payment term amendment documents targeting this "
        "enrollment, backing the Amendments smart button.",
    )

    @api.depends("amendment_ids")
    def _compute_amendment_count(self):
        """Count the payment term amendment documents of this enrollment.

        :return: None
        """
        for record in self:
            record.amendment_count = len(record.amendment_ids)
