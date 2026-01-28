# -*- coding: utf-8 -*-

from datetime import timedelta, date
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Modelo abstracto de archivo (archivable)'

    activo = fields.Boolean(default=True)

    def archivar(self):
        for record in self:
            record.activo = not record.activo

class BibliotecaComic(models.Model):
    _name = 'biblioteca.comic'
    _description = 'Cómic de la biblioteca'
    _inherit = ['base.archive']
    _order = 'fecha_publicacion desc, nombre'
    _rec_name = 'nombre'

    nombre = fields.Char(string='Título', required=True, index=True)
    estado = fields.Selection([
        ('borrador', 'No disponible'),
        ('disponible', 'Disponible'),
        ('perdido', 'Perdido')
    ], string='Estado', default='borrador')
    descripcion = fields.Html(string='Descripción', sanitize=True, strip_style=False)
    portada = fields.Binary(string='Portada del cómic')
    fecha_publicacion = fields.Date(string='Fecha de publicación')
    precio = fields.Float(string='Precio')
    paginas = fields.Integer(string='Número de páginas', groups='base.group_user')
    valoracion_lector = fields.Float(string='Valoración media lectores', digits=(14, 4))

    autor_ids = fields.Many2many('res.partner', string='Autores')
    editorial_id = fields.Many2one('res.partner', string='Editorial')
    categoria_id = fields.Many2one('biblioteca.comic.categoria', string='Categoría')

    data_limit = fields.Date(string='Fecha límite')
    vencidas = fields.Boolean(string='Vencido', compute='_compute_vencidas', store=True)
    usuari_assignat = fields.Many2one('res.users', string='Usuario asignado')

    dias_lanzamiento = fields.Integer(string='Días desde lanzamiento',
        compute='_compute_dias_lanzamiento', inverse='_inverse_dias_lanzamiento',
        search='_search_dias_lanzamiento', store=False)

    ref_doc_id = fields.Reference(selection='_referencable_models', string='Referencia a documento')

    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([('field_id.name', '=', 'message_ids')])
        return [(x.model, x.name) for x in models]

    @api.depends('fecha_publicacion')
    def _compute_dias_lanzamiento(self):
        hoy = fields.Date.today()
        for comic in self:
            if comic.fecha_publicacion:
                delta = hoy - comic.fecha_publicacion
                comic.dias_lanzamiento = delta.days
            else:
                comic.dias_lanzamiento = 0

    @api.depends('data_limit', 'estado')
    def _compute_vencidas(self):
        for comic in self:
            if comic.data_limit and comic.estado != 'disponible':
                comic.vencidas = comic.data_limit < date.today()
            else:
                comic.vencidas = False

    def _inverse_dias_lanzamiento(self):
        hoy = fields.Date.today()
        for comic in self:
            if comic.dias_lanzamiento is not None:
                nueva_fecha = hoy - timedelta(days=comic.dias_lanzamiento)
                comic.fecha_publicacion = nueva_fecha

    def _search_dias_lanzamiento(self, operator, value):
        hoy = fields.Date.today()
        fecha_limite = hoy - timedelta(days=value)
        operator_map = {'>': '<', '>=': '<=', '<': '>', '<=': '>='}
        new_op = operator_map.get(operator, operator)
        return [('fecha_publicacion', new_op, fecha_limite)]

    def name_get(self):
        result = []
        for record in self:
            nombre = "%s (%s)" % (record.nombre, record.fecha_publicacion or 'Sin fecha')
            result.append((record.id, nombre))
        return result

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (nombre)', 'El título del cómic debe ser único.'),
        ('positive_page', 'CHECK(paginas>0)', 'El cómic debe tener al menos una página.')
    ]

    @api.constrains('fecha_publicacion')
    def _check_release_date(self):
        for record in self:
            if record.fecha_publicacion and record.fecha_publicacion > fields.Date.today():
                raise ValidationError('La fecha de publicación no puede ser en el futuro.')
