# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class ListaTareas(models.Model):
    _name = 'lista_tareas.lista'
    _description = 'Modelo de la lista de tareas'
    _rec_name = "tarea"

    tarea = fields.Char(string="Tarea")
    prioridad = fields.Integer(string="Prioridad")
    urgente = fields.Boolean(string="Urgente", compute="_value_urgente", store=True)
    realizada = fields.Boolean(string="Realizada")
    fecha_asignada = fields.Date(string="Fecha asignada")
    data_limit = fields.Date(string="Fecha límite")
    vencidas = fields.Boolean(string="Vencida", compute="_compute_vencidas", store=True)
    usuari_assignat = fields.Many2one('res.users', string='Usuario asignado')
    categoria_id = fields.Many2one('lista_tareas.categoria', string='Categoría')

    @api.depends('prioridad')
    def _value_urgente(self):
        for record in self:
            record.urgente = record.prioridad > 10

    @api.depends('data_limit', 'realizada')
    def _compute_vencidas(self):
        for record in self:
            if record.data_limit and not record.realizada:
                record.vencidas = record.data_limit < date.today()
            else:
                record.vencidas = False
