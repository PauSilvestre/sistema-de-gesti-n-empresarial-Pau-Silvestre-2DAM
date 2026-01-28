# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Alumne(models.Model):
    _name = 'ciclo.alumne'
    _description = 'Alumno'
    _rec_name = 'nombre_completo'

    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    nombre_completo = fields.Char(string='Nombre completo', compute='_compute_nombre_completo', store=True)
    dni = fields.Char(string='DNI')
    email = fields.Char(string='Email')
    telefono = fields.Char(string='Teléfono')
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
    modul_ids = fields.Many2many('ciclo.modul', 'modul_alumne_rel', 'alumne_id', 'modul_id', string='Módulos matriculados')
    num_moduls = fields.Integer(string='Número de módulos', compute='_compute_num_moduls')

    @api.depends('nombre', 'apellidos')
    def _compute_nombre_completo(self):
        for alumne in self:
            alumne.nombre_completo = f"{alumne.nombre} {alumne.apellidos}"

    def _compute_num_moduls(self):
        for alumne in self:
            alumne.num_moduls = len(alumne.modul_ids)

    _sql_constraints = [
        ('dni_uniq', 'UNIQUE (dni)', 'El DNI del alumno debe ser único.')
    ]
