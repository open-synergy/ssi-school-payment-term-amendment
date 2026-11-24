# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- BUKAN HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolPaymentTermAmendment(HttpSavepointCase):
    """Tour tests for ``school_payment_term_amendment`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the enrollment, terms, and fixture documents for the tours.

        The academic term's enrollment window is opened first through
        its public ``action_open_enrollment()`` (see
        ``ssi_school/tests/test_ui_school_academic_term.py``) --
        ``school_enrollment._check_enrollment_window`` rejects an
        enrollment reaching ``open`` while
        ``academic_term_id.enrollment_state`` is still the model's
        default ``close``.

        The enrollment itself is then given a literal ``name`` *before*
        being opened, and is opened through its own
        ``action_open()`` (``mixin.transaction_open``,
        ``_after_approved_method = "action_open"`` on
        ``school_enrollment``) with ``bypass_policy_check`` in the
        context -- exercising its own approval workflow is out of
        scope for this module's tours. ``write({"state": "open"})``
        is deliberately NOT used: it skips ``sudo()``, the
        ``_run_pre_open_check``/``_run_post_open_action`` decorator
        hooks, and -- the part that matters for the create tour's
        many2one dropdown below -- ``_prepare_open_data()``'s call to
        ``_create_sequence()`` (see ``odoo-development-ui-test`` skill,
        ``structure-and-runner.md`` §"Prasyarat state fixture", which
        documents this exact PR). Skipping ``_create_sequence()``
        leaves ``name`` at its default ``"/"``, and ``name_get()``
        (``ssi_transaction_mixin/models/mixin_transaction.py:194-202``)
        then reports every such record as ``"*" + id`` -- indistinguishable
        from the m2o widget's own "Create '...'" entry. Pre-setting
        ``name`` to a literal string (checked by
        ``_create_sequence()`` against the sentinel ``"/"``) also
        skips consuming an ``ir.sequence`` number, avoiding a
        year-dependent ``display_name`` that a tour could not match
        with a literal selector. The edit/delete fixture documents get
        ``user_id`` set explicitly to ``base.user_admin``: ``cls.env``
        runs as superuser, and
        ``school_payment_term_amendment_internal_user_rule`` would
        otherwise hide them from the ``admin`` session the tours log
        in as.
        """
        super().setUpClass()
        admin = cls.env.ref("base.user_admin")
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR PTA Grade Type", "code": "TPTAGT"}
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR PTA School",
                "code": "TPTASC",
                "grade_type_id": grade_type.id,
            }
        )
        academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR PTA Academic Year",
                "code": "TPTAAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR PTA Term",
                "code": "TPTATM",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR PTA Grade",
                "code": "TPTAGR",
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR PTA Class",
                "code": "TPTACL",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR PTA Contact"})
        student = cls.env["school_student"].create(
            {
                "name": "TOUR PTA Student",
                "code": "TPTAST",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        cls.tour_enrollment = cls.env["school_enrollment"].create(
            {
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
            }
        )
        academic_term.action_open_enrollment()
        cls.tour_enrollment.write({"name": "TOUR PTA Enrollment"})
        cls.tour_enrollment.with_context(bypass_policy_check=True).action_open()
        account_type_income = cls.env.ref("account.data_account_type_revenue")
        income_account = cls.env["account.account"].create(
            {
                "name": "TOUR PTA Income Account",
                "code": "TPTAIA",
                "user_type_id": account_type_income.id,
                "reconcile": False,
            }
        )
        product = cls.env["product.product"].create(
            {"name": "TOUR PTA Product", "type": "service"}
        )
        cls.tour_term = cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": cls.tour_enrollment.id,
                "name": "TOUR PTA Term",
            }
        )
        uom_unit = cls.env.ref("uom.product_uom_unit")

        def _create_detail(detail_name):
            """Create one detail line on the fixture payment term.

            :param detail_name: value of the detail's ``name``.
            :return: the created
                ``school_enrollment_payment_term_detail`` record.
            """
            return cls.env["school_enrollment_payment_term_detail"].create(
                {
                    "term_id": cls.tour_term.id,
                    "product_id": product.id,
                    "name": detail_name,
                    "account_id": income_account.id,
                    "uom_id": uom_unit.id,
                    "uom_quantity": 1.0,
                    "price_unit": 100000.0,
                }
            )

        cls.tour_detail_create = _create_detail("TOUR PTA Detail Create")
        cls.tour_reason_create = cls.env["school_payment_term_amendment_reason"].create(
            {"name": "TOUR PTA Reason Create", "code": "/"}
        )
        # ``global_use=True`` is required: the cancel wizard's radio field
        # is domained to ``model_id.all_cancel_reason_ids``, which only
        # merges reasons with ``global_use=True`` (see
        # ``ssi_transaction_cancel_mixin``'s ``ir_model.py``).
        cls.tour_cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR PTA Cancel Reason",
                "code": "/",
                "global_use": True,
            }
        )

        def _create_amendment_doc(reason_name, detail_name):
            """Create one draft amendment document for a tour.

            The document carries one Void Detail line on its own detail
            line, so no two fixtures share a detail. ``user_id`` is set
            to ``base.user_admin`` so the internal-user record rule does
            not hide it from the ``admin`` session of the tour.

            :param reason_name: value of the fixture Reason's ``name``.
            :param detail_name: value of the fixture detail's ``name``.
            :return: the created ``school_payment_term_amendment``
                record.
            """
            reason = cls.env["school_payment_term_amendment_reason"].create(
                {"name": reason_name, "code": "/"}
            )
            detail = _create_detail(detail_name)
            return cls.env["school_payment_term_amendment"].create(
                {
                    "user_id": admin.id,
                    "enrollment_id": cls.tour_enrollment.id,
                    "reason_id": reason.id,
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "type": "void",
                                "term_id": cls.tour_term.id,
                                "detail_id": detail.id,
                            },
                        )
                    ],
                }
            )

        cls.tour_edit_doc = _create_amendment_doc(
            "TOUR PTA Reason Edit", "TOUR PTA Detail Edit"
        )
        cls.tour_delete_doc = _create_amendment_doc(
            "TOUR PTA Reason Delete", "TOUR PTA Detail Delete"
        )
        cls.tour_confirm_doc = _create_amendment_doc(
            "TOUR PTA Reason Confirm", "TOUR PTA Detail Confirm"
        )

        # ``base.user_admin`` is listed in the validator group's ``users``
        # (see security/res_groups), which implies the user group -- so
        # ``admin`` can Confirm, Approve, Reject, Cancel, and Restart every
        # fixture below, and is the approval template's approver.
        cls.tour_approve_doc = _create_amendment_doc(
            "TOUR PTA Reason Approve", "TOUR PTA Detail Approve"
        )
        cls.tour_approve_doc.with_context(bypass_policy_check=True).action_confirm()

        cls.tour_reject_doc = _create_amendment_doc(
            "TOUR PTA Reason Reject", "TOUR PTA Detail Reject"
        )
        cls.tour_reject_doc.with_context(bypass_policy_check=True).action_confirm()

        cls.tour_cancel_doc = _create_amendment_doc(
            "TOUR PTA Reason Cancel", "TOUR PTA Detail Cancel"
        )

        cls.tour_restart_doc = _create_amendment_doc(
            "TOUR PTA Reason Restart", "TOUR PTA Detail Restart"
        )
        cls.tour_restart_doc.with_context(bypass_policy_check=True).action_cancel(
            cancel_reason=cls.tour_cancel_reason
        )

        cls.tour_restart_approval_doc = _create_amendment_doc(
            "TOUR PTA Reason Restart Approval", "TOUR PTA Detail Restart Approval"
        )
        cls.tour_restart_approval_doc.with_context(
            bypass_policy_check=True
        ).action_confirm()
        # Simulate a stalled approval process: no approval template
        # assigned. This is not a state transition (``state`` stays
        # ``confirm``), it is exactly the precondition documented in
        # ``14-restart-approval.md``.
        cls.tour_restart_approval_doc.write({"approval_template_id": False})

        cls.tour_reload_template_doc = _create_amendment_doc(
            "TOUR PTA Reason Reload Template", "TOUR PTA Detail Reload Template"
        )

    def test_create(self):
        """Run the create tour for ``school_payment_term_amendment``.

        IK: docs/school_payment_term_amendment/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_payment_term_amendment``.

        IK: docs/school_payment_term_amendment/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_payment_term_amendment``.

        IK: docs/school_payment_term_amendment/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_payment_term_amendment``.

        IK: docs/school_payment_term_amendment/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_payment_term_amendment``.

        IK: docs/school_payment_term_amendment/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_payment_term_amendment``.

        IK: docs/school_payment_term_amendment/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_payment_term_amendment``.

        IK: docs/school_payment_term_amendment/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_payment_term_amendment``.

        IK: docs/school_payment_term_amendment/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_restart",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval tour for ``school_payment_term_amendment``.

        IK: docs/school_payment_term_amendment/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_restart_approval",
            login="admin",
        )

    def test_reload_template_policy(self):
        """Run the reload template policy tour.

        IK: docs/school_payment_term_amendment/15-reload-template-policy.md
        """
        self.start_tour(
            "/web",
            "ssi_school_payment_term_amendment_reload_template_policy",
            login="admin",
        )
