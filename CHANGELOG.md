# Changelog

All notable changes to JSPL are documented in this file.

Versioning follows [Semantic Versioning](https://semver.org/): MAJOR for breaking changes, MINOR for backward-compatible features, and PATCH for backward-compatible fixes.

## [2.0.0] - 2026-09-07

### Added

- Blanket Booking Order now has a **Status** field: Draft, To Order (Ordered Quantity is 0), Partially Ordered (Ordered Quantity less than Quantity), Completed (Ordered Quantity reaches Quantity), On Hold, Closed, Cancelled. It's computed automatically from Ordered Quantity on every save and whenever a linked Purchase/Sales Order is submitted or cancelled - except while manually On Hold or Closed, where it stays put until explicitly cleared.
- Manual **Hold** (prompts for a reason, logged as a comment) / **Resume**, and **Close** / **Re-open** actions on a submitted Blanket Booking Order, mirroring Sales Order's own workflow. Only available to users with submit permission; unavailable once a Blanket Booking Order is Completed.
- A Closed Blanket Booking Order can no longer be cancelled directly - it must be Re-opened first; cancelling any Blanket Booking Order now also sets its status to Cancelled.
- On Hold / Closed Blanket Booking Orders are excluded from the Blanket Booking Order picker on Purchase/Sales Order items, and rejected server-side if one is referenced anyway.
- The list view now shows a colored status indicator instead of the generic Draft/Submitted/Cancelled badge.

### Changed

- Blanket Booking Order Item's Rate (and Rate in Company Currency) is no longer mandatory. The Purchase/Sales Order item's rate is only overridden when a Rate is actually set on the matching Blanket Booking Order row; if it's left blank, the order's own rate is used as-is.
- Renamed the Blanket Booking Order Item checkbox label from "Allow Overvaluation Purchase/Sales" to **"Allow Over Purchase/Sale"**, and added it to the list view.

### Fixed

- The client-side check that validates a row's Item Group against its Blanket Booking Order (and prefills Rate) could momentarily read the *previous* item's Item Group right after changing Item Code, since Item Group is fetched asynchronously - causing a spurious "Item Group not listed" error and clearing the Blanket Booking Order selection. It now resolves the Item's group itself and re-checks the row hasn't changed again before acting on either lookup's result.

## [1.0.0] - 2026-09-03

### Added

- **Blanket Booking Order** (submittable): a Blanket Order-style agreement scoped to Item Group instead of Item Code, for Selling or Purchasing. Includes a Currency section (collapsed by default) with exchange rate, a From/To Date range, and a Terms and Conditions section.
- **Blanket Booking Order Item**: child table capturing Item Group, Quantity, Rate, Rate (Company Currency), and Ordered Quantity.
- **Allow Overvaluation Purchase/Sales** checkbox on Blanket Booking Order Item — when checked, that row's quantity-allowance check is skipped, so the linked Purchase/Sales Order can book more than the committed Quantity for that Item Group.
- Purchase Order Item and Sales Order Item each carry a required **Blanket Booking Order** field, filtered to submitted Blanket Booking Orders of the matching Order Type (Purchasing/Selling) for the order's supplier/customer, and whose From/To Date covers the order's Transaction Date.
- Once a row has a Blanket Booking Order, its Item Code picker is restricted to Items whose Item Group is listed on that BBO — two rows on the same order can reference two different BBOs and each only see their own BBO's Item Groups.
- Submitting a Purchase Order or Sales Order validates every Blanket Booking Order referenced by its items: the BBO must be submitted, of the matching Order Type, for the same supplier/customer, its validity must cover the order's Transaction Date, each referenced Item Group must actually be listed on that BBO, and the quantity booked per Item Group must stay within the BBO row's remaining quantity plus the Buying/Selling Settings → Blanket Order Allowance (unless that row has Allow Overvaluation checked).
- Purchase/Sales Order item Rate is overridden from the linked Blanket Booking Order Item's Rate (converted into the order's currency) every time the order is saved, so it can't drift from the committed BBO rate.
- A Blanket Booking Order's **Ordered Quantity** per Item Group is kept in sync automatically — it increases when a linked Purchase Order or Sales Order is submitted and decreases when that order is cancelled.
- Changing the Supplier on a Purchase Order (or Customer on a Sales Order) clears any Blanket Booking Order already selected on its items, since that selection is only valid for the party it was chosen against.

### Fixed

- A client-side lookup used to validate a row's Item Group against its Blanket Booking Order (and to prefill Rate) omitted the parent doctype on a permission-checked child-table read. This could fail permission silently and be misread as "Item Group not listed", clearing the row's Blanket Booking Order and leaving Rate un-overridden even when the BBO genuinely listed that Item Group.
