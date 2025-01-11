# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>

from odoo import models, api


class StockReport(models.Model):
    _name = 'stock.report'
    _inherit = ['stock.report', 'stored.product.attribute.mixin']

    @api.model
    def _select(self):
        _select = super(StockReport, self)._select()
        for attribute_custom_field in self.env['product.attribute'].search([('is_stored', '=', True)]):
            if attribute_custom_field._exists_in_model(self._name):
                _select += f""",\n p.{attribute_custom_field.technical_name} as {attribute_custom_field.technical_name}"""
        return _select

    def _group_by(self):
        group_by_str = super(StockReport, self)._group_by()
        for attribute_custom_field in self.env['product.attribute'].search([('is_stored', '=', True)]):
            if attribute_custom_field._exists_in_model(self._name):
                group_by_str += f""",\n p.{attribute_custom_field.technical_name}"""
        return group_by_str
