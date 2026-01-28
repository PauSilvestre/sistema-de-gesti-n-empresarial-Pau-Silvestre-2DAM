# -*- coding: utf-8 -*-

from odoo import models, fields

class ListaTareasCategoria(models.Model):
    _name = 'lista_tareas.categoria'
    _description = 'Categoría de tareas'

    nombre = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
    tarea_ids = fields.One2many('lista_tareas.lista', 'categoria_id', string='Tareas en esta categoría')
