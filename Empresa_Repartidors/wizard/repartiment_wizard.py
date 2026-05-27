from odoo import models, fields


# modelo transitorio
class RepartimentWizard(models.TransientModel):
    _name = 'repartiment.repartiment.wizard'
    _description = 'asistente crear reparto'

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

    # crea reparto y abre su ficha
    def action_crear_repartiment(self):
        self.ensure_one()
        nou = self.env['repartiment.repartiment'].create({
            'empleat_id': self.empleat_id.id,
            'vehicle_id': self.vehicle_id.id,
            'client_id': self.client_id.id,
            'data_recepcio': self.data_recepcio,
            'kilometres': self.kilometres,
            'urgencia': self.urgencia,
            'receptor_nom': self.receptor_nom,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'repartiment.repartiment',
            'res_id': nou.id,
            'view_mode': 'form',
            'target': 'current',
        }
