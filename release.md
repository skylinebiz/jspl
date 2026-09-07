# Release Notes

## v2.0.0 — 2026-09-07

Blanket Booking Order now has a lifecycle of its own, matching Sales Order's Hold/Close workflow:

- A **Status** field tracks it automatically as **Draft → To Order → Partially Ordered → Completed**, based on how much of its committed quantity has actually been ordered.
- It can be manually put **On Hold** (with a reason) or **Closed**, and later **Resumed** or **Re-opened** - while held or closed, it's excluded from the picker on new Purchase/Sales Order items and status stops auto-updating until it's cleared. A Completed order can't be Held or Closed, and a Closed one can't be cancelled without reopening it first.
- The list view shows this status as a proper colored indicator instead of the generic Draft/Submitted/Cancelled badge.

Alongside that: a Blanket Booking Order Item's Rate is now optional (the order's rate is only overridden when one is actually set), its "Allow Over Purchase/Sale" checkbox is easier to spot in the grid, and a timing bug that could flash a false "Item Group not listed" error - and silently drop the Blanket Booking Order - right after switching an item is fixed.

## v1.0.0 — 2026-09-03

Initial release of JSPL.

This release introduces **Blanket Booking Order**: an item-group-level companion to ERPNext's Blanket Order. It lets you commit quantities and a rate against an Item Group (rather than a specific Item Code) for a customer or supplier over a date range — for both Purchasing and Selling.

Purchase Orders and Sales Orders are both integrated with it end to end:

- Each order item can be tied to a submitted Blanket Booking Order for the same party, valid for that order's date, and is then restricted to Item Codes from that BBO's Item Group.
- The order's rate is kept in lockstep with the rate committed on the BBO.
- Booking more than the committed quantity is blocked by default, unless a Blanket Booking Order Item row is explicitly marked to allow it.
- Each Blanket Booking Order tracks, per Item Group, how much has actually been ordered — automatically, as Purchase/Sales Orders are submitted or cancelled.

For the full, version-by-version list of what was added, changed, updated, and removed, see [CHANGELOG.md](CHANGELOG.md).
