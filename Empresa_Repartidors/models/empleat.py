# -*- coding: utf-8 -*-
# model empleat: guarda dades dels repartidors (nom, dni, carnet, foto...)
# un empleat te molts repartiments
from odoo import models, fields

class Empleat(models.Model):
    _name = 'repartiment.empleat'
    _description = 'empleat repartidor'
    _order = 'cognom, nom'
    _rec_name = 'nom'

    # dades personals de l'empleat
    nom = fields.Char('nom', required=True)
    cognom = fields.Char('cognom', required=True)
    dni = fields.Char('dni', required=True)
    telefon = fields.Char('telefon')
    foto = fields.Image('foto', max_width=200, max_height=200)

    # carnets que te l'empleat
    carnet_ciclomotor = fields.Boolean('carnet ciclomotor', default=False)
    carnet_furgoneta = fields.Boolean('carnet furgoneta', default=False)

    # relacio one2many: un empleat pot tindre molts repartiments
    # camp invers: empleat_id del model repartiment.repartiment
    repartiment_ids = fields.One2many(
        'repartiment.repartiment', 'empleat_id', string='repartiments'
    )

    # constraint sql: el dni ha de ser unic
    _sql_constraints = [
        ('dni_uniq', 'UNIQUE(dni)', 'el dni de l\'empleat ha de ser unic'),
    ]
