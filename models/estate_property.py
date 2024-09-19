from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError, ValidationError
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"  # Order by ID in descending order
    
    # Set the 'name' and 'expected_price' fields as required (not nullable in the database)
    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", required=False)
    
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
    
    # Property tags
    tag_ids = fields.Many2many('estate.property.tag', 
                               'estate_property_tag_rel', 
                               'property_id', 
                               'tag_id', 
                               string='Tags'
                               )
    # Offers 
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    # Total area
    total_area = fields.Float(string='Total Area', compute='_compute_total_area', store=True)

    # Best price

    best_price = fields.Float(string='Best Offer', compute='_compute_best_price', store=True)

    status = fields.Selection([
        ('new', 'New'),
        ('available', 'Available'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], string='Status', default='new')
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.constrains('expected_price', 'selling_price', 'bedrooms', 'living_area', 'facades', 'garden_area', 'best_price')
    def _check_positive_values(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("Expected Price must be strictly positive.")
            if record.selling_price and record.selling_price <= 0:
                raise ValidationError("Selling Price must be strictly positive.")
            if record.bedrooms and record.bedrooms <= 0:
                raise ValidationError("Bedrooms must be strictly positive.")
            if record.living_area and record.living_area <= 0:
                raise ValidationError("Living Area must be strictly positive.")
            if record.facades and record.facades <= 0:
                raise ValidationError("Facades must be strictly positive.")
            if record.garden_area and record.garden_area <= 0:
                raise ValidationError("Garden Area must be strictly positive.")
            if record.best_price and record.best_price <= 0:
                raise ValidationError("Best Offer must be strictly positive.")
            
    def action_cancel(self):
        """Cancel the property."""
        if self.status == 'sold':
            raise UserError("Sold properties cannot be canceled.")
        self.status = 'canceled'

    def action_sold(self):
        """Mark the property as sold."""
        if self.status == 'canceled':
            raise UserError("Canceled properties cannot be sold.")
        if not self.offer_ids.filtered(lambda offer: offer.status == 'accepted'):
            raise UserError("You need to accept an offer before selling the property.")
        self.status = 'sold'

    @api.model
    def unlink(self):
        for record in self:
            if record.status not in ['new', 'canceled']:
                raise exceptions.UserError("You cannot delete a property that is not in 'New' or 'Canceled' state.")
        return super(EstateProperty, self).unlink()