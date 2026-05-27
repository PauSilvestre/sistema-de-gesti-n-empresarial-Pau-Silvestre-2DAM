from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Repartiment(models.Model):
    _name = 'repartiment.repartiment'
    _description = 'reparto / envio'
    # orden por fecha y urgencia
    _order = 'data_recepcio, urgencia'

    # codigo via ir.sequence
    codi = fields.Char('codi', readonly=True, copy=False, default='nou')

    # fechas
    data_inici = fields.Datetime('data inici')
    data_retorn = fields.Datetime('data retorn')
    data_recepcio = fields.Date('data recepcio')

    # many2one
    empleat_id = fields.Many2one('repartiment.empleat', string='repartidor', required=True)
    vehicle_id = fields.Many2one('repartiment.vehicle', string='vehicle', required=True)
    client_id = fields.Many2one('repartiment.client', string='client emissor', required=True)

    # paquete
    kilometres = fields.Float('kilometres')
    pes = fields.Float('pes (kg)')
    volum = fields.Float('volum (m3)')
    observacions = fields.Text('observacions')

    # receptor
    receptor_nom = fields.Char('nom receptor')
    receptor_telefon = fields.Char('telefon receptor')
    receptor_adreca = fields.Char('adreca receptor')

    estat = fields.Selection([
        ('no_ha_eixit', 'no ha eixit'),
        ('de_cami', 'de cami'),
        ('entregada', 'entregada'),
    ], string='estat', default='no_ha_eixit', required=True)

    # 1 = mas urgente
    urgencia = fields.Selection([
        ('1', 'organs humans'),
        ('2', 'aliments refrigerats'),
        ('3', 'aliments'),
        ('4', 'alta prioritat'),
        ('5', 'baixa prioritat'),
    ], string='urgencia', default='5', required=True)

    @api.model
    def create(self, vals):
        if vals.get('codi', 'nou') == 'nou':
            vals['codi'] = self.env['ir.sequence'].next_by_code('repartiment.repartiment') or 'nou'
        return super().create(vals)

    # carnet segun vehiculo
    @api.constrains('empleat_id', 'vehicle_id')
    def _check_carnet(self):
        for rec in self:
            if rec.vehicle_id.tipus == 'ciclomotor' and not rec.empleat_id.carnet_ciclomotor:
                raise ValidationError("el empleado no tiene carnet de ciclomotor")
            if rec.vehicle_id.tipus == 'furgoneta' and not rec.empleat_id.carnet_furgoneta:
                raise ValidationError("el empleado no tiene carnet de furgoneta")

    # no doble viaje activo
    @api.constrains('empleat_id', 'vehicle_id', 'estat')
    def _check_disponibilitat(self):
        for rec in self:
            if rec.estat == 'de_cami':
                if self.search_count([
                    ('empleat_id', '=', rec.empleat_id.id),
                    ('estat', '=', 'de_cami'),
                    ('id', '!=', rec.id),
                ]):
                    raise ValidationError("el empleado ya esta de viaje en otro reparto")
                if self.search_count([
                    ('vehicle_id', '=', rec.vehicle_id.id),
                    ('estat', '=', 'de_cami'),
                    ('id', '!=', rec.id),
                ]):
                    raise ValidationError("el vehiculo ya esta de viaje en otro reparto")

    # bici: max 10 km
    @api.constrains('kilometres', 'vehicle_id')
    def _check_distancia_bicicleta(self):
        for rec in self:
            if rec.vehicle_id.tipus == 'bicicleta' and rec.kilometres > 10:
                raise ValidationError("mas de 10 km no se puede hacer en bicicleta")

    # furgoneta: min 1 km
    @api.constrains('kilometres', 'vehicle_id')
    def _check_distancia_furgoneta(self):
        for rec in self:
            if rec.vehicle_id.tipus == 'furgoneta' and rec.kilometres < 1:
                raise ValidationError("menos de 1 km no se puede hacer en furgoneta")

    # fechas coherentes
    @api.constrains('data_inici', 'data_retorn')
    def _check_dates(self):
        for rec in self:
            if rec.data_inici and rec.data_retorn and rec.data_retorn < rec.data_inici:
                raise ValidationError("la fecha de retorno no puede ser anterior a la de inicio")
