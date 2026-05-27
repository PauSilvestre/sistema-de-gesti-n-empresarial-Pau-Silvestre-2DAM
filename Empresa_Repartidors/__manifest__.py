{
    'name': 'Empresa Repartidors',
    'version': '1.0',
    'summary': 'gestion de repartos con empleados, vehiculos y clientes',
    'description': 'modulo para gestionar una empresa de repartidores',
    'author': 'Alumne',
    'category': 'Educativo',
    # web: necesario para el report pdf
    'depends': ['base', 'web'],
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
