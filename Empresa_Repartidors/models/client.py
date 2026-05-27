from odoo import models, fields


class Client(models.Model):
    _name = 'repartiment.client'
    _description = 'cliente emisor'
    _order = 'cognom, nom'
    _rec_name = 'nom'

    dni = fields.Char('dni', required=True)
    nom = fields.Char('nom', required=True)
    cognom = fields.Char('cognom')
    telefon = fields.Char('telefon')

    _sql_constraints = [
        ('dni_uniq', 'UNIQUE(dni)', 'el dni del cliente debe ser unico'),
    ]
