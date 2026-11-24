# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Payment Term Amendment",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_company_currency_mixin",
        "ssi_product_line_account_mixin",
        "web_tour",
    ],
    "data": [
        "security/ir_module_category/school_payment_term_amendment.xml",
        "security/res_groups/school_payment_term_amendment_reason.xml",
        "security/res_groups/school_payment_term_amendment.xml",
        "security/ir_model_access/school_payment_term_amendment_reason.xml",
        "security/ir_model_access/school_payment_term_amendment.xml",
        "security/ir_rule/school_payment_term_amendment.xml",
        "ir_sequence/school_payment_term_amendment.xml",
        "sequence_template/school_payment_term_amendment.xml",
        "approval_template/school_payment_term_amendment.xml",
        "policy_template/school_payment_term_amendment.xml",
        "views/school_payment_term_amendment_reason.xml",
        "views/school_payment_term_amendment.xml",
        "views/school_enrollment.xml",
        "views/assets.xml",
    ],
}
