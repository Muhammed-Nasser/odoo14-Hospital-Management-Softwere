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
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/patient.xml',
    ],
    'demo': [],
    'qweb': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
