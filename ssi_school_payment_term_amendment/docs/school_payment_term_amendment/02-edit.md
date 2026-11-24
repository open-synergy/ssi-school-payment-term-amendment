# Edit School Payment Term Amendment

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
2. Open the record to edit.
3. Change any of the editable fields: **Enrollment**, **Reason**, **Date**, the **Line**
   table (add, edit, or remove lines), or **Note**.
4. Click **Save**.

## Post-Condition

- The changes are saved.
- The record still shows **Draft** on the statusbar, with the **Confirm** button
  available in the header.
