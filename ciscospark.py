#! /usr/bin/env python
# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * CUCM_Spark_Rest.py
# *
# * Cisco Spark Rest Python
# *
# * Copyright (C) 2018 Carlos Sanz <carlos.sanzpenas@gmail.com>
# *
# *  This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License
# * as published by the Free Software Foundation; either version 2
# * of the License, or (at your option) any later version.
# *
# *  This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# *------------------------------------------------------------------
# *
# Import Modules
import sys
import platform
import logging
import getopt
import ssl
import time
import uuid
import os
import re
import json
import requests

def _url(path):
    return 'https://api.ciscospark.com/v1' + path

def _fix_at(at):
    at_prefix = 'Bearer '
    if not re.match(at_prefix, at):
        return 'Bearer ' + at
    else:
        return at
# GET Request
def get_me(csp_spark_token):
    logger.debug('Entramos en la funcion get_me')
    # La cabecera es mandada para la autenticacion
    csp_headers = {'Authorization': _fix_at(csp_spark_token), 'content-type': 'application/json; charset=utf-8'}

    # Consulta
    csp_response = requests.get(_url('/people/me'), headers=csp_headers)

    if (csp_response.status_code == requests.codes.ok):
        csp_response_json = csp_response.json()
        print (json.dumps(csp_response_json,indent = 4, sort_keys = True))
    else:
        logger.error('csp_response.status_code')

def get_people(csp_spark_token, email='', displayname='', max=10):
    logger.debug('Entramos en la funcion get_people')
    # La cabecera es mandada para la autenticacion
    csp_headers = {'Authorization': _fix_at(csp_spark_token), 'content-type': 'application/json; charset=utf-8'}
    payload = {'max': max}
    if email:
        payload['email'] = email
    if displayname:
        payload['displayName'] = displayname
    # print (payload)
    csp_response = requests.get(_url('/people'), params=payload, headers=csp_headers)

    if (csp_response.status_code == requests.codes.ok):
        csp_response_json = csp_response.json()
        print (json.dumps(csp_response_json,indent = 4, sort_keys = True))
        return csp_response_json
    else:
        logger.error(csp_response.status_code)
        return csp_response.status_code

def get_license(csp_spark_token):
    logger.debug('Entramos en la funcion get_me')
    # La cabecera es mandada para la autenticacion
    csp_headers = {'Authorization': _fix_at(csp_spark_token), 'content-type': 'application/json; charset=utf-8'}

    # Consulta
    csp_response = requests.get(_url('/licenses'), headers=csp_headers)

    if (csp_response.status_code == requests.codes.ok):
        csp_response_json = csp_response.json()
        print (json.dumps(csp_response_json,indent = 4, sort_keys = True))
        return csp_response_json
    else:
        logger.error(csp_response.status_code)
        return csp_response.status_code

# POST Requests
def post_createuser(csp_spark_token, email='', displayname='', firstName='', lastName=''):
    logger.debug('Entramos en la funcion post_createuser')
    # La cabecera es mandada para la autenticacion
    csp_headers = {'Authorization': _fix_at(csp_spark_token), 'content-type': 'application/json; charset=utf-8'}

    # Configuracion de un usuario dentro de Acuntia con Permisos para Spark y Webex
    csp_payload = {"emails": [email],
                   "displayName": displayname,
                   "firstName": firstName,
                   "lastName": lastName,
                   "orgId": "Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNTE4ZWU2Ny1kYjlkLTQwODktOTQ3MS1iMmM4MjE4YzU5ZWM",
                   "licenses":["Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvMzUxOGVlNjctZGI5ZC00MDg5LTk0NzEtYjJjODIxOGM1OWVjOkNBXzYzYTQ1MTczLWU5NTQtNDExMS1hYThkLTA1MDI3N2Y3ZjdlOQ",
                        "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvMzUxOGVlNjctZGI5ZC00MDg5LTk0NzEtYjJjODIxOGM1OWVjOk1TX2VjZWJhMDc5LWZjOTctNDZhYi1hZjhiLTgxYzc5YjJiNGU3Mw",
                        "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvMzUxOGVlNjctZGI5ZC00MDg5LTk0NzEtYjJjODIxOGM1OWVjOkVFXzRjYzQ3OTM5LTkwNDctNGNmNS05ZTJiLWUxMzhjOTZkMGU0MF9tZWV0YWN1bnRpYS53ZWJleC5jb20",
                        "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvMzUxOGVlNjctZGI5ZC00MDg5LTk0NzEtYjJjODIxOGM1OWVjOkNNUl85MDUwMGE5Yy0yODY2LTQ3NTYtOGVmZi04MjIxOWFiNjRmOWZfbWVldGFjdW50aWEud2ViZXguY29t",
                        "Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvMzUxOGVlNjctZGI5ZC00MDg5LTk0NzEtYjJjODIxOGM1OWVjOkNGX2MwOTY4ZGE4LThlM2ItNDFhOS04ZjE4LTZlZGE1YTdhM2Q1ZQ"],
    }
    # print (payload)
    csp_response = requests.post(_url('/people'), json=csp_payload, headers=csp_headers)

    if (csp_response.status_code == requests.codes.ok):
        csp_response_json = csp_response.json()
        print (json.dumps(csp_response_json,indent = 4, sort_keys = True))
    else:
        logger.error(csp_response.status_code)

    return csp_response_json

def post_createroom(at, title):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'title': title}
    resp = requests.post(url=_url('/people'), json=payload, headers=headers)
    create_room_dict = json.loads(resp.text)
    create_room_dict['statuscode'] = str(resp.status_code)
    return create_room_dict

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-25s %(name)s[%(process)d] : %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='Log/spark_' + time.strftime("%Y%m%d-%H%M%S-") + str(uuid.uuid4()) + '.log',
                        filemode='w',
                        )

    ssl._create_default_https_context = ssl._create_unverified_context
    element_config_file = None
    logger = logging.getLogger('cisco.spark.api')
    logger.setLevel(logging.INFO)

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)-25s %(name)s[%(process)d] : %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    console.setLevel=logger.setLevel
    logging.getLogger('').addHandler(console)

    csp_spark_token = 'ZWU4ZTAzNDctODc2Ni00MTFmLWI2YzgtNDBlMjU0OTA4NWM5MGU0Y2VmZDEtNmY3'

    logger.info('Comienzo del script')

    # Obtenemos informacion mia
    # get_me(csp_spark_token)

    # Buscamos información de los usuarios de mi organización
    # get_people(csp_spark_token,email='', displayname='David', max=20)

    # Crear un usuario
    # post_createuser(csp_spark_token, email='prueba@acuntia.es', displayname='Usuario de Pruebas', firstName='Usuario', lastName='Prueba')

    # Licencias
    get_license(csp_spark_token)