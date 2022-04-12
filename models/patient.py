# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient Model"

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, tracking=True)
    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'cancelled'),
    ], default='draft', string="Status", tracking=True)
    responsible_id = fields.Many2one('res.partner', string="Responsible", tracking=True)

    def action_confirm(self):
        if self.state != 'cancel':
            self.state = 'cancel'
        else:
            print("not allowed")

    def action_done(self):
        if self.state != 'done':
            self.state = 'done'
        else:
            print("not allowed")

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "New Patient"
        return super(HospitalPatient, self).create(vals)



