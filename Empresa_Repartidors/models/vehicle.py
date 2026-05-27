from odoo import models, fields, api


class Vehicle(models.Model):
    _name = 'repartiment.vehicle'
    _description = 'vehiculo de reparto'
    _order = 'matricula'
    _rec_name = 'display_name'

    tipus = fields.Selection([
        ('bicicleta', 'bicicleta'),
        ('ciclomotor', 'ciclomotor'),
        ('furgoneta', 'furgoneta'),
    ], string='tipus', required=True)

    matricula = fields.Char('matricula')
    foto = fields.Image('foto', max_width=200, max_height=200)
    descripcio = fields.Text('descripcio')

    # antes: name_get (deprecado en odoo 17); ahora compute
    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.depends('tipus', 'matricula')
    def _compute_display_name(self):
        for rec in self:
            nom = rec.tipus or ''
            if rec.matricula:
                nom += ' [' + rec.matricula + ']'
            rec.display_name = nom or 'vehicle'
