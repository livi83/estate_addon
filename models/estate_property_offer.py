from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "price desc"  # Order by price in descending order
    
    price = fields.Float(string='Price')
    status = fields.Selection([
        ('waiting', 'Waiting'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', default='waiting')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True, ondelete='cascade')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True, string="Property Type")
    
    def action_accept(self):
        """Accept the offer."""
        if self.property_id.status == 'sold':
            raise UserError("Cannot accept offers for sold properties.")
        if self.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted'):
            raise UserError("Only one offer can be accepted for this property.")
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.status = 'offer_accepted'

    def action_refuse(self):
        """Refuse the offer."""
        if self.status == 'accepted':
            raise UserError("Cannot refuse an accepted offer.")
        self.status = 'refused'
        
    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        if property_id:
            property_record = self.env['estate.property'].browse(property_id)
            # Check if there are existing offers for this property
            existing_offers = property_record.offer_ids
            if existing_offers:
                # Raise an error if the new offer is lower than existing offers
                max_offer = max(existing_offers.mapped('price'))
                if vals.get('price', 0.0) < max_offer:
                    raise exceptions.UserError(f"The offer must be greater than the current maximum offer of {max_offer}.")

            # Set the property state to 'Offer Received'
            property_record.status = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals)