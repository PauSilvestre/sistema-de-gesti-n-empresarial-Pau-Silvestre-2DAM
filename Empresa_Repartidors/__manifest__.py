# -*- coding: utf-8 -*-
{
    'name': 'Empresa Repartidors',
    'version': '1.0',
    'summary': 'gestio de repartiments amb empleats, vehicles i clients',
    'description': 'modul per gestionar una empresa de repartidors amb control de carnets, vehicles i estat dels enviaments',
    'author': 'Alumne',
    'category': 'Educativo',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/empleat.xml',
        'views/vehicle.xml',
        'views/client.xml',
        'views/repartiment.xml',
        'wizard/repartiment_wizard.xml',
        'report/repartiment_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
