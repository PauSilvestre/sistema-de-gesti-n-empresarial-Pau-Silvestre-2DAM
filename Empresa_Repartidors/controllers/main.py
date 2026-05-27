import json
from odoo import http
from odoo.http import request


# endpoint publico
class RepartimentController(http.Controller):

    @http.route('/repartiment/estat', type='http', auth='none', csrf=False)
    def obtenir_estat(self, codi=None, **kwargs):
        if not codi:
            return json.dumps({'error': 'falta el parametro codi'})

        rep = request.env['repartiment.repartiment'].sudo().search(
            [('codi', '=', codi)], limit=1
        )
        if not rep:
            return json.dumps({'error': 'no se ha encontrado el reparto ' + codi})

        return json.dumps({
            'codi': rep.codi,
            'estat': rep.estat,
            'empleat': (rep.empleat_id.nom or '') + ' ' + (rep.empleat_id.cognom or ''),
            'vehicle': rep.vehicle_id.tipus,
            'urgencia': rep.urgencia,
        })
