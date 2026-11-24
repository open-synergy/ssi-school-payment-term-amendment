odoo.define(
    "ssi_school_payment_term_amendment.school_payment_term_amendment_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_payment_term_amendment/01-create.md
        tour.register(
            "ssi_school_payment_term_amendment_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu. "Student Activities" is a
                // level-2 menu (direct child of the app root), so unlike
                // a level-3 grouping header it IS clickable.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Click the New button
                {
                    content: "Click New",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Fill in the required header fields
                {
                    content: "Select the Enrollment",
                    trigger: ".o_field_many2one[name='enrollment_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR PTA Enrollment",
                },
                {
                    content: "Pick the Enrollment from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PTA Enrollment)",
                    in_modal: false,
                },
                {
                    content: "Select the Reason",
                    trigger: ".o_field_many2one[name='reason_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR PTA Reason Create",
                },
                {
                    content: "Pick the Reason from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PTA Reason Create)",
                    in_modal: false,
                },

                // Flow 5 — Open the Amendment Detail tab
                {
                    content: "Open the Amendment Detail tab",
                    trigger: ".o_notebook .nav-link:contains(Amendment Detail)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },

                // Flow 6 — Add a Void Detail line (the default Operation)
                {
                    content: "Click Add a line",
                    trigger: ".o_field_x2many .o_field_x2many_list_row_add a",
                },
                {
                    content: "Select the Payment Term",
                    trigger: ".o_selected_row .o_field_widget[name='term_id'] input",
                    run: "text TOUR PTA Term",
                },
                {
                    content: "Pick the Payment Term from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR PTA Term)",
                    in_modal: false,
                },
                {
                    content: "Select the Detail",
                    trigger: ".o_selected_row .o_field_widget[name='detail_id'] input",
                    run: "text TOUR PTA Detail Create",
                },
                {
                    content: "Pick the Detail from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR PTA Detail Create)",
                    in_modal: false,
                },
                {
                    content: "Commit the line by clicking another cell",
                    // The row is still `.o_selected_row` and `detail_id`
                    // renders as an input while selected, so anchor on the
                    // readonly Price Before cell of the selected row. The
                    // `name` attribute lives on the inner field widget, not
                    // on the `<td>` -- 14.0 `<td>` carries no `name`.
                    trigger:
                        ".o_selected_row .o_field_widget[name='price_unit_before']",
                },

                // Flow 10 — Click Save
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition — document created in Draft
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Confirm button is visible in the header",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_amendment/02-edit.md
        tour.register(
            "ssi_school_payment_term_amendment_edit",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Open the record to edit (found by its Reason,
                // since the document number stays "/" while still Draft)
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTA Reason Edit) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Change the Note field
                {
                    content: "Fill in Note",
                    trigger:
                        ".o_notebook .tab-pane.active textarea.o_field_widget[name='note']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Edited via tour",
                },

                // Flow 4 — Click Save
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition — the change is saved
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Status is Draft with Confirm available",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Confirm button is visible in the header",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_amendment/03-delete.md
        tour.register(
            "ssi_school_payment_term_amendment_delete",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Select the record to delete (found by its
                // Reason, since the document number stays "/" while
                // still Draft)
                {
                    content: "Select the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTA Reason Delete) .o_list_record_selector input",
                    extra_trigger: ".o_list_view",
                },

                // Flow 3 — Click Action > Delete
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Delete",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Delete";
                            }
                        );
                        $delete[0].click();
                    },
                },

                // Flow 4 — Click OK to confirm
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — the record no longer appears in the list
                {
                    content: "Record is removed from the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR PTA Reason Delete)))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_amendment/04-confirm.md
        tour.register(
            "ssi_school_payment_term_amendment_confirm",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Open the record to confirm
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTA Reason Confirm) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Confirm button
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — status changes to Waiting for Approval
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_amendment/05-approve.md
        tour.register(
            "ssi_school_payment_term_amendment_approve",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Open the record to approve
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTA Reason Approve) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Approve button
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — all approval levels fulfilled, status
                // changes automatically to Done
                {
                    content: "Status is Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_amendment/06-reject.md
        tour.register(
            "ssi_school_payment_term_amendment_reject",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Open the record to reject
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTA Reason Reject) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Reject button
                {
                    content: "Click the Reject button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reject_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — status changes to Rejected
                {
                    content: "Status is Rejected",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_amendment/10-cancel.md
        tour.register(
            "ssi_school_payment_term_amendment_cancel",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Open the record to cancel
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTA Reason Cancel) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Cancel button. The header button is
                // `type="action"` naming a numeric action id, never
                // `[name='action_cancel']` -- `:contains(Cancel)` is the
                // only stable selector (odoo-development-ui-test skill,
                // patterns-dialogs-and-wizards.md §H).
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — In the wizard, select the Cancellation Reason.
                // 14.0: no `.modal` prefix -- the trigger is searched
                // INSIDE the already-open modal (§H).
                {
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] .o_radio_item:contains(TOUR PTA Cancel Reason) input",
                },

                // Flow 5 — Click Confirm
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Flow 6 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                },

                // Post-Condition — status changes to Cancelled
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_amendment/12-restart.md
        tour.register(
            "ssi_school_payment_term_amendment_restart",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Open the record to restart
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTA Reason Restart) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Restart button
                {
                    content: "Click the Restart button",
                    trigger: ".o_statusbar_buttons button[name='action_restart']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — status returns to Draft
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_amendment/14-restart-approval.md
        tour.register(
            "ssi_school_payment_term_amendment_restart_approval",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Open the record whose approval process is
                // stalled
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTA Reason Restart Approval) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — Click the Restart Approval Process button
                {
                    content: "Click the Restart Approval Process button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reload_approval_template']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition — status remains Waiting for Approval,
                // and a new approval process is rebuilt from the
                // approval template that now matches (visible on the
                // Approvals tab as `approval_template_id` = "Standard",
                // populated again where it was cleared to False by the
                // fixture)
                {
                    content: "Status is still Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Open the Approvals tab",
                    trigger: ".o_notebook .nav-link:contains(Approvals)",
                },
                {
                    content: "Approval Template is re-assigned",
                    trigger:
                        ".o_field_widget[name='approval_template_id']:contains(Standard)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );

        // IK: docs/school_payment_term_amendment/15-reload-template-policy.md
        tour.register(
            "ssi_school_payment_term_amendment_reload_template_policy",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Student Activities >
                // Payment Term Amendments menu
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Student Activities menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_student_activity"]',
                },
                {
                    content: "Open the Payment Term Amendments menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_payment_term_amendment.school_payment_term_amendment_menu"]',
                },
                {
                    content: "Payment Term Amendments list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Payment Term Amendments)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 2 — Open the record whose assigned policy
                // template should be re-evaluated
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(TOUR PTA Reason Reload Template) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 — On the Policies tab, click Reload Template
                // Policy
                {
                    content: "Open the Policies tab",
                    trigger: ".o_notebook .nav-link:contains(Policies)",
                },
                {
                    content: "Click Reload Template Policy",
                    trigger: "button[name='action_reload_policy_template']",
                },

                // Post-Condition — Policy Template is recomputed and
                // re-assigned (still "Standard", the only template
                // this module ships, so the visible field keeps
                // showing the same value across the reload)
                {
                    content: "Policy Template is assigned",
                    trigger:
                        ".o_field_widget[name='policy_template_id']:contains(Standard)",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
