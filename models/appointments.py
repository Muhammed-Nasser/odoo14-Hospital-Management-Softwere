# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HospitalAppointments(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointments Model"
    # order by field desc
    _order = "reference desc"

    note = fields.Text(string='Description', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'cancelled'),
    ], default='draft', string="Status", tracking=True)
    # to test onchange method
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, tracking=True)
    # Many2one Relation
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, tracking=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True, tracking=True)
    reference = fields.Char(string='appointment Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    date_appointment = fields.Date(string="Date", required=True, tracking=True)
    date_check = fields.Datetime(string="Check Up Time")
    # related fields
    age = fields.Integer(string='Age', related='patient_id.age')
    responsible_id = fields.Many2one('res.partner', string="Responsible", tracking=True,
                                     related='patient_id.responsible_id')

    def action_confirm(self):
        for rec in self:
            if rec.state != 'cancel':
                rec.state = 'cancel'
            else:
                print("not allowed")

    def action_done(self):
        for rec in self:
            if rec.state != 'done':
                rec.state = 'done'
            else:
                print("not allowed")

    # override create function
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "New Patient"
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('appointment.no') or _('New')
        return super(HospitalAppointments, self).create(vals)

    # onchange function
    @api.onchange('patient_id', 'note')
    def onchange_patient_id(self):
        if self.patient_id:
            # check if there is a value in patient_id.gender => gender = patient_id.gender
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
            # check if there is a value in patient_id.note => note = patient_id.note
            if self.patient_id.note:
                self.note = self.patient_id.note
        else:
            self.gender = ''
            self.note = ''



