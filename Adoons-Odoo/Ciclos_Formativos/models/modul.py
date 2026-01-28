# -*- coding: utf-8 -*-

from odoo import models, fields

class Modul(models.Model):
    _name = 'ciclo.modul'
    _description = 'Módulo Educativo'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Nombre del Módulo', required=True)
    codigo = fields.Char(string='Código')
    horas = fields.Integer(string='Horas')
    curso = fields.Selection([('1', 'Primer curso'), ('2', 'Segundo curso')], string='Curso')
    ciclo_id = fields.Many2one('ciclo.formativo', string='Ciclo Formativo', required=True)
    professor_id = fields.Many2one('ciclo.professor', string='Profesor')
    alumne_ids = fields.Many2many('ciclo.alumne', 'modul_alumne_rel', 'modul_id', 'alumne_id', string='Alumnos matriculados')
    num_alumnes = fields.Integer(string='Número de alumnos', compute='_compute_num_alumnes')
    descripcion = fields.Text(string='Descripción')

    def _compute_num_alumnes(self):
        for modul in self:
            modul.num_alumnes = len(modul.alumne_ids)
