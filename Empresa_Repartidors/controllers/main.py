# -*- coding: utf-8 -*-
# web controller: endpoint http per consultar l'estat d'un repartiment pel seu codi
# ruta: /repartiment/estat?codi=REP/00001
# relacionat amb: model repartiment.repartiment (camp codi i estat)
import json
from odoo import http
from odoo.http import request

class RepartimentController(http.Controller):

    # ruta http publica (auth='none' = sense login)
    # csrf=false per permetre peticions externes sense token
    @http.route('/repartiment/estat', type='http', auth='none', csrf=False)
    def obtenir_estat(self, codi=None, **kwargs):
        """rep un codi de repartiment i torna el seu estat en json"""
        if not codi:
            # si no es passa codi, torna error
            return json.dumps({'error': 'falta el parametre codi'})

        # busca el repartiment amb sudo() (perque auth='none' no te permisos)
        repartiment = request.env['repartiment.repartiment'].sudo().search(
            [('codi', '=', codi)], limit=1
        )

        if not repartiment:
            return json.dumps({'error': 'no s\'ha trobat cap repartiment amb codi ' + codi})

        # torna les dades basiques del repartiment en format json
        resultat = {
            'codi': repartiment.codi,
            'estat': repartiment.estat,
            'empleat': repartiment.empleat_id.nom + ' ' + repartiment.empleat_id.cognom,
            'vehicle': repartiment.vehicle_id.tipus,
            'urgencia': repartiment.urgencia,
        }
        return json.dumps(resultat)
