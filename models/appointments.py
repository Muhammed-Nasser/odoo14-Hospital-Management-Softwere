# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HospitalAppointments(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointments Model"

    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'cancelled'),
    ], default='draft', string="Status", tracking=True)
    # Many2one Relation
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, tracking=True)
    reference = fields.Char(string='appointment Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    date_appointment = fields.Date(string="Date")
    date_check = fields.Datetime(string="Check Up Time")
    age = fields.Integer(string='Age', related='patient_id.age')
    responsible_id = fields.Many2one('res.partner', string="Responsible", tracking=True,
                                     related='patient_id.responsible_id')

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
            vals['reference'] = self.env['ir.sequence'].next_by_code('appointment.no') or _('New')
        return super(HospitalAppointments, self).create(vals)



