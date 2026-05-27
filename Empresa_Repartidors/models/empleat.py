from odoo import models, fields


class Empleat(models.Model):
    _name = 'repartiment.empleat'
    _description = 'empleado repartidor'
    _order = 'cognom, nom'
    _rec_name = 'nom'

    nom = fields.Char('nom', required=True)
    cognom = fields.Char('cognom', required=True)
    dni = fields.Char('dni', required=True)
    telefon = fields.Char('telefon')
    foto = fields.Image('foto', max_width=200, max_height=200)

    # carnets
    carnet_ciclomotor = fields.Boolean('carnet ciclomotor', default=False)
    carnet_furgoneta = fields.Boolean('carnet furgoneta', default=False)

    # relacion inversa
    repartiment_ids = fields.One2many(
        'repartiment.repartiment', 'empleat_id', string='repartiments'
    )

    _sql_constraints = [
        ('dni_uniq', 'UNIQUE(dni)', 'el dni del empleado debe ser unico'),
    ]
