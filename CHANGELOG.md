# Changelog

All notable changes to JSPL are documented in this file.

Versioning follows [Semantic Versioning](https://semver.org/): MAJOR for breaking changes, MINOR for backward-compatible features, and PATCH for backward-compatible fixes.

## [1.0.0] - 2026-09-03

### Added

- **Blanket Booking Order** (submittable): a Blanket Order-style agreement scoped to Item Group instead of Item Code, for Selling or Purchasing. Includes a Currency section (collapsed by default) with exchange rate, a From/To Date range, and a Terms and Conditions section.
- **Blanket Booking Order Item**: child table capturing Item Group, Quantity, Rate, Rate (Company Currency), and Ordered Quantity.
- Purchase Order Item now carries a required **Blanket Booking Order** field, filtered to submitted, Purchasing Blanket Booking Orders for the order's supplier.
- Submitting a Purchase Order validates every Blanket Booking Order referenced by its items: the BBO must be submitted, Purchasing, and for the same supplier; each referenced Item Group must actually be listed on that BBO; and the quantity booked per Item Group must stay within the BBO row's remaining quantity plus the Buying Settings → Blanket Order Allowance.
- A Blanket Booking Order's **Ordered Quantity** per Item Group is kept in sync automatically — it increases when a linked Purchase Order is submitted and decreases when that order is cancelled.
