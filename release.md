# Release Notes

## v1.0.0 — 2026-09-03

Initial release of JSPL.

This release introduces **Blanket Booking Order**: an item-group-level companion to ERPNext's Blanket Order. It lets you commit quantities and a rate against an Item Group (rather than a specific Item Code) for a customer or supplier over a date range — for both Purchasing and Selling.

Purchase Orders and Sales Orders are both integrated with it end to end:

- Each order item can be tied to a submitted Blanket Booking Order for the same party, valid for that order's date, and is then restricted to Item Codes from that BBO's Item Group.
- The order's rate is kept in lockstep with the rate committed on the BBO.
- Booking more than the committed quantity is blocked by default, unless a Blanket Booking Order Item row is explicitly marked to allow it.
- Each Blanket Booking Order tracks, per Item Group, how much has actually been ordered — automatically, as Purchase/Sales Orders are submitted or cancelled.

For the full, version-by-version list of what was added, changed, updated, and removed, see [CHANGELOG.md](CHANGELOG.md).
