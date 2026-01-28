# -*- coding: utf-8 -*-
{
    'name': "Ciclos Formativos",
    'summary': "Gestión de ciclos formativos de un instituto",
    'description': """
        Módulo para gestionar:
        - Ciclos formativos
        - Módulos educativos
        - Alumnos matriculados
        - Profesores
    """,
    'author': "Tu Nombre",
    'website': "https://tusitio.com",
    'category': 'Education',
    'version': '0.1',
    'application': True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/ciclo_formativo.xml',
        'views/modul.xml',
        'views/alumne.xml',
        'views/professor.xml',
    ],
}
