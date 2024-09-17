from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', default='refused')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True, ondelete='cascade')

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
