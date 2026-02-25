# -*- coding: utf-8 -*-
{
    'name': 'Ejemplo_LigaFutbol',
    'version': '1.0',
    'summary': 'Gestión de liga de fútbol con equipos, partidos y clasificación.',
    'description': 'Módulo de liga de fútbol',
    'author': 'Sergi',
    'website': 'https://apuntesfpinformatica.es',
    'category': 'Educativo',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/liga_equipo.xml',
        'views/liga_partido.xml',
        'views/liga_equipo_clasificacion.xml',
        'wizard/liga_equipo_wizard.xml',
        'wizard/liga_partido_wizard.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
}
