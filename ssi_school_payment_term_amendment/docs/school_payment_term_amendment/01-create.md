# Create School Payment Term Amendment

> **Module:** `ssi_school_payment_term_amendment`
>
> **Model:** `school_payment_term_amendment`
>
> **Menu:** School ‣ Student Activities ‣ Payment Term Amendments
>
> **Actor:** user in group _School Payment Term Amendment — User_
>
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** An Enrollment in status **Open** or **Done** exists for the student, with at
  least one Payment Term that has no customer invoice yet.
- **Data:** For a Void Detail or Change Price line, that Payment Term has at least one
  detail line with no customer invoice line yet that is not already voided.
- **Data:** A Payment Term Amendment Reason exists (see
  `school_payment_term_amendment_reason/01-create`).
- **Access:** User is in group _School Payment Term Amendment — User_.

## Flow

1. Open the **School ‣ Student Activities ‣ Payment Term Amendments** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Enrollment** _(required)_: Select the open or done enrollment whose payment terms
     are amended. Selecting it fills Student, Academic Year, and Academic Term
     automatically.
   - **Reason** _(required)_: Select why the payment terms are amended.
4. **Date** is filled with today's date automatically; change it if needed.
5. Open the **Amendment Detail** tab.
6. In the **Line** table, click **Add a line** and fill in:
   - **Operation** _(required)_: Select what the line does -- **Void Detail** (the
     detail stops being billed, its price stays visible), **Change Price** (the detail
     gets a new unit price, higher or lower), **Add Detail** (a new detail is added to a
     payment term), or **Add Term** (a new payment term is created).
   - **Payment Term** _(required for Void Detail and Change Price)_: Select the payment
     term to amend. Only payment terms of the selected Enrollment that have no customer
     invoice yet are selectable. For **Add Detail**, select it or **New Term**.
   - **Detail** _(required for Void Detail and Change Price)_: Select the detail line to
     amend. Only detail lines of the selected Payment Term that have no customer invoice
     line yet and are not already voided are selectable. **Price Before** is filled
     automatically.
   - **Price Unit** _(required for Change Price and Add Detail)_: For **Change Price**,
     enter the new unit price (it is proposed from the current one).
   - For **Add Detail**, also fill **Product**, **Description**, **Account**, **UoM**,
     **UoM Quantity**, **Price Unit**, and **Tax(es)** as needed, and either **Payment
     Term** or **New Term** (the **Add Term** line of this same document -- save the
     document first so that line can be selected).
   - For **Add Term**, fill **New Term Name** _(required)_, **New Term Sequence**,
     **Estimated Invoice Date**, and **Estimated Due Date**. Then add one **Add Detail**
     line per fee of that term, pointing at it through **New Term**.
7. Repeat step 6 for additional lines. A detail can appear on only one Void Detail or
   Change Price line.
8. Optionally fill in **Note** with a free-form explanation.
9. Click **Save**.

## Post-Condition

- A new Payment Term Amendment document is created in **Draft** status. It has no
  document number yet.
- The document does not write anything to the payment terms or their detail lines yet --
  the change only takes effect after approval (see `05-approve`).
- The **Confirm** button is visible in the header (usable once the prerequisites in
  `04-confirm` are met), and the statusbar shows **Draft ‣ Waiting for Approval ‣
  Done**.
- The Enrollment shows an **Amendments** smart button counting the amendment documents
  of that enrollment.
