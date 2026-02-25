# -*- coding: utf-8 -*-
from odoo import models, fields

class LigaPartidoWizard(models.TransientModel):
    _name = 'liga.partido.wizard'
    _description = 'Asistente para crear partidos'

    equipo_casa = fields.Many2one('liga.equipo', string='Equipo local', required=True)
    goles_casa = fields.Integer(string='Goles local', default=0)
    equipo_fuera = fields.Many2one('liga.equipo', string='Equipo visitante', required=True)
    goles_fuera = fields.Integer(string='Goles visitante', default=0)

    def crear_partido(self):
        self.env['liga.partido'].create({
            'equipo_casa': self.equipo_casa.id,
            'goles_casa': self.goles_casa,
            'equipo_fuera': self.equipo_fuera.id,
            'goles_fuera': self.goles_fuera,
        })
