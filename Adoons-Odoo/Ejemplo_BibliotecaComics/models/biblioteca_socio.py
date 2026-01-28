# -*- coding: utf-8 -*-

from odoo import models, fields, api

class BibliotecaSocio(models.Model):
    _name = 'biblioteca.socio'
    _description = 'Socio de la biblioteca'
    _rec_name = 'nombre_completo'

    nombre = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    identificador = fields.Char(string='Identificador', required=True)
    nombre_completo = fields.Char(string='Nombre completo', compute='_compute_nombre_completo', store=True)
    ejemplar_ids = fields.One2many('biblioteca.comic.ejemplar', 'socio_id', string='Ejemplares prestados')

    @api.depends('nombre', 'apellido')
    def _compute_nombre_completo(self):
        for socio in self:
            socio.nombre_completo = f"{socio.nombre} {socio.apellido}"

    _sql_constraints = [
        ('identificador_uniq', 'UNIQUE (identificador)', 'El identificador del socio debe ser único.')
    ]
