# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>

# Author: Charifsoltani <soltani.charif@gmail.com>.
# Contributions:
#               - Charif Soltani

{
    'name': 'Search & Group by Product Attributes',
    'category': 'Inventory/Product',
    'summary': "Analyze your sales data with attribute",
    'depends': [
        'product',
        # uncomment any module that you're using, don't forget to uncomment it also in the __init__.py file of module
        'account',
        'sale',
        'stock',
        # 'purchase',
        # 'stock_enterprise',
    ],
    'data': [
         # views
        'views/res_config_settings_views.xml',
        'views/product_attribute_views.xml',
    ],
    'images': [
        'static/description/cover.png',
    ],
    'version': '16.0',
    "author": "Charif SOLTANI",
    'support': "soltani.charif@gmail.com",
    'website': 'www.linkedin.com/in/charif-soltani-b0351811a',
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
