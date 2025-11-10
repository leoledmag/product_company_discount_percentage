# -*- coding: utf-8 -*-
# Manifest for "Company Discount Percentage"
{
    "name": "Company Discount Percentage",
    "summary": "Automatic per-company discount pricelists (1%â€“100%) + dynamic default discount in Sales",
    "version": "1.0.0",
    "category": "Sales/Price Lists",
    "author": "Leonardo Ledesma Maguilla",
    "website": "https://github.com/leoledmag/product_company_discount_percentage",
    "license": "LGPL-3",
    "depends": ["sale_management", "product"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_config_parameter.xml",
        "data/discount_pricelists.xml",
        "views/res_config_settings_views.xml",
        "views/product_template_views.xml",
        "views/menu_company_discount.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "product_company_discount_percentage/static/description/icon.png"
        ]
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "maintainers": ["leoledmag"],
    "support": "leoledmag@github"
}