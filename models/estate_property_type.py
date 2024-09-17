from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(required=True, string='Name')

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing_tag = self.search([
                ('name', '=', record.name),
                ('id', '!=', record.id)  # Exclude current record from the search
            ])
            if existing_tag:
                raise ValidationError("The property type must be unique.")