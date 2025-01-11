# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>

from odoo import models, api


class StoredProductAttribute(models.Model):
    _inherit = 'stored.product.attribute'

    def _prepare_field_vals(self, model):
        vals = super(StoredProductAttribute, self)._prepare_field_vals(model)
        # in product.product the field is computed based on the attributes.
        if model in ['stock.quant', 'stock.move', 'stock.move.line', 'stock.valuation.layer']:
            vals.update({
                'related': "product_id.%s" % self.technical_name,
                'index': 1,
            })
        return vals

    @api.model
    def _models_list(self):
        return super(StoredProductAttribute, self)._models_list() + ['stock.quant', 'stock.move', 'stock.move.line', 'stock.valuation.layer']

