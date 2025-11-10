# -*- coding: utf-8 -*-
# Core: product fields + pricelist auto-generation + config
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

BASE_FIELD_PARAM = "company_discount_percentage.base_price_field"

class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_company_discount_percentage = fields.Integer(
        string="Company Discount (%)",
        help="Discount to apply by default in Sales for this product. Range 1â€“100.",
        default=1,
        required=True
    )

    @api.constrains("x_company_discount_percentage")
    def _check_discount_range(self):
        for rec in self:
            if not (1 <= rec.x_company_discount_percentage <= 100):
                raise ValidationError(_("Discount must be between 1 and 100."))

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    company_discount_base_field = fields.Selection(
        selection=[
            ("list_price", "Public Price (list_price)"),
            ("standard_price", "Cost Price (standard_price)"),
        ],
        string="Base field for company discount calculation",
        default="list_price",
        config_parameter=BASE_FIELD_PARAM,
        help="Select the product price field used as the base for generated pricelist percentage."
    )

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @api.model
    def _company_discount_item_vals(self, percent):
        """Build a pricelist item dict applying -percent on selected base field."""
        # Map config -> item 'base' selection across v15â†’v19
        param = self.env["ir.config_parameter"].sudo().get_param(BASE_FIELD_PARAM, "list_price")
        base = "list_price" if param not in ("standard_price",) else "standard_price"
        return {
            "applied_on": "3_global",     # global rule
            "compute_price": "percentage",
            "percent_price": -float(percent),
            # 'base' exists in v15â€“v19 to choose list or cost
            "base": base,
        }

    @api.model
    def create_company_discount_pricelists(self):
        """Generate 100 discount pricelists (1%â€“100%) per company, with lowest priority."""
        companies = self.env["res.company"].search([])
        for company in companies:
            for p in range(1, 101):
                name = _("Company Discount %s%%") % p
                pl = self.search([("name", "=", name), ("company_id", "=", company.id)], limit=1)
                if pl:
                    # Ensure at least one global rule exists
                    if not pl.item_ids:
                        self.env["product.pricelist.item"].create(
                            dict(self._company_discount_item_vals(p), pricelist_id=pl.id)
                        )
                    continue
                pl = self.create({
                    "name": name,
                    "company_id": company.id,
                    # sequence low priority (higher number means lower priority in pricelist matching UI)
                    "sequence": 99,
                    "discount_policy": "without_discount",
                })
                self.env["product.pricelist.item"].create(
                    dict(self._company_discount_item_vals(p), pricelist_id=pl.id)
                )