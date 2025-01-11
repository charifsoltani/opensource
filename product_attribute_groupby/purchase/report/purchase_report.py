# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>
from lxml import etree

from odoo import models, api
from odoo.tools import odoo_resolver


class PurchaseReport(models.Model):
    _name = 'purchase.report'
    _inherit = ['purchase.report', 'stored.product.attribute.mixin']

    @api.model
    def _select(self):
        _select = super(PurchaseReport, self)._select()
        for attribute_custom_field in self.env['stored.product.attribute'].search([('state', '=', 'confirm')]):
            if attribute_custom_field._exists_in_model(self._name):
                _select += f""",\n p.{attribute_custom_field.technical_name} as {attribute_custom_field.technical_name}"""
        return _select

    @api.model
    def _group_by(self):
        _group_by = super(PurchaseReport, self)._group_by()
        for attribute_custom_field in self.env['stored.product.attribute'].search([('state', '=', 'confirm')]):
            if attribute_custom_field._exists_in_model(self._name):
                _group_by += f""",\n p.{attribute_custom_field.technical_name}"""
        return _group_by
