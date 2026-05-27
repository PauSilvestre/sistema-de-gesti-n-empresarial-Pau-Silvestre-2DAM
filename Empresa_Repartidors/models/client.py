# -*- coding: utf-8 -*-
# model client: guarda dades dels clients que envien paquets
from odoo import models, fields

class Client(models.Model):
    _name = 'repartiment.client'
    _description = 'client emissor'
    _order = 'cognom, nom'
    _rec_name = 'nom'

    # dades del client
    dni = fields.Char('dni', required=True)
    nom = fields.Char('nom', required=True)
    cognom = fields.Char('cognom')
    telefon = fields.Char('telefon')

    # constraint sql: el dni ha de ser unic
    _sql_constraints = [
        ('dni_uniq', 'UNIQUE(dni)', 'el dni del client ha de ser unic'),
    ]
