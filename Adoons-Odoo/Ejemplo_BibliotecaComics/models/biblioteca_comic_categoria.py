# -*- coding: utf-8 -*-

from odoo import models, fields

class BibliotecaComicCategoria(models.Model):
    _name = 'biblioteca.comic.categoria'
    _description = 'Categoría de cómics'

    nombre = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
    comic_ids = fields.One2many('biblioteca.comic', 'categoria_id', string='Cómics en esta categoría')
