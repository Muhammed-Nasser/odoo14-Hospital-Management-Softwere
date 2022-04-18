# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
import re

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient Model"
    # order depends on multiple fields
    _order = "name,age desc"

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
    # one2many Relation
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    reference = fields.Char(string='Patient Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    image = fields.Binary(string="Patient Image")
    email = fields.Char(string="Email", required=True)

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
            raise ValidationError(_("Sorry, %s has already cancel state!" % self.reference))

    def action_done(self):
        if self.state != 'done':
            self.state = 'done'
        else:
            raise ValidationError(_("Sorry, %s has already done state!" % self.reference))

    # override create function
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "New Patient"
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('patient.no') or _('New')
        return super(HospitalPatient, self).create(vals)

    # override default value function => called when we add default='value' attr.
    # when we override it we can add all default values in it
    @api.model
    def default_get(self, fields):
        vals = super(HospitalPatient, self).default_get(fields)
        vals['gender'] = 'female'
        return vals

    # override delete function
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("Sorry, You can not delete %s that has a DONE status!" % self.reference))
        return super(HospitalPatient, self).unlink()

    # add constrains to field
    @api.constrains('email')
    def check_email_value(self):
        for rec in self:
            # unique
            patient = self.env['hospital.patient'].search([('email', '=', rec.email), ('id', '!=', rec.id)])
            # match email format
            if not re.match('(\w+[.|\w])*@(\w+[.])*\w+', self.email):
                raise UserError("Email not valid.")
            if patient:
                raise UserError("Email already exist.")

    # override name get method _rec_name
    def name_get(self):
        result = []
        for account in self:
            name = '[' + account.reference + '] ' + account.name
            result.append((account.id, name))
        return result


