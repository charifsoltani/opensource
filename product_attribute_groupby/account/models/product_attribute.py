# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>

from odoo import models, api


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    @api.model
    def _models_list(self):
        return super(ProductAttribute, self)._models_list() + ['account.invoice.report']
