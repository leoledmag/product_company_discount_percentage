# -*- coding: utf-8 -*-
# Apply product company discount by default in Sales without materializing prices.
from odoo import api, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def _onchange_product_id_company_discount(self):
        """
        When selecting a product, if it has x_company_discount_percentage set,
        compute price_unit using the matching company discount pricelist.
        Falls back to the order pricelist if not found.
        """
        for line in self:
            if not line.product_id or not line.order_id:
                continue
            # Get percentage from template (works for variants)
            tmpl = line.product_id.product_tmpl_id
            pct = tmpl.x_company_discount_percentage or 0
            if pct < 1 or pct > 100:
                continue

            company = line.company_id or line.order_id.company_id
            pricelist_name = line._get_pricelist_name(pct)
            pl = self.env["product.pricelist"].sudo().search([
                ("name", "=", pricelist_name),
                ("company_id", "=", company.id)
            ], limit=1)

            # Compute price with discount pricelist if available
            product = line.product_id.with_context(lang=line.order_id.partner_id.lang)
            qty = line.product_uom_qty or 1.0
            partner = line.order_id.partner_id

            target_pricelist = pl or line.order_id.pricelist_id
            if target_pricelist:
                price = target_pricelist.with_context(uom=line.product_uom.id).get_product_price(
                    product, qty, partner)
                if price is not False:
                    line.price_unit = price

    def _get_pricelist_name(self, pct):
        return self.env._("Company Discount %s%%") % int(pct)