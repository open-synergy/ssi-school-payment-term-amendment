# Delete School Payment Term Amendment

> **Module:** `ssi_school_payment_term_amendment`
>
> **Model:** `school_payment_term_amendment`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Amendments
>
> **Actor:** user in group _School Payment Term Amendment — User_
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _School Payment Term Amendment — User_.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Amendments** menu.
2. Select the record to delete (or open it).
3. Click the **Action** menu, then **Delete**. When deleting from the list, select the
   record's checkbox first.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- The Payment Term Amendment document, along with all of its lines, no longer exists.
- The enrollment's payment terms and their detail lines are unaffected.
