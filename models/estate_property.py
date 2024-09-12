from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    # Set the 'name' and 'expected_price' fields as required (not nullable in the database)
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    
    # Required field
    expected_price = fields.Float(string='Expected Price', required=True, default=0.0)

    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )

    # Default fields for tracking creation and updates
    create_uid = fields.Many2one('res.users', string="Created by", readonly=True)
    create_date = fields.Datetime(string="Created on", readonly=True)
    write_uid = fields.Many2one('res.users', string="Last Updated by", readonly=True)
    write_date = fields.Datetime(string="Last Updated on", readonly=True)

    # Relation to property type
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
  
    # Buyer field
    buyer_id = fields.Many2one('res.partner', string='Buyer')

    # Salesperson field
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)