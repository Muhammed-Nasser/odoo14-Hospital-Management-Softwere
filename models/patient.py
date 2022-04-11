# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient Model"

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True)
    note = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'cancelled'),
    ], default='draft', string="Status")

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


