# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class Main(http.Controller):

    @http.route('/ligafutbol/equipo/json', type='http', auth='none', csrf=False)
    def obtenerDatosEquiposJSON(self):
        equipos = request.env['liga.equipo'].sudo().search([])
        listaDatosEquipos = []
        for equipo in equipos:
            listaDatosEquipos.append([
                equipo.nombre,
                str(equipo.fecha_fundacion),
                equipo.jugados,
                equipo.puntos,
                equipo.victorias,
                equipo.empates,
                equipo.derrotas,
            ])
        json_result = json.dumps(listaDatosEquipos)
        return json_result

    @http.route('/eliminarempates', type='http', auth='none', csrf=False)
    def eliminar_empates(self):
        partidos = request.env['liga.partido'].sudo().search([])
        eliminados = 0
        for partido in partidos:
            if partido.goles_casa == partido.goles_fuera:
                partido.unlink()
                eliminados += 1
        return "Partidos eliminados: %d" % eliminados
