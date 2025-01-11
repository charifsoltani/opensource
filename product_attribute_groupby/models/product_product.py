# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>


from odoo import models


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'stored.product.attribute.mixin']

    def _get_custom_field_config(self, field_name):
        return self.env['product.attribute'].search([('technical_name', '=', field_name)], limit=1)

    def _attribute_value_by_product_product(self, custom_field_name):
        """ return dict where {product_id: attribute value}. """
        if not self:
            return {}
        custom_field = self._get_custom_field_config(field_name=custom_field_name)
        self.env['product.template.attribute.value'].flush_model()
        self._cr.execute("""
        SELECT 
              pvc.product_product_id,
              ptav.product_attribute_value_id
        FROM product_variant_combination pvc
              INNER JOIN product_template_attribute_value ptav on ptav.id = pvc.product_template_attribute_value_id
        WHERE
           ptav.attribute_id = %s 
           AND pvc.product_product_id in %s
        """, [custom_field.id or 0, tuple(self.ids)])
        return dict(self._cr.fetchall())


