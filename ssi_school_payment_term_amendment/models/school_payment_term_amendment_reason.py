# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolPaymentTermAmendmentReason(
    models.Model
):  # pylint: disable=too-few-public-methods
    """Represents the reason behind a payment term amendment.

    A payment term amendment voids, reprices or adds not-yet-invoiced
    payment term lines of an enrollment. This model only carries the
    reason (e.g. activity cancelled, pricing correction) that a
    payment term amendment document records.

    All fields (``name``, ``code``, ``active``, ``note``) are provided by
    ``mixin.master_data``; this model does not redeclare any of them.
    """

    _name = "school_payment_term_amendment_reason"
    _inherit = ["mixin.master_data"]
    _description = "School Payment Term Amendment Reason"
    _order = "name, id"
