# cliente XML-RPC para Odoo

import xmlrpc.client
import re
import sys

URL = 'http://localhost:8069'
DB = 'Pausiar'
USER = 'ogpausiar@gmail.com'
PASSWORD = 'Pausilves1'

def conectar():
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USER, PASSWORD, {})
    if not uid:
        raise Exception('Error d\'autenticació. Comprova URL, DB, USER i PASSWORD.')
    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    return uid, models

def parsear_params(texto):
    texto = texto.replace('\u201c', '"').replace('\u201d', '"')
    texto = texto.replace('\u2018', '"').replace('\u2019', '"')
    params = {}
    matches = re.findall(r'(\w+)\s*=\s*"([^\"]*)"', texto)
    for key, value in matches:
        params[key.strip()] = value.strip()
    return params

def crear_socio(uid, models, params):
    nombre = params.get('nombre', '').strip()
    num_socio = params.get('num_socio', '').strip()
    if not nombre or not num_socio:
        print("Error: falta 'nombre' o 'num_socio'.")
        return
    try:
        existents = models.execute_kw(DB, uid, PASSWORD, 'res.partner', 'search', [[['ref', '=', num_socio]]])
        if existents:
            print(f"Avís: Ja existeix un soci amb num_socio='{num_socio}' (ID: {existents[0]}).")
            return
        partner_id = models.execute_kw(DB, uid, PASSWORD, 'res.partner', 'create', [{'name': nombre, 'ref': num_socio}])
        print(f"Soci creat amb èxit en Odoo (ID: {partner_id}).")
    except Exception as e:
        print(f"Error al crear el soci: {e}")

def consultar_socio(uid, models, params):
    num_socio = params.get('num_socio', '').strip()
    if not num_socio:
        print("Error: falta 'num_socio'.")
        return
    try:
        result = models.execute_kw(DB, uid, PASSWORD, 'res.partner', 'search_read', [[['ref', '=', num_socio]]], {'fields': ['name', 'ref', 'email', 'phone'], 'limit': 1})
        if result:
            socio = result[0]
            out = f"Dades d'Odoo -> Nom: {socio['name']} | Referència: {socio['ref']}"
            if socio.get('email'):
                out += f" | Email: {socio['email']}"
            if socio.get('phone'):
                out += f" | Telèfon: {socio['phone']}"
            print(out)
        else:
            print(f"No s'ha trobat cap soci amb num_socio='{num_socio}'.")
    except Exception as e:
        print(f"Error al consultar el soci: {e}")

def borrar_socio(uid, models, params):
    num_socio = params.get('num_socio', '').strip()
    if not num_socio:
        print("Error: falta 'num_socio'.")
        return
    try:
        ids = models.execute_kw(DB, uid, PASSWORD, 'res.partner', 'search', [[['ref', '=', num_socio]]])
        if ids:
            models.execute_kw(DB, uid, PASSWORD, 'res.partner', 'unlink', [ids])
            print(f"Soci amb referència '{num_socio}' eliminat correctament.")
        else:
            print(f"No s'ha trobat cap soci amb num_socio='{num_socio}'.")
    except Exception as e:
        print(f"Error al borrar el soci: {e}")

def main():
    print("CLIENT ODOO XML-RPC - Gestió de Contactes")
    try:
        uid, models = conectar()
        print(f"Connexió correcta! UID: {uid}\n")
    except Exception as e:
        print(f"No s'ha pogut connectar: {e}")
        return
    if '--auto-test' in sys.argv:
        test_ref = 'S_AUTOTEST01'
        crear_socio(uid, models, {'nombre': 'Prova Auto', 'num_socio': test_ref})
        consultar_socio(uid, models, {'num_socio': test_ref})
        borrar_socio(uid, models, {'num_socio': test_ref})
        return
    print('Ordres: Crear, Consultar, Borrar, sortir')
    while True:
        try:
            entrada = input('Ordre > ').strip()
        except (KeyboardInterrupt, EOFError):
            print('\nEixint...')
            break
        if entrada.lower() == 'sortir':
            print('Fins aviat!')
            break
        if not entrada:
            continue
        partes = entrada.split(',', 1)
        ordre = partes[0].strip()
        resto = partes[1] if len(partes) > 1 else ''
        params = parsear_params(resto)
        if ordre == 'Crear':
            crear_socio(uid, models, params)
        elif ordre == 'Consultar':
            consultar_socio(uid, models, params)
        elif ordre == 'Borrar':
            borrar_socio(uid, models, params)
        else:
            print('Orden no soportada.')

if __name__ == '__main__':
    main()

