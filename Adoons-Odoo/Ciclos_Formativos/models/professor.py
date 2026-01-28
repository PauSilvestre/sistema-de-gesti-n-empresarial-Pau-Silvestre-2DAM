# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Professor(models.Model):
    _name = 'ciclo.professor'
    _description = 'Profesor'
    _rec_name = 'nombre_completo'

    nombre = fields.Char(string='Nombre', required=True)
    apellidos = fields.Char(string='Apellidos', required=True)
    nombre_completo = fields.Char(string='Nombre completo', compute='_compute_nombre_completo', store=True)
    dni = fields.Char(string='DNI')
    email = fields.Char(string='Email')
    telefono = fields.Char(string='Teléfono')
    especialidad = fields.Char(string='Especialidad')
    modul_ids = fields.One2many('ciclo.modul', 'professor_id', string='Módulos que imparte')
    num_moduls = fields.Integer(string='Número de módulos', compute='_compute_num_moduls')

    @api.depends('nombre', 'apellidos')
    def _compute_nombre_completo(self):
        for professor in self:
            professor.nombre_completo = f"{professor.nombre} {professor.apellidos}"

    def _compute_num_moduls(self):
        for professor in self:
            professor.num_moduls = len(professor.modul_ids)

    _sql_constraints = [
        ('dni_uniq', 'UNIQUE (dni)', 'El DNI del profesor debe ser único.')
    ]
