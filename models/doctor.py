# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
    image = fields.Binary(string="Patient Image", copy=0)

    appointments_count = fields.Integer(string='Appointments Count', compute='_compute_appointments_count')

    # buttons functions
    def action_available(self):
        if self.state != 'available':
            self.state = 'available'
        else:
            raise ValidationError(_("Sorry, %s has already available state!" % self.reference))

    def action_busy(self):
        if self.state != 'busy':
            self.state = 'busy'
        else:
            raise ValidationError(_("Sorry, %s has already busy state!" % self.reference))

    # override create function
    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = "No Description"
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('doctor.no') or _('New')
        return super(HospitalDoctor, self).create(vals)

    # override copy(duplicate) method
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        if 'name' not in default:
            default['name'] = _("%s (Copy)") % self.name
            # if you want to erase value (do not copy it )
            # there is two methods => in field you can add this attribute copy="0" look at image or this method
            default['age'] = ""
        return super(HospitalDoctor, self).copy(default=default)

    # computed method
    def _compute_appointments_count(self):
        # Singleton Error => solve for rec in self:
        for rec in self:
            num = rec.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
            rec.appointments_count = num
            print(rec.env['hospital.appointment'])

    # action to smart bottom appointments
    def action_open_appointment(self):
        action = self.env['ir.actions.actions']._for_xml_id('om_hospital.appointments_action')
        # condition
        action['domain'] = [('doctor_id', '=', self.id)]
        return action









