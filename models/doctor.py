# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Doctor Model"

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age')

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, tracking=True)
    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('not_available', 'Not Available'),

    ], default='not_available', string="Status", tracking=True)

    reference = fields.Char(string='Doctor Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    image = fields.Binary(string="Patient Image")

    # buttons functions
    def action_available(self):
        if self.state != 'available':
            self.state = 'available'
        else:
            print("not allowed")

    def action_busy(self):
        if self.state != 'busy':
            self.state = 'busy'
        else:
            print("not allowed")

    # override create function
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "No Description"
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('doctor.no') or _('New')
        return super(HospitalDoctor, self).create(vals)






