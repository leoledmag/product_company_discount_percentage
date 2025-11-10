# Company Discount Percentage

**Author:** Leonardo Ledesma Maguilla  
**GitHub:** [leoledmag](https://github.com/leoledmag)  
**License:** LGPL-3  
**Compatibility:** Odoo 15.0 â†’ 19.0

## Overview
Creates **100 company discount pricelists (1% -> 100%)** per company and applies a per-product discount **by default in Sales** via SO line pricing, without materializing prices.

## Features
- Auto-generate discount pricelists 1% -> 100% per company.
- Default discount in Sales based on product field **Company Discount (%)**.
- Configurable base: `list_price` (default) or `standard_price`.
- Multi-company, 15 languages, low-priority pricelists.
- Admin menu to review pricelists.

## Installation
1. Copy the module folder into your addons path.
2. Update Apps, install **Company Discount Percentage**.

## Configuration
**Sales â†’ Settings â†’ Company Discount**  
Pick the base field used in generated pricelist items.

## Usage
Set **Company Discount (%)** on the product (1â€“100).  
When adding the product to a Sales Order, the line price is computed using the matching **Company Discount X%** pricelist for the company. If not found, the order pricelist is used.

## Notes
- No change to stored product prices.
- Works across Odoo 15â€“19 core pricelist models.

## Contributing
See `CONTRIBUTING.md`.

## Changelog
See `CHANGELOG.md`.
