# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>

from odoo import models, api


class StoredProductAttribute(models.Model):
    _inherit = 'stored.product.attribute'

    @api.model
    def _models_list(self):
        return super(StoredProductAttribute, self)._models_list() + ['purchase.report']

