from odoo import fields, models, _, api


class CreateAppointmentWizard(models.TransientModel):
    _name = 'create.appointment.wizard'
    _description = 'Create Appointment Wizard'

    date_appointment = fields.Date(string="Date", required=True, tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient")


    # method to create appointment from wizard form
    def action_create_appointment(self):
        vals = {
            'date_appointment': self.date_appointment,
            'patient_id': self.patient_id.id,
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)

        # return view form of this new record
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
        }

    # Return Action and View From
    def action_view_appointments(self):
        action = self.env['ir.actions.actions']._for_xml_id('om_hospital.appointments_action')
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

    def action_get_test(self):
        active_model = self.env.context.get('active_model')
        vals = {
            'date_appointment': self.date_appointment,
            'patient_id': self.env[active_model].browse(self.env.context.get('active_id')).id,
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)

        # return view form of this new record
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
        }





