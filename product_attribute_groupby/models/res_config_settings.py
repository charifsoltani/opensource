# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    stored_product_attributes_ids = fields.Many2many(
        comodel_name="product.attribute",
        compute="_compute_stored_product_attributes",
        string="Stored Product Attributes",
    )

    @api.depends('company_id')
    def _compute_stored_product_attributes(self):
        self.stored_product_attributes_ids = self.env['product.attribute'].search([('is_stored', '=', True)])