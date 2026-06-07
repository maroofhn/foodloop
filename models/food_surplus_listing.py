from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class FoodSurplusListing(models.Model):
    _name = 'food.surplus.listing'
    _description = 'Surplus Food Listing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, available_from asc'

    name = fields.Char(string='Listing Title', required=True)
    # auto reference like FL/0001 so it looks tidy
    reference = fields.Char(string='Reference', readonly=True, copy=False, default='New')
    donor_id = fields.Many2one('res.partner', string='Donor', required=True)
    charity_id = fields.Many2one('res.partner', string='Charity', tracking=True)
    driver_id = fields.Many2one('res.partner', string='Driver', tracking=True)
    available_from = fields.Date(string='Available From', default=fields.Date.context_today)
    best_before = fields.Date(string='Best Before')
    notes = fields.Text(string='Notes')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Urgent'),
    ], string='Priority', default='0')
    state = fields.Selection([
        ('listed', 'Listed'),
        ('claimed', 'Claimed'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('closed', 'Closed'),
    ], default='listed', tracking=True, group_expand='_expand_states')
    # color is used by the kanban so each stage looks different
    color = fields.Integer(string='Color', compute='_compute_color')
    is_expiring = fields.Boolean(string='Expiring Soon', compute='_compute_is_expiring', store=True)
    line_ids = fields.One2many('food.surplus.line', 'listing_id', string='Items')
    total_meals = fields.Integer(string='Total Meals', compute='_compute_totals', store=True)
    total_kg = fields.Float(string='Total Weight (kg)', compute='_compute_totals', store=True)
    co2_saved_kg = fields.Float(string='CO2 Saved (kg)', compute='_compute_totals', store=True)

    @api.depends('line_ids', 'line_ids.meal_count', 'line_ids.weight_kg')
    def _compute_totals(self):
        for rec in self:
            rec.total_meals = sum(rec.line_ids.mapped('meal_count'))
            rec.total_kg = sum(rec.line_ids.mapped('weight_kg'))
            # 2.5 kg of CO2 saved per kg of food rescued (industry average)
            rec.co2_saved_kg = rec.total_kg * 2.5

    @api.model
    def _expand_states(self, states, domain):
        # keep the kanban columns in workflow order, not alphabetical
        return [key for key, _label in self._fields['state'].selection]

    @api.depends('state')
    def _compute_color(self):
        # one color per stage so the board reads at a glance
        colors = {
            'listed': 4,
            'claimed': 3,
            'picked_up': 2,
            'delivered': 10,
            'closed': 0,
        }
        for rec in self:
            rec.color = colors.get(rec.state, 0)

    @api.depends('best_before')
    def _compute_is_expiring(self):
        # flag anything that is past or due today so it stands out
        for rec in self:
            rec.is_expiring = bool(rec.best_before and rec.best_before <= date.today())

    @api.model_create_multi
    def create(self, vals_list):
        # give each new listing a reference number
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('food.surplus.listing') or 'New'
        return super().create(vals_list)

    def action_claim(self):
        # a charity must be set before it can be claimed
        if not self.charity_id:
            raise UserError("Please select a charity before claiming.")
        self.state = 'claimed'

    def action_pick_up(self):
        # a driver must be set before pickup
        if not self.driver_id:
            raise UserError("Please assign a driver before picking up.")
        self.state = 'picked_up'

    def action_deliver(self):
        self.state = 'delivered'

    def action_close(self):
        self.state = 'closed'

    def action_reset(self):
        # safety net to send a listing back to the start
        self.state = 'listed'
