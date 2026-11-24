# Approve School Payment Term Amendment

> **Module:** `ssi_school_payment_term_amendment`
>
> **Model:** `school_payment_term_amendment`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Amendments
>
> **Actor:** approver on the pending approval level, in group _School Payment Term
> Amendment — Validator_
>
> **State:** `confirm` → `done`
>
> **Requires:** `04-confirm`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Record:** No targeted Payment Term has received a Customer Invoice since Confirm --
  if one has, Approve fails and the term that is already invoiced is named in the error.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. When the template uses sequential approval, only the first unapproved
  level is pending.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Amendments** menu.
2. Open the record to approve.
3. Click the **Approve** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
- If all approval levels are fulfilled, status changes automatically to **Done** and the
  amendment is applied, in this order: every **Add Term** line creates its payment term;
  every **Add Detail** line creates its detail line on the target term; every **Change
  Price** line writes the new unit price on its detail; every **Void Detail** line marks
  its detail as voided, so it no longer counts toward the term and enrollment totals and
  is never billed, while its original price stays visible. New terms and details are
  locked. Terms and details that no line mentions are unchanged. The enrollment's
  chatter receives a message summarising the amendment with a link back to this
  document. Once Done, the amendment is terminal and can no longer be cancelled or
  reverted -- to undo it, create a new amendment.

> **Note:** `school_payment_term_amendment` has no manual Done button
> (`_automatically_insert_done_button` is disabled). The transition to **Done** always
> happens automatically as soon as the last approval level is fulfilled -- there is no
> `07-start.md`, `08-open.md`, or `09-finish.md` for this model.
