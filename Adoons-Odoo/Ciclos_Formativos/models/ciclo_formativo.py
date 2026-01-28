# -*- coding: utf-8 -*-

from odoo import models, fields

class CicloFormativo(models.Model):
    _name = 'ciclo.formativo'
    _description = 'Ciclo Formativo'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre del Ciclo', required=True)
    codigo = fields.Char(string='Código')
    nivel = fields.Selection([
        ('grado_medio', 'Grado Medio'),
        ('grado_superior', 'Grado Superior')
    ], string='Nivel', default='grado_medio')
    duracion = fields.Integer(string='Duración (horas)')
    descripcion = fields.Text(string='Descripción')
    modul_ids = fields.One2many('ciclo.modul', 'ciclo_id', string='Módulos del ciclo')
    num_moduls = fields.Integer(string='Número de módulos', compute='_compute_num_moduls')

    def _compute_num_moduls(self):
        for ciclo in self:
            ciclo.num_moduls = len(ciclo.modul_ids)
