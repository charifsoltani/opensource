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
        """ add stored attribute fields to search view."""
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
        for attribute_custom_field in self.env['product.attribute'].search([('is_stored', '=', True)]):
            if not attribute_custom_field._exists_in_model(self._name):
                continue
            _field = ModelField._get('product.product', attribute_custom_field.technical_name)
            if attribute_custom_field.show_in_filters:
                groupby.addprevious(etree.Element('field', {'name': _field.name, 'domain': _field.domain}))
            if attribute_custom_field.show_in_group_by:
                groupby.append(etree.Element('filter', {'string': _field.field_description, 'context': "{'group_by':'%s'}" % _field.name}))

        result['arch'] = etree.tostring(doc, encoding="unicode").replace('\t', '')
        return result
