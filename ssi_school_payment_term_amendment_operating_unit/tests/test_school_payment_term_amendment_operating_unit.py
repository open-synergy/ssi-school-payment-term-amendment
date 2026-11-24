# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolPaymentTermAmendmentOperatingUnit(YamlTransactionCase):
    """Cover Operating Unit handling on ``school_payment_term_amendment``.

    Includes the derivation of ``operating_unit_id`` from
    ``enrollment_id`` on create/write, an explicit value winning over
    that derivation, the onchange mirroring it, the record rule
    restricting visibility to a user's own Operating Units --
    exercised across two different Operating Units so the restriction
    is actually tested rather than passing by coincidence -- and an
    enrollment without an Operating Unit leaving the document without
    one.
    """

    def test_school_payment_term_amendment_operating_unit(self):
        """Run every Operating Unit scenario for the amendment document."""
        self.run_yaml_scenario(
            "test_data_school_payment_term_amendment_operating_unit.yaml"
        )
