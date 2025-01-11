# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>

from odoo import models


class StockQuant(models.Model):
    _name = 'stock.quant'
    _inherit = ['stock.quant', 'stored.product.attribute.mixin']


class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = ['stock.move', 'stored.product.attribute.mixin']


class StockMoveLine(models.Model):
    _name = 'stock.move.line'
    _inherit = ['stock.move.line', 'stored.product.attribute.mixin']


class StockValuationLayer(models.Model):
    _name = 'stock.valuation.layer'
    _inherit = ["stock.valuation.layer", 'stored.product.attribute.mixin']
