# -*- coding: utf-8 -*-
# wizard per crear repartiments de forma simplificada
# model transitori (no es guarda a la BD)
# els models empleat, vehicle, client i repartiment
from odoo import models, fields

class RepartimentWizard(models.TransientModel):
    _name = 'repartiment.repartiment.wizard'
    _description = 'assistent per crear repartiments de forma rapida'

    # camps basics per crear un repartiment rapid
    empleat_id = fields.Many2one('repartiment.empleat', string='repartidor', required=True)
    vehicle_id = fields.Many2one('repartiment.vehicle', string='vehicle', required=True)
    client_id = fields.Many2one('repartiment.client', string='client emissor', required=True)
    data_recepcio = fields.Date('data recepcio', required=True)
    kilometres = fields.Float('kilometres')
    urgencia = fields.Selection([
        ('1', 'organs humans'),
        ('2', 'aliments refrigerats'),
        ('3', 'aliments'),
        ('4', 'alta prioritat'),
        ('5', 'baixa prioritat'),
    ], string='urgencia', default='5', required=True)
    receptor_nom = fields.Char('nom receptor')

    def action_crear_repartiment(self):
        """crea el repartiment real al model repartiment.repartiment amb les dades del wizard"""
        for wiz in self:
            self.env['repartiment.repartiment'].create({
                'empleat_id': wiz.empleat_id.id,
                'vehicle_id': wiz.vehicle_id.id,
                'client_id': wiz.client_id.id,
                'data_recepcio': wiz.data_recepcio,
                'kilometres': wiz.kilometres,
                'urgencia': wiz.urgencia,
                'receptor_nom': wiz.receptor_nom,
            })
