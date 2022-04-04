# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient Model"

    name = fields.Char(string='Name', required=True)
    age = fields.Integer (string='Age')
    gender = fields.Selection([
        ('other', 'Male'),
        ('male', 'Female'),
        ('female', 'Other'),
    ], required=True, default='other')
    note = fields.Text(string='Description')
