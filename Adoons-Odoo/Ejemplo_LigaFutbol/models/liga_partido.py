# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LigaPartido(models.Model):
    _name = 'liga.partido'
    _description = 'Un partido de la liga'

    equipo_casa = fields.Many2one('liga.equipo', string='Equipo local')
    goles_casa = fields.Integer()
    equipo_fuera = fields.Many2one('liga.equipo', string='Equipo visitante')
    goles_fuera = fields.Integer()

    @api.constrains('equipo_casa')
    def _check_equipo_local(self):
        for record in self:
            if not record.equipo_casa:
                raise ValidationError('Debe seleccionarse un equipo local.')
            if record.equipo_casa == record.equipo_fuera:
                raise ValidationError('Los equipos deben ser diferentes.')

    @api.constrains('equipo_fuera')
    def _check_equipo_visitante(self):
        for record in self:
            if not record.equipo_fuera:
                raise ValidationError('Debe seleccionarse un equipo visitante.')
            if record.equipo_casa == record.equipo_fuera:
                raise ValidationError('Los equipos deben ser diferentes.')

    # recalcula la clasificacion de todos los equipos
    def actualizoRegistrosEquipo(self):
        for equipo in self.env['liga.equipo'].search([]):
            equipo.victorias = equipo.empates = equipo.derrotas = 0
            equipo.goles_a_favor = equipo.goles_en_contra = 0
            equipo.puntos = 0

            for partido in self.env['liga.partido'].search([]):
                diferencia = abs(partido.goles_casa - partido.goles_fuera)
                
                if partido.equipo_casa == equipo:
                    equipo.goles_a_favor += partido.goles_casa
                    equipo.goles_en_contra += partido.goles_fuera
                    if partido.goles_casa > partido.goles_fuera:
                        equipo.victorias += 1
                        # victoria por 4 o mas goles da 4 puntos
                        if diferencia >= 4:
                            equipo.puntos += 4
                        else:
                            equipo.puntos += 3
                    elif partido.goles_casa < partido.goles_fuera:
                        equipo.derrotas += 1
                        # derrota por 4 o mas goles resta 1 punto
                        if diferencia >= 4:
                            equipo.puntos -= 1
                    else:
                        equipo.empates += 1
                        equipo.puntos += 1

                if partido.equipo_fuera == equipo:
                    equipo.goles_a_favor += partido.goles_fuera
                    equipo.goles_en_contra += partido.goles_casa
                    if partido.goles_fuera > partido.goles_casa:
                        equipo.victorias += 1
                        if diferencia >= 4:
                            equipo.puntos += 4
                        else:
                            equipo.puntos += 3
                    elif partido.goles_fuera < partido.goles_casa:
                        equipo.derrotas += 1
                        if diferencia >= 4:
                            equipo.puntos -= 1
                    else:
                        equipo.empates += 1
                        equipo.puntos += 1

    @api.onchange('equipo_casa', 'goles_casa', 'equipo_fuera', 'goles_fuera')
    def actualizar(self):
        self.actualizoRegistrosEquipo()

    @api.model
    def create(self, values):
        record = super().create(values)
        self.actualizoRegistrosEquipo()
        return record

    def unlink(self):
        res = super().unlink()
        self.actualizoRegistrosEquipo()
        return res

    # + 2 goles a todos los equipos de casa
    def sumar_goles_casa(self):
        partidos = self.env['liga.partido'].search([])
        for partido in partidos:
            partido.goles_casa += 2
        self.actualizoRegistrosEquipo()

    # + 2 goles a todos los equipos visitantes
    def sumar_goles_fuera(self):
        partidos = self.env['liga.partido'].search([])
        for partido in partidos:
            partido.goles_fuera += 2
        self.actualizoRegistrosEquipo()
