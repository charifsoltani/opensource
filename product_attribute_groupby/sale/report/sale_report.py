# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>
from lxml import etree


from odoo import models


class SaleReport(models.Model):
    _name = 'sale.report'
    _inherit = ['sale.report', 'stored.product.attribute.mixin']

    def _select_additional_fields(self):
        """ add all activated field to `sale.report` """
        res = super()._select_additional_fields()
        for attribute_custom_field in self.env['product.attribute'].search([('is_stored', '=', True)]):
            if attribute_custom_field._exists_in_model(self._name):
                res[attribute_custom_field.technical_name] = f"p.{attribute_custom_field.technical_name}"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        for attribute_custom_field in self.env['product.attribute'].search([('is_stored', '=', True)]):
            if attribute_custom_field._exists_in_model(self._name):
                res += f""",
                    p.{attribute_custom_field.technical_name}"""
        return res
