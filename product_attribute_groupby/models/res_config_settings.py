# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    stored_product_attributes_ids = fields.Many2many("stored.product.attribute",
                                                     compute="_compute_stored_product_attributes")

    @api.depends('company_id')
    def _compute_stored_product_attributes(self):
        self.stored_product_attributes_ids = self.env['stored.product.attribute'].search([('state', '=', 'confirm')])