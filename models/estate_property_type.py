from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = "sequence, name"  # Order by sequence and then name
    
    name = fields.Char(required=True, string='Name')
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer(string="Sequence", default=10, help="Sequence for manual ordering")
    
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing_tag = self.search([
                ('name', '=', record.name),
                ('id', '!=', record.id)  # Exclude current record from the search
            ])
            if existing_tag:
                raise ValidationError("The property type must be unique.")