# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BibliotecaComicEjemplar(models.Model):
    _name = 'biblioteca.comic.ejemplar'
    _description = 'Ejemplar de cómic para préstamo'
    _rec_name = 'codigo'

    codigo = fields.Char(string='Código de ejemplar', required=True)
    comic_id = fields.Many2one('biblioteca.comic', string='Cómic', required=True)
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('mantenimiento', 'En mantenimiento')
    ], string='Estado', default='disponible')
    socio_id = fields.Many2one('biblioteca.socio', string='Prestado a')
    fecha_prestamo = fields.Date(string='Fecha de préstamo')
    fecha_devolucion_prevista = fields.Date(string='Fecha prevista de devolución')
    comic_nombre = fields.Char(related='comic_id.nombre', string='Título del cómic', store=True)
    comic_categoria = fields.Many2one(related='comic_id.categoria_id', string='Categoría', store=True)

    @api.constrains('fecha_prestamo')
    def _check_fecha_prestamo(self):
        for ejemplar in self:
            if ejemplar.fecha_prestamo and ejemplar.fecha_prestamo > date.today():
                raise ValidationError('La fecha de préstamo no puede ser posterior al día de hoy.')

    @api.constrains('fecha_devolucion_prevista')
    def _check_fecha_devolucion(self):
        for ejemplar in self:
            if ejemplar.fecha_devolucion_prevista and ejemplar.fecha_devolucion_prevista < date.today():
                raise ValidationError('La fecha prevista de devolución no puede ser anterior al día de hoy.')

    @api.onchange('socio_id')
    def _onchange_socio_id(self):
        if self.socio_id:
            self.estado = 'prestado'
            if not self.fecha_prestamo:
                self.fecha_prestamo = date.today()
        else:
            self.estado = 'disponible'
            self.fecha_prestamo = False
            self.fecha_devolucion_prevista = False

    _sql_constraints = [
        ('codigo_uniq', 'UNIQUE (codigo)', 'El código del ejemplar debe ser único.')
    ]
