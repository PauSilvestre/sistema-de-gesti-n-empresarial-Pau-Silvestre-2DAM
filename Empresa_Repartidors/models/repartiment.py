# -*- coding: utf-8 -*-
# model principal, gestiona cada enviament
# relacions many2one amb empleat, vehicle i client
# restriccions: carnet, distancia, vehicle ja de viatge, etc.
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Repartiment(models.Model):
    _name = 'repartiment.repartiment'
    _description = 'repartiment / enviament'
    # ordenat per data recepcio i urgencia (organs primer, baixa prioritat al final)
    _order = 'data_recepcio, urgencia'

    # codi autonumeric unic (sequence), es genera sol al crear
    codi = fields.Char('codi', readonly=True, copy=False, default='nou')

    # dates del repartiment
    data_inici = fields.Datetime('data i hora inici')
    data_retorn = fields.Datetime('data i hora retorn')
    data_recepcio = fields.Date('data recepcio')

    # relacio many2one amb empleat (cada repartiment te 1 empleat)
    empleat_id = fields.Many2one(
        'repartiment.empleat', string='repartidor', required=True
    )
    # relacio many2one amb vehicle
    vehicle_id = fields.Many2one(
        'repartiment.vehicle', string='vehicle', required=True
    )
    # relacio many2one amb client emissor
    client_id = fields.Many2one(
        'repartiment.client', string='client emissor', required=True
    )

    # dades del paquet
    kilometres = fields.Float('kilometres')
    pes = fields.Float('pes (kg)')
    volum = fields.Float('volum (m3)')
    observacions = fields.Text('observacions')

    # dades del receptor (text lliure, no es un model a part)
    receptor_nom = fields.Char('nom receptor')
    receptor_telefon = fields.Char('telefon receptor')
    receptor_adreca = fields.Char('adreça receptor')

    # estat del repartiment amb colors a la vista tree
    estat = fields.Selection([
        ('no_ha_eixit', 'no ha eixit'),
        ('de_cami', 'de camí'),
        ('entregada', 'entregada'),
    ], string='estat', default='no_ha_eixit', required=True)

    # urgencia amb categories ordenades (organs = 1 = mes urgent)
    urgencia = fields.Selection([
        ('1', 'organs humans'),
        ('2', 'aliments refrigerats'),
        ('3', 'aliments'),
        ('4', 'alta prioritat'),
        ('5', 'baixa prioritat'),
    ], string='urgència', default='5', required=True)

    # genera el codi autonumeric usant ir.sequence al crear el registre
    @api.model
    def create(self, vals):
        # si no te codi o es 'nou', li assigna un de la sequencia
        if vals.get('codi', 'nou') == 'nou':
            vals['codi'] = self.env['ir.sequence'].next_by_code('repartiment.repartiment') or 'nou'
        return super().create(vals)

    # l'empleat ha de tindre carnet si el vehicle ho requereix
    @api.constrains('empleat_id', 'vehicle_id')
    def _check_carnet(self):
        for rec in self:
            if rec.vehicle_id.tipus == 'ciclomotor' and not rec.empleat_id.carnet_ciclomotor:
                raise ValidationError(
                    'l\'empleat no te carnet de ciclomotor i el vehicle es un ciclomotor'
                )
            if rec.vehicle_id.tipus == 'furgoneta' and not rec.empleat_id.carnet_furgoneta:
                raise ValidationError(
                    'l\'empleat no te carnet de furgoneta i el vehicle es una furgoneta'
                )

    # no es pot crear viatge si empleat o vehicle ja estan de viatge
    @api.constrains('empleat_id', 'vehicle_id', 'estat')
    def _check_disponibilitat(self):
        for rec in self:
            if rec.estat != 'entregada':
                # busca repartiments actius del mateix empleat (exclou el actual)
                empleat_actiu = self.search([
                    ('empleat_id', '=', rec.empleat_id.id),
                    ('estat', '=', 'de_cami'),
                    ('id', '!=', rec.id),
                ])
                if empleat_actiu:
                    raise ValidationError(
                        'l\'empleat ja esta de viatge en un altre repartiment'
                    )
                # busca repartiments actius del mateix vehicle
                vehicle_actiu = self.search([
                    ('vehicle_id', '=', rec.vehicle_id.id),
                    ('estat', '=', 'de_cami'),
                    ('id', '!=', rec.id),
                ])
                if vehicle_actiu:
                    raise ValidationError(
                        'el vehicle ja esta de viatge en un altre repartiment'
                    )

    # mes de 10 km no es pot fer en bicicleta
    @api.constrains('kilometres', 'vehicle_id')
    def _check_distancia_bicicleta(self):
        for rec in self:
            if rec.vehicle_id.tipus == 'bicicleta' and rec.kilometres > 10:
                raise ValidationError(
                    'els repartiments de mes de 10 km no es poden fer en bicicleta'
                )

    # menys de 1 km no es pot fer en furgoneta
    @api.constrains('kilometres', 'vehicle_id')
    def _check_distancia_furgoneta(self):
        for rec in self:
            if rec.vehicle_id.tipus == 'furgoneta' and rec.kilometres < 1:
                raise ValidationError(
                    'els repartiments de menys de 1 km no es poden fer en furgoneta'
                )
