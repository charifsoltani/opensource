# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>
import re

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    is_stored = fields.Boolean(
        string="Is Stored",
        compute="_compute_is_stored",
        store=True,
    )
    technical_name = fields.Char(
        string='Technical field name',
        help="Technical name of the field that will be created in the product.product model.\n"
             "please don't use special characters or spaces instead user pattern like this:\n"
             "- `x_{id}_color_value`\n"
             "- `x_{id}_size_value`\n"
             "Keep the name in english and unique.",
    )
    name = fields.Char(inverse="_inverse_name")
    technical_name_suggestion = fields.Char(compute="_compute_technical_name_suggestion")
    field_ids = fields.Many2many('ir.model.fields', compute="_compute_stored_fields")
    # views related fields
    show_in_filters = fields.Boolean("Show In Search View Suggestion", default=1)
    show_in_group_by = fields.Boolean("Show In Search View Group by", default=1)

    _sql_constraints = [
        ('attribute_uniq', 'unique (technical_name)', "Technical name must be unique"),
    ]

    @api.constrains("technical_name")
    def _check_technical_name(self):
        for rec in self.filtered('technical_name'):
            if not re.match(r'^[1-9a-z_]+$', rec.technical_name):
                raise UserError("Technical name must be in lowercase and separated by underscore, you can only use alpha and numeric charcaters.")
            if not rec.technical_name.startswith(f'x_{rec.id}_'):
                raise UserError(_("For technical reason technical must start with `x_%s_`") % rec.id)

    @api.depends('name')
    def _compute_technical_name_suggestion(self):
        for rec in self:
            rec.technical_name_suggestion = f"x_{rec._origin.id}_{re.sub(r'W', '_', rec.name.lower())}_value"

    @api.depends('field_ids')
    def _compute_is_stored(self):
        for rec in self:
            rec.is_stored = len(rec.field_ids) > 0

    def _inverse_name(self):
        self.flush_model(['name'])
        cr = self.env.cr
        for rec in self.filtered('is_stored'):
            for field in rec.field_ids:
                cr.execute("""
                UPDATE ir_model_fields SET field_description = attr.name
                FROM product_attribute attr
                WHERE ir_model_fields.id = %s and attr.id = %s
                """, (field.id, rec.id))

    @api.depends('technical_name')
    def _compute_stored_fields(self):
        for rec in self:
            rec.field_ids = self.env['ir.model.fields']
            for model in self._models_list():
                rec.field_ids += rec._exists_in_model(model)

    def _prepare_field_vals(self, model):
        vals = {
            'model': model,
            'model_id': self.env['ir.model']._get_id(model),
            'name': self.technical_name,
            'field_description': self.name,
            'relation': 'product.attribute.value',
            'domain': f"[('attribute_id', '=', {self.id})]",
            'copied': False,
            'store': True,
            'ttype': 'many2one'
        }
        # in product.product the field is computed based on the attributes.
        if model == 'product.product':
            vals.update({
                'compute': "result = self._attribute_value_by_product_product('%s')\n"
                           "for rec in self:\n"
                           "    rec['%s'] = result.get(rec.id)" % (self.technical_name, self.technical_name),
                'depends': 'combination_indices',
                'index': 1,
            })
        return vals

    def _exists_in_model(self, model):
        return self.env['ir.model.fields'].sudo()._get(model, self.technical_name)

    @api.model
    def _models_list(self):
        return ['product.product']

    def action_create_fields(self):
        """ create custom fields and store them in m2m field"""
        self._check_technical_name()
        ModelFields = self.env['ir.model.fields']
        for rec in self:
            for model in self._models_list():
                field = rec._exists_in_model(model)
                if not field:
                    field += ModelFields.sudo().create(rec._prepare_field_vals(model))
                rec.field_ids += field
        self.write(dict(is_stored=True))
        self._inverse_name()
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def _remove_fields(self):
        """ delete product.variant fields in last. """
        for field in reversed(self.field_ids.sorted(lambda f: f.model_id.name == 'product.product')):
            field.unlink()
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_delete_fields(self):
        self._remove_fields()
        return self.write(dict(is_stored=False))

    def unlink(self):
        self._remove_fields()
        return super(ProductAttribute, self).unlink()
