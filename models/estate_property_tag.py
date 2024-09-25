from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"  # Order by name in ascending order
    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color")

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing_tag = self.search([
                ('name', '=', record.name),
                ('id', '!=', record.id)  # Exclude current record from the search
            ])
            if existing_tag:
                raise ValidationError("The tag name must be unique.")
    
   