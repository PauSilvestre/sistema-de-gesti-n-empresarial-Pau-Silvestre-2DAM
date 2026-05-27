# -*- coding: utf-8 -*-
# model vehicle: guarda dades dels vehicles de l'empresa
# tipus: bicicleta, ciclomotor o furgoneta
from odoo import models, fields

class Vehicle(models.Model):
    _name = 'repartiment.vehicle'
    _description = 'vehicle de repartiment'
    _order = 'matricula'
    _rec_name = 'tipus'

    # tipus de vehicle amb seleccio
    tipus = fields.Selection([
        ('bicicleta', 'bicicleta'),
        ('ciclomotor', 'ciclomotor'),
        ('furgoneta', 'furgoneta'),
    ], string='tipus', required=True)

    matricula = fields.Char('matricula')
    foto = fields.Image('foto', max_width=200, max_height=200)
    descripcio = fields.Text('descripció')

    # nom que es mostra al seleccionar el vehicle
    def name_get(self):
        result = []
        for rec in self:
            # mostra tipus + matricula si en te
            nom = rec.tipus or ''
            if rec.matricula:
                nom += ' [' + rec.matricula + ']'
            result.append((rec.id, nom))
        return result
