# Intern Sales Discount Approval

Odoo 19.0 Community module that extends `sale.order` with a manager approval step for high line discounts.

## Features

- Adds a computed `requires_approval` field on sales orders.
- Marks an order as requiring approval when any non-section order line has `discount > 10`.
- Adds a new sale order state `to_approve` for orders waiting for discount approval.
- Moves draft/sent orders to `to_approve` when a user tries to confirm an unapproved high-discount order.
- Adds an **Approve Discount** button for users in the **Discount Approver** group.
- Approval marks `discount_approved`, stores `discount_approved_by`, and returns the order to draft so it can be confirmed normally.
- Resets approval when an approved order line discount is changed.
- Includes TransactionCase tests for direct confirmation, approval blocking, approval flow, and approval reset.

## Installation

1. Put this repository's `custom_addons` directory in the Odoo addons path.
2. Start Odoo 19.0 Community with the sale module available, for example:

   ```bash
   odoo-bin -d <database> --addons-path=<odoo-addons>,custom_addons --dev=all
   ```

3. Enable Developer Mode.
4. Update Apps List.
5. Install **Intern Sales Discount Approval**.
6. Add users who can approve discount requests to the **Discount Approver** group.

## Assumptions

- The target version is Odoo 19.0 Community.
- The module depends on the standard `sale` module.
- A sale order requires approval when at least one order line discount is greater than 10%.
- Approved orders are returned to `draft` after approval, matching the assignment requirement.
