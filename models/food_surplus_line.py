from odoo import models, fields


class FoodSurplusLine(models.Model):
    _name = 'food.surplus.line'
    _description = 'Surplus Food Line Item'

    listing_id = fields.Many2one('food.surplus.listing', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Food Item')
    meal_count = fields.Integer(string='Meals')
    weight_kg = fields.Float(string='Weight (kg)')
