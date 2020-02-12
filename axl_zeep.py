#! /usr/bin/python3
# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * axl_zeep.py
# *
# * Cisco AXL Python
# *
# * Copyright (C) 2019 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

from lxml import etree
from requests import Session
from requests.auth import HTTPBasicAuth

from zeep import Client, Settings, Plugin, xsd
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from prettytable import PrettyTable
from configobj import ConfigObj

import getopt
import logging

import sys
import platform
import time
import uuid
import os
import csv
import urllib3
import json
import pprint

class PrettyLog():
    def __init__(self, obj):
        self.obj = obj
    def __repr__(self):
        return pprint.pformat(self.obj)

# Argumentos pasados por linea de comandos
def parse_command_line(args):
    logger.debug('Ha entrado en la funcion parse_command_line()')
    global element_config_file
    global cspconfigfile
    try:
        opts, args = getopt.getopt(args[1:],"hc:",["config-file="])
    except getopt.GetoptError as err:
        print (str(err))
        logger.info(get_usage())
        sys.exit(2)

    """
     * options:
     *       -c, --config-file <Config file>
    """
    for option, arg in opts:
        if option == '-h':
            logger.info(get_usage())
            sys.exit()
        elif option in ("-c", "--config-file"):
            element_config_file = arg

    if(element_config_file==None):
        logger.info(get_usage())
        csp_table_file=PrettyTable(['id', 'Filename'])
        csp_table_id=0
        csp_dir = 'conf/'
        csp_file = []
        logger.debug('Buscamos todos los archivos *.cfg del directorio conf/')
        for file in os.listdir(csp_dir):
            if file.endswith(".cfg"):
                csp_file.append(file)
                csp_table_file.add_row([csp_table_id,file])
                csp_table_id += 1
        logger.debug('El numero de ficheros de configuracion es: %d',csp_table_id)
        if csp_table_id == 1:
            element_config_file = csp_dir + csp_file[0]
            logger.info('Ha seleccionado el fichero de configuracion: %s' % (element_config_file))
            cspconfigfile = ConfigObj(element_config_file)
            return {'Status':True,'Detail': element_config_file}
        else:
            print (csp_table_file)
            csp_file_config = input('Seleccione el archivo de configuracion: ')
            if int(csp_file_config) > csp_table_id - 1:
                logger.error('Ha seleccionado un fichero erroneo')
                return False
            else:
                element_config_file = csp_dir + csp_file[int(csp_file_config)]
                logger.info('Ha seleccionado el fichero de configuracion: %s' % (element_config_file))
                cspconfigfile = ConfigObj(element_config_file)
                return {'Status':True,'Detail': element_config_file}
    return True

# Help function
def get_usage():
    logger.debug('Ha entrado en la funcion get_usage()')
    return "Uso: -c <Config file>"

# This class lets you view the incoming and outgoing http headers and/or XML
class MyLoggingPlugin(Plugin):
    def ingress(self, envelope, http_headers, operation):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers
    
    def egress(self, envelope, http_headers, operation, binding_options):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers

# Funcion para crear el cliente SOAP
def client_soap(config_file):
    logger.debug('Ha entrado en la funcion client_soap()')
    csp_cmserver = cspconfigfile['CUCM']['server']
    csp_username = cspconfigfile['CUCM']['user']
    csp_password = cspconfigfile['CUCM']['pass']
    csp_version  = cspconfigfile['CUCM']['version']

    if platform.system() == 'Windows':
        logger.debug('El sistema operativo es: %s' % (platform.system()))
        wsdl = 'file://' + os.getcwd().replace ("\\","//") + '//Schema//CUCM//' + csp_version + '//AXLAPI.wsdl'
    else:
        logger.debug('El sistema operativo es: %s' % (platform.system()))
        wsdl = 'file://' + os.getcwd() + '/Schema/CUCM/' + csp_version + '/AXLAPI.wsdl'

    csp_location = 'https://' + csp_cmserver + ':8443/axl/'

    logger.debug('El valor de csp_cmserver es: %s' % (csp_cmserver))
    logger.debug('El valor de csp_username es: %s' % (csp_username))
    logger.debug('El valor de csp_version es: %s' % (csp_version))
    logger.debug('El valor de csp_location es: %s' % (csp_location))
    logger.debug('El valor de wsdl es: %s' % (wsdl))

    # history shows http_headers
    global history
    history = HistoryPlugin()

    # The first step is to create a SOAP client session
    session = Session()

    # We avoid certificate verification by default, but you can uncomment and set
    # your certificate here, and comment out the False setting

    #session.verify = CERT
    session.verify = False
    session.auth = HTTPBasicAuth(csp_username, csp_password)

    transport = Transport(session=session, timeout=10, cache=SqliteCache())
    
    # strict=False is not always necessary, but it allows zeep to parse imperfect XML
    settings = Settings(strict=False, xml_huge_tree=True)

    try:
        csp_soap_client = Client(wsdl,
                                settings=settings,
                                transport=transport,
                                plugins=[MyLoggingPlugin(),history],
                                )
        service = csp_soap_client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding", csp_location)

    except:
        logger.error('Se ha producido un error al crear el cliente soap')
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha creado el cliente SOAP.')
        return service

# Main Function
if __name__=='__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-25s %(name)s [%(process)d]: %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='Log/' + time.strftime("%Y%m%d-%H%M%S-") + str(uuid.uuid4()) + '.log',
                        filemode='w',
                        )
    urllib3.disable_warnings()
    element_config_file = None
    history = None
    logger = logging.getLogger('cisco.cucm.axl.zeep')
    logger.setLevel(logging.INFO)

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)-25s %(name)s [%(process)d]: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    console.setLevel=logger.setLevel
    logging.getLogger('').addHandler(console)

    logger.info('Estamos usando Python v%s' % (platform.python_version()))

    '''
    logger.debug('This is a debug message %s' % (variable))
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical error message')
    '''

    if not parse_command_line(sys.argv):
        logger.error("Error in parsing arguments")
        sys.exit(1)

    logger.info('Se ha seleccionado el cliente: %s' % (cspconfigfile['INFO']['customer'].upper()))
    service = client_soap(element_config_file)

    soap_data = {
        'userid': 'telefonia'
    }

    try:
        user_resp = service.getUser(**soap_data)
    except Fault as err:
        logger.error('Se ha producido un error en la consulta SOAP: %s' % format(err))
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('getUser Response:\n %s' % user_resp)
        logger.info('HTTP Last Send:\n %s' % PrettyLog(history.last_sent))
        logger.info('HTTP Last Received:\n %s' % PrettyLog(history.last_received))

    #CiscoCustomer.Customer(logger, csp_soap_client,cspconfigfile)
    #Customer(logger, csp_soap_client,cspconfigfile)
    logger.info('Se cerrara el programa')
    sys.exit()