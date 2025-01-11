# -*- coding: utf-8 -*-
# Author - Soltani Charif <https://www.linkedin.com/in/soltani-charif-b0351811a/>
import re

from lxml import etree

from odoo import models, fields, api


class StoredProductMixin(models.AbstractModel):
    """ Mixin that override get_view to add activated fields in search view. """
    _name = 'stored.product.attribute.mixin'
    _description = "Stored Attribute Mixin"

    def get_view(self, view_id=None, view_type='form', **options):
        """ force label of field to be contact person."""
        result = super(StoredProductMixin, self).get_view(view_id=view_id, view_type=view_type, **options)
        if view_type != 'search':
            return result

        doc = etree.fromstring(result['arch'])
        # add filters
        groupby = doc.xpath("//filter[contains(@context, 'group_by')]/..")
        if not groupby:
            return result
        groupby = groupby[0]
        ModelField = self.env['ir.model.fields']
        groupby.addprevious(etree.Element('separator', {}))
        groupby.append(etree.Element('separator', {}))
        for attribute_custom_field in self.env['stored.product.attribute'].search([('state', '=', 'confirm')]):
            if not attribute_custom_field._exists_in_model(self._name):
                continue
            _field = ModelField._get('product.product', attribute_custom_field.technical_name)
            if attribute_custom_field.show_in_filters:
                groupby.addprevious(etree.Element('field', {'name': _field.name, 'domain': _field.domain}))
            if attribute_custom_field.show_in_group_by:
                groupby.append(etree.Element('filter', {'string': _field.field_description, 'context': "{'group_by':'%s'}" % _field.name}))

        result['arch'] = etree.tostring(doc, encoding="unicode").replace('\t', '')
        return result


class StoredProductAttribute(models.Model):
    _name = 'stored.product.attribute'
    _description = 'stored product attribute'
    _rec_name = 'attribute_id'

    state = fields.Selection([
        ('draft', 'Not Stored'),
        ('confirm', 'Stored')
    ], 'State', readonly=True, default='draft')
    show_in_filters = fields.Boolean("Show In Search View Suggestion", default=1)
    show_in_group_by = fields.Boolean("Show In Search View Group by", default=1)
    attribute_id = fields.Many2one('product.attribute', 'Product Attribute', required=True)
    technical_name = fields.Char('Technical field name', required=True)
    field_ids = fields.Many2many('ir.model.fields',
                                 'ir_field_product_rel',
                                 'stored_field_id',
                                 'field_id',
                                 'Fields',)
    field_description = fields.Char(compute="_compute_field_data", inverse="_set_field_data", translate=True)
    field_help = fields.Text(compute="_compute_field_data", inverse="_set_field_data", translate=True)

    _sql_constraints = [
        ('attribute_uniq', 'unique (attribute_id)', "You can activate only one field by attribute"),
    ]

    @api.depends('field_ids.field_description', 'field_ids.help')
    def _compute_field_data(self):
        for rec in self:
            rec.field_description = rec.field_ids[:1].field_description
            rec.field_help = rec.field_ids[:1].help

    def _set_field_data(self):
        for rec in self:
            rec.field_ids.write(dict(
                field_description=rec.field_description,
                help=rec.field_help,
            ))

    @api.onchange('attribute_id')
    def _onchange_attribute(self):
        for rec in self.filtered(lambda r: r.attribute_id):
            rec.technical_name = 'x_' + '_'.join(re.split(r"\W", rec.attribute_id.name.lower())) + '_value'
            rec.field_description = rec.attribute_id.name

    def _prepare_field_vals(self, model):
        vals = {
            'model': model,
            'model_id': self.env['ir.model']._get_id(model),
            'name': self.technical_name,
            'field_description': self.attribute_id.name,
            'relation': 'product.attribute.value',
            'domain': f"[('attribute_id', '=', {self.attribute_id.id})]",
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
        ModelFields = self.env['ir.model.fields']
        for rec in self:
            for model in self._models_list():
                field = rec._exists_in_model(model)
                if not field:
                    field += ModelFields.sudo().create(rec._prepare_field_vals(model))
                rec.field_ids += field
        self.write(dict(state='confirm'))

    def _remove_fields(self):
        """ delete product.variant fields in last. """
        for field in reversed(self.field_ids.sorted(lambda f: f.model_id.name == 'product.product')):
            field.unlink()

    def action_delete_fields(self):
        self._remove_fields()
        return self.write(dict(state='draft'))

    def unlink(self):
        self._remove_fields()
        return super(StoredProductAttribute, self).unlink()
