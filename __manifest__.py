# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hospital Management Software',
    'version': '1.0',
    'author': 'Muhammad Nasser',
    'summary': 'Hospital Management Software',
    'sequence': 10,
    'description': """ Hospital Management Software """,
    'category': 'Productivity',
    'depends': ['sale',
                'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/patient_all.xml',
        'views/patient_kids.xml',
        'views/appointment_view.xml',
        'views/sale.xml',
    ],
    'demo': [],
    'qweb': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
