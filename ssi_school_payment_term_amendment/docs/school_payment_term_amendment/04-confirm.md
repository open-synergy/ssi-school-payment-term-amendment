# Confirm School Payment Term Amendment

> **Module:** `ssi_school_payment_term_amendment`
>
> **Model:** `school_payment_term_amendment`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Amendments
>
> **Actor:** user in group _School Payment Term Amendment — User_
>
> **State:** `draft` → `confirm`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** The Enrollment is in status **Open** or **Done**.
- **Record:** The document has at least one line.
- **Record:** Every targeted Payment Term belongs to the Enrollment and has no Customer
  Invoice yet.
- **Record:** Every targeted Detail belongs to its Payment Term, has no Customer Invoice
  Line yet, and is not already voided. A detail appears on only one Void Detail or
  Change Price line, and every Add Term line is used by at least one Add Detail line.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Config:** An active `sequence.template` exists for this model.
- **Access:** User is in group _School Payment Term Amendment — User_.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Amendments** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
- No payment term or detail line has been changed yet -- the amendment is only applied
  once the document reaches **Done**.
