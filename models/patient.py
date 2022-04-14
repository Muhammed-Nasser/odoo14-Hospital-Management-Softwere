# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient Model"

    name = fields.Char(string='Name', required=True, tracking=True)
    age = fields.Integer(string='Age')
    # computed field
    appointments_count = fields.Integer(string='Appointments Count', compute='_compute_appointments_count')
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
    # Many2one Relation
    responsible_id = fields.Many2one('res.partner', string="Responsible", tracking=True)
    reference = fields.Char(string='Patient Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))

    # computed method
    def _compute_appointments_count(self):
        # Singleton Error => solve for rec in self:
        for rec in self:
            num = rec.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointments_count = num
            print(rec.env['hospital.appointment'])


    # buttons functions
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
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('patient.no') or _('New')
        return super(HospitalPatient, self).create(vals)



