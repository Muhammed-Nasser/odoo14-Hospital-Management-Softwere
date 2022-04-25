from odoo import fields, models, _, api


class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = 'Appointments Report Wizard'

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    date_from = fields.Date(string="From")
    date_to = fields.Date(string="To")

    def action_appointment_report(self):
        domain = []
        patient_id = self.patient_id
        if patient_id:
            domain += [('patient_id', '=', patient_id.id)]

        date_from = self.date_from
        if date_from:
            domain += [('date_appointment', '>=', date_from)]

        date_to = self.date_to
        if date_to:
            domain += [('date_appointment', '<=', date_to)]

        print (domain)
        appointments = self.env['hospital.appointment'].search_read(domain)
        data = {
            'form_data': self.read()[0],
            'appointments': appointments
        }
        print(self.read()[0])
        return self.env.ref('om_hospital.action_report_patient_appointments').report_action(self, data=data)

