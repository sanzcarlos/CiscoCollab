#! /usr/bin/python3
# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * CUCM_axl.py
# *
# * Cisco AXL Python
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
import suds
import ssl
import time
import uuid
import os
import csv
import json

from CiscoAXL import *

from prettytable import PrettyTable
from configobj import ConfigObj
from suds.client import Client
from suds.cache import NoCache

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

def get_usage():
    logger.debug('Ha entrado en la funcion get_usage()')
    return "Uso: -c <Config file>"

def client_soap(config_file):
    # *------------------------------------------------------------------
    # * function client_soap(config_file)
    # *
    # * Copyright (C) 2015 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

    logger.debug('Ha entrado en la funcion client_soap()')
    csp_cmserver = cspconfigfile['CUCM']['server']
    csp_username = cspconfigfile['CUCM']['user']
    csp_password = cspconfigfile['CUCM']['pass']
    csp_version = cspconfigfile['CUCM']['version']

    if platform.system() == 'Windows':
        logger.debug('El sistema operativo es: %s' % (platform.system()))
        wsdl = 'file:///' + os.getcwd().replace ("\\","//") + '//Schema//CUCM//' + csp_version + '//AXLAPI.wsdl'
    else:
        logger.debug('El sistema operativo es: %s' % (platform.system()))
        wsdl = 'file:///' + os.getcwd() + '/Schema/CUCM/' + csp_version + '/AXLAPI.wsdl'

    csp_location = 'https://' + csp_cmserver + ':8443/axl/'

    logger.debug('El valor de csp_cmserver es: %s' % (csp_cmserver))
    logger.debug('El valor de csp_username es: %s' % (csp_username))
    logger.debug('El valor de csp_version es: %s' % (csp_version))
    logger.debug('El valor de csp_location es: %s' % (csp_location))
    logger.debug('El valor de wsdl es: %s' % (wsdl))

    # Tiempo de inicio de ejecucion.
    try:
        csp_soap_client = suds.client.Client(wsdl,
                                             location = csp_location,
                                             username = csp_username,
                                             password = csp_password,
                                             cache = NoCache(),
                                             )
    except:
        logger.error('Se ha producido un error al crear el cliente soap')
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha creado el cliente SOAP.')

    try:
        csp_version_long = cspaxl_version.Get(logger,csp_soap_client,csp_cmserver)
    except:
        logger.error('Se ha producido un error al comprobar la version del servidor soap')
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        if csp_version_long['Status']:
            logger.info('Se ha verificado la version del servidor soap.')
            csp_table = PrettyTable(['Server','Username','Version Conf_File','Version Real'])
            csp_table.add_row([csp_cmserver, csp_username, csp_version,csp_version_long['Detail']])
            csp_table_response = csp_table.get_string(
                fields=['Server', 'Username', 'Version Conf_File', 'Version Real'], sortby="Server")
            logger.info('\n\n' + csp_table_response + '\n')
            return csp_soap_client
        else:
            logger.error('Se ha proucido un error comprobando la version del servidor soap')
            sys.exit()

def Customer(logger,csp_soap_client,cspconfigfile):
    '''
    # *------------------------------------------------------------------
    # * function Customer(logger,csp_soap_client,cspconfigfile)
    # *
    # * Copyright (C) 2018 Carlos Sanz <carlos.sanzpenas@gmail.com>
    # *
    # *------------------------------------------------------------------
    '''

    logger.debug('Ha entrado en la funcion Customer del archivo customer.py')

    # Sincronizamos el CUCM con el Ldap
    '''
    logger.info('Sincronizamos el CUCM con el Ldap')
    try:
        result = cspaxl_LdapSync.do_start(logger, csp_soap_client, cspconfigfile['LDAP']['name'])
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
    else:
        logger.debug('Se ha ejecutado la accion anterior\n\
                     \t\t\t\t\t\t\t\t\t\tEstado:\t\t%s\n\
                     \t\t\t\t\t\t\t\t\t\tDetalles:\t%s' % (result['Status'], result['Detail']))

    '''

    '''
    # *------------------------------------------------------------------
    # * Definimos las funciones que podemos hacer dentro del cliente
    # *------------------------------------------------------------------
    '''
    csp_table_file = PrettyTable(['id', 'Funcion'])
    csp_table_id = 0
    csp_funtion = ['Alta Fichero Usuarios','Alta Sede','Translation Pattern','Calling Party Transformation Pattern','Usuarios','Salir']

    for csp_fun in csp_funtion:
        csp_table_file.add_row([csp_table_id, csp_fun])
        csp_table_id += 1

    print (csp_table_file)

    csp_fun = int(input('Seleccione la opcion deseada: '))

    if csp_fun == 0:
        logger.debug('Ha seleccionado la funcion %s' % csp_funtion[csp_fun])
        AltaFicheroUsuario(logger, csp_soap_client, cspconfigfile)
    elif csp_fun == 1:
        logger.debug('Ha seleccionado la funcion %s' % csp_funtion[csp_fun])
        AltaSede(logger, csp_soap_client, cspconfigfile)
    elif csp_fun == 2:
        logger.debug('Ha seleccionado la funcion %s' % csp_funtion[csp_fun])
        TranslationPattern(logger, csp_soap_client, cspconfigfile)
    elif csp_fun == 3:
        logger.debug('Ha seleccionado la funcion %s' % csp_funtion[csp_fun])
        CallingPartyTransformationPattern(logger, csp_soap_client, cspconfigfile)
    elif csp_fun == 4:
        logger.debug('Ha seleccionado la funcion %s' % csp_funtion[csp_fun])
        EndUser(logger, csp_soap_client, cspconfigfile)
    elif csp_fun == 5:
        logger.debug('Ha seleccionado la funcion %s' % csp_funtion[csp_fun])
        sys.exit()
    else:
        logger.error('El valor introducido no es valido')

def EndUser(logger,csp_soap_client,cspconfigfile):
    '''
    # *------------------------------------------------------------------
    # * function EndUser(logger,csp_soap_client)
    # *
    # * Copyright (C) 2020 Carlos Sanz <carlos.sanzpenas@gmail.com>
    # *
    # *------------------------------------------------------------------
    '''

    logger.debug('Ha entrado en la funcion EndUser del archivo customer.py')

    csp_csv_file_path = 'csv/'
    csp_filename = csp_csv_file_path + input('Nombre del fichero: ')
    try:
        csp_csv_file = open(csp_filename, 'r', encoding='utf-8')
    except:
        logger.error('Se ha producido un error al abrir el archivo %s' % (csp_filename))
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha abierto el archivo %s' % (csp_filename))
        csp_field_names = (
            "FirstName", "Surname", "userPrincipalName", "DirectoryNumber", "Type", "IPPhone", "MACAddress",
            "IncomingDID", "OutgoingDID", "CSS", "VoiceMail", "CallPickupGroup", "WebUser", "Locale", "ForwardCSS",
            "CallWaiting", "SRST")
        csp_file_reader = csv.DictReader(csp_csv_file, csp_field_names)

        csp_add_status = PrettyTable(['UserID', 'UserID Status'])

        for row in csp_file_reader:
            row['FirstName']         = row['FirstName'].strip()
            row['Surname']           = row['Surname'].strip()
            row['userPrincipalName'] = row['userPrincipalName'].strip()
            row['Type']              = row['Type'].strip()
            row['IPPhone']           = row['IPPhone'].strip()
            row['MACAddress']        = row['MACAddress'].strip()
            row['DirectoryNumber']   = row['DirectoryNumber'].strip()
            row['IncomingDID']       = row['IncomingDID'].strip()
            row['OutgoingDID']       = row['OutgoingDID'].strip()
            row['CSS']               = row['CSS'].strip()
            row['VoiceMail']         = row['VoiceMail'].strip()
            row['CallPickupGroup']   = row['CallPickupGroup'].strip()
            row['WebUser']           = row['WebUser'].strip()
            row['Locale']            = row['Locale'].strip()
            row['ForwardCSS']        = row['ForwardCSS'].strip()
            row['CallWaiting']       = row['CallWaiting'].strip()
            row['SRST']              = row['SRST'].strip()
            row['Customer']          = cspconfigfile['INFO']['customer'].upper()

            # Damos de alta el usuario
            csp_temp = cspaxl_User.Add(logger, csp_soap_client, row)
            if csp_temp['Status'] is True:
                logger.debug('Se ha dado de alta el Usuario \n\n%s\n' % (str(csp_temp['Detail'],'utf-8')))
            else:
                logger.debug('No se ha dado de alta el Usuario:    %s' % (csp_temp['Detail']))
            csp_row_enduser = csp_temp['Status']

            csp_add_status.add_row([row['userPrincipalName'], csp_row_enduser])

        csp_add_status_response = csp_add_status.get_string(fields=['UserID', 'UserID Status'],
                                                  sortby='UserID').encode('latin-1')

        logger.info('Se han procesado los siguientes usuarios:\n\n%s\n' % (str(csp_add_status_response,'utf-8')))

def AltaFicheroUsuario(logger,csp_soap_client,cspconfigfile):
    '''
    # *------------------------------------------------------------------
    # * function Customer(logger,csp_soap_client)
    # *
    # * Copyright (C) 2018 Carlos Sanz <carlos.sanzpenas@gmail.com>
    # *
    # *------------------------------------------------------------------
    '''

    logger.debug('Ha entrado en la funcion AltaFicheroUsuario del archivo customer.py')

    csp_csv_file_path = 'csv/'
    csp_filename = csp_csv_file_path + input('Nombre del fichero: ')
    try:
        csp_csv_file = open(csp_filename, 'r', encoding='utf-8')
    except:
        logger.error('Se ha producido un error al abrir el archivo %s' % (csp_filename))
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha abierto el archivo %s' % (csp_filename))
        csp_field_names = (
            "FirstName", "Surname", "userPrincipalName", "DirectoryNumber", "Type", "IPPhone", "MACAddress",
            "IncomingDID", "OutgoingDID", "CSS", "VoiceMail", "CallPickupGroup", "WebUser", "Locale", "ForwardCSS",
            "CallWaiting", "SRST")
        csp_file_reader = csv.DictReader(csp_csv_file, csp_field_names)

        csp_customer_countrycode = input('Codigo del Pais: ')
        csp_customer_sitecode = input('Codigo de la sede: ')

        logger.info('El codigo del pais es: %s' % (csp_customer_countrycode))
        logger.info('El codigo de la sede es: %s' % (csp_customer_sitecode))

        csp_add_status = PrettyTable(['Directory Number', 'DN Status', 'IP Phone Model', 'MAC Address', 'IP Phone Status'])

        for row in csp_file_reader:
            row['Country']    = csp_customer_countrycode
            row['SiteCode']   = csp_customer_sitecode
            row['CSSForward'] = csp_customer_countrycode + cspconfigfile['CONFIG']['default-CSSForward']
            row['Partition']  = cspconfigfile['CONFIG']['default-Partition']
            row['softkeyTemplateName']  = cspconfigfile['CONFIG']['default-softkeyTemplateName']

            # Comprobamos si tenemos que dar de alta el CPG
            if row['CallPickupGroup'] != '':
                logger.info('Hay que configurar el Call PickUp Group %s' % (row['CallPickupGroup']))
                # Tendriamos que definir la secuencia para crear el CPG
                # CPG_<Country_Code>_<Site_Code>_<Excel_File>
            else:
                logger.info('No hay que configurar un Call PickUp Group')
            '''
            if row['CallPickupGroup'] != '':
                logger.debug('Comprobamos si tenemos que crearnos el Call Pickup Group')
                csp_temp = cspaxl_CallPickupGroup.Add(logger, csp_soap_client, row)
            '''

            row['FirstName']         = row['FirstName'].strip()
            row['Surname']           = row['Surname'].strip()
            row['userPrincipalName'] = row['userPrincipalName'].strip()
            row['Type']              = row['Type'].strip()
            row['IPPhone']           = row['IPPhone'].strip()
            row['MACAddress']        = row['MACAddress'].strip()
            row['DirectoryNumber']   = row['DirectoryNumber'].strip()
            row['IncomingDID']       = row['IncomingDID'].strip()
            row['OutgoingDID']       = row['OutgoingDID'].strip()
            row['CSS']               = row['CSS'].strip()
            row['CSSForward']        = row['CSSForward'].strip()
            row['VoiceMail']         = row['VoiceMail'].strip()
            row['CallPickupGroup']   = row['CallPickupGroup'].strip()
            row['WebUser']           = row['WebUser'].strip()
            row['Locale']            = row['Locale'].strip()
            row['ForwardCSS']        = row['ForwardCSS'].strip()
            row['CallWaiting']       = row['CallWaiting'].strip()
            row['SRST']              = row['SRST'].strip()
            row['Partition']         = row['Partition'].strip()

            # Damos de alta la extension
            csp_temp = cspaxl_Line.Add(logger, csp_soap_client, row)
            if csp_temp['Status'] is True:
                logger.debug('Se ha dado de alta la linea\n\n%s\n' % (str(csp_temp['Detail'],'utf-8')))
            else:
                logger.debug('No se ha dado de alta la linea:    %s' % (csp_temp['Detail']))
            csp_row_dn = csp_temp['Status']

            # Damos de alta el telefono
            csp_temp = cspaxl_Phone.Add(logger, csp_soap_client, row, cspconfigfile)
            if csp_temp['Status'] is True:
                logger.info('Se ha dado de alta el telefono\n\n%s\n' % (str(csp_temp['Detail'],'utf-8')))
            else:
                logger.info('No se ha dado de alta el telefono: %s' % (csp_temp['Detail']))
            csp_row_phone = csp_temp['Status']

            csp_add_status.add_row([row['DirectoryNumber'], csp_row_dn, row['IPPhone'], row['MACAddress'], csp_row_phone])

        csp_add_status_response = csp_add_status.get_string(fields=['Directory Number', 'DN Status', 'IP Phone Model', 'MAC Address', 'IP Phone Status'],
                                                  sortby='Directory Number').encode('latin-1')

        logger.info('Se han procesado los siguientes telefonos:\n\n%s\n' % (str(csp_add_status_response,'utf-8')))

def AltaSede(logger,csp_soap_client, cspconfigfile):
    '''
    # *------------------------------------------------------------------
    # * function Customer(logger,csp_soap_client)
    # *
    # * Copyright (C) 2018 Carlos Sanz <carlos.sanzpenas@gmail.com>
    # *
    # *------------------------------------------------------------------
    '''

    #logger.debug('Ha entrado en la funcion AltaSede del archivo customer_Gestamp.py')
    #csp_temp = cspaxl_Phone.Get(logger, csp_soap_client,'SEP0CD0F821AF24')
    #print (csp_temp)
    #csp_customer_countrycode = input('Codigo del Pais: ')
    #csp_customer_sitecode = input('Codigo de la sede: ')

    #cspaxl_Phone.Get(logger, csp_soap_client, 'BOT41799')

    # Date/Time Group
    '''
    # *------------------------------------------------------------------
    # * Date/Time Group
    # *
    # * Format: 'DTG_' + csp_customer_countrycode
    # *
    # *------------------------------------------------------------------
    '''
    # Location
    '''
    # *------------------------------------------------------------------
    # * Location
    # *
    # * Format: 'L_' + csp_customer_countrycode + '_' + csp_customer_sitecode
    # *
    # *------------------------------------------------------------------
    '''
    # Physical Location
    '''
    # *------------------------------------------------------------------
    # * Physical Location
    # *
    # * Format: 'PL_' + csp_customer_countrycode + '_' + csp_customer_sitecode
    # *
    # *------------------------------------------------------------------
    '''
    # Region
    '''
    # *------------------------------------------------------------------
    # * Region
    # *
    # * Format: 'R_' + csp_customer_countrycode + '_' + csp_customer_sitecode
    # *
    # *------------------------------------------------------------------
    '''
    # Partition
    '''
    # *------------------------------------------------------------------
    # * Partition
    # *
    # * Format: 'XFORM_ANI_SALIDA_' + csp_customer_countrycode + '-' + csp_customer_sitecode
    # * Format: 'XFORM_DNIS_SALIDA_' + csp_customer_countrycode + '-' + csp_customer_sitecode
    # *
    # *------------------------------------------------------------------
    '''
    # Calling Search Space
    '''
    # *------------------------------------------------------------------
    # * Calling Search Space
    # *
    # * Format: 'XFORM_ANI_SALIDA_' + csp_customer_countrycode + '-' + csp_customer_sitecode
    # * Format: 'XFORM_DNIS_SALIDA_' + csp_customer_countrycode + '-' + csp_customer_sitecode
    # *
    # *------------------------------------------------------------------
    '''
    # SIP Trunk
    '''
    # *------------------------------------------------------------------
    # * SIP Trunk
    # *
    # * Format: 'CS_GAUIPT_' + csp_customer_countrycode + '_' + csp_customer_sitecode
    # *
    # *------------------------------------------------------------------
    '''
    # Route Group
    '''
    # *------------------------------------------------------------------
    # * Route Group
    # *
    # * Format: 'RG_GW_' + csp_customer_countrycode + '_' + csp_customer_sitecode
    # *
    # *------------------------------------------------------------------
    '''
    # Device Pool
    '''
    # *------------------------------------------------------------------
    # * Device Pool
    # *
    # * Format: 'DP_' + csp_customer_countrycode + '_' + csp_customer_sitecode
    # *
    # *------------------------------------------------------------------
    '''

def TranslationPattern(logger,csp_soap_client, cspconfigfile):
    '''
    # *------------------------------------------------------------------
    # * function Customer(logger,csp_soap_client)
    # *
    # * Copyright (C) 2019 Carlos Sanz <carlos.sanzpenas@gmail.com>
    # *
    # *------------------------------------------------------------------
    '''

    logger.debug('Ha entrado en la funcion TranslationPattern')
    csp_csv_file_path = 'csv/'
    csp_filename = csp_csv_file_path + input('Nombre del fichero: ')
    try:
        csp_csv_file = open(csp_filename, 'r')
    except:
        logger.error('Se ha producido un error al abrir el archivo %s' % (csp_filename))
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha abierto el archivo %s' % (csp_filename))
        csp_field_names = (
            "Pattern", "Partition", "CSS", "CalledPartyTransformMask")
        csp_file_reader = csv.DictReader(csp_csv_file, csp_field_names)

        csp_add_status = PrettyTable(['Pattern', 'Partition', 'CSS', 'Called Party Transform Mask', 'TP Status'])

        for row in csp_file_reader:
            # Comprobamos si existe el Translation Pattern
            row['Pattern']                   = row['Pattern'].strip()
            row['Partition']                 = row['Partition'].strip()
            row['CSS']                       = row['CSS'].strip()
            row['CalledPartyTransformMask']  = row['CalledPartyTransformMask'].strip()

            # Damos de alta el Translation Pattern
            csp_temp = cspaxl_TransPattern.Add(logger, csp_soap_client, row)
            if csp_temp['Status'] is True:
                logger.info('Se ha dado de alta el siguiente Translation Pattern: %s en la Partition %s' % (row['Pattern'],row['Partition']))
            else:
                logger.error('No se ha dado de alta el siguiente Translation Pattern: %s en la Partition %s' % (row['Pattern'],row['Partition']))

            csp_add_status.add_row([row['Pattern'], row['Partition'], row['CSS'], row['CalledPartyTransformMask'], csp_temp['Status']])

        csp_add_status_response = csp_add_status.get_string(fields=['Pattern', 'Partition', 'CSS', 'Called Party Transform Mask', 'TP Status'],
                                                  sortby='Pattern').encode('latin-1')
        logger.info('Se han procesado los siguientes TP:\n\n%s\n' % (str(csp_add_status_response,'utf-8')))

def CallingPartyTransformationPattern(logger,csp_soap_client, cspconfigfile):
    '''
    # *------------------------------------------------------------------
    # * function Customer(logger,csp_soap_client)
    # *
    # * Copyright (C) 2018 Carlos Sanz <carlos.sanzpenas@gmail.com>
    # *
    # *------------------------------------------------------------------
    '''

    logger.debug('Ha entrado en la funcion CallingPartyTransformationPattern')

    csp_csv_file_path = 'csv/'
    #csp_filename = csp_csv_file_path + input('Nombre del fichero: ')
    csp_filename = csp_csv_file_path + 'AYTO_ES_CPT'
    try:
        csp_csv_file = open(csp_filename, 'r')
    except:
        logger.error('Se ha producido un error al abrir el archivo %s' % (csp_filename))
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        sys.exit()
    else:
        logger.info('Se ha abierto el archivo %s' % (csp_filename))
        csp_field_names = (
            'Pattern', 'Partition', 'callingPartyTransformationMask')
        csp_file_reader = csv.DictReader(csp_csv_file, csp_field_names)

        csp_add_status = PrettyTable(['Pattern', 'Partition', 'Calling Party Transform Mask', 'Status'])

        for row in csp_file_reader:
            # Comprobamos si existe el Calling Party Transformation Pattern
            row['Pattern']                         = row['Pattern'].strip()
            row['Partition']                       = row['Partition'].strip()
            row['callingPartyTransformationMask']  = row['callingPartyTransformationMask'].strip()

            # Damos de alta el Calling Party Transformation Pattern
            csp_temp = cspaxl_CallingPartyTransformationPattern.Add(logger, csp_soap_client, row)
            if csp_temp['Status'] is True:
                logger.debug('Se ha dado de alta el siguiente Calling Party Transformation Pattern:\n\n%s\n' % (csp_temp['Detail']))
            else:
                logger.debug('No se ha dado de alta el siguiente Calling Party Transformation Pattern:\n\n%s\n' % (csp_temp['Detail']))

            csp_add_status.add_row([row['Pattern'], row['Partition'], row['callingPartyTransformationMask'], csp_temp['Status']])

        csp_add_status_response = csp_add_status.get_string(fields=['Pattern', 'Partition', 'Calling Party Transform Mask', 'Status'],
                                                  sortby='Pattern').encode('latin-1')
        logger.info('Se han procesado los siguientes Calling Party Transformation Pattern:\n\n%s\n' % (str(csp_add_status_response,'utf-8')))

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)-25s %(name)s[%(process)d] : %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='Log/' + time.strftime("%Y%m%d-%H%M%S-") + str(uuid.uuid4()) + '.log',
                        filemode='w',
                        )

    ssl._create_default_https_context = ssl._create_unverified_context
    element_config_file = None
    logger = logging.getLogger('cisco.cucm.axl')
    logger.setLevel(logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.CRITICAL)
    logging.getLogger('suds.transport').setLevel(logging.CRITICAL)
    logging.getLogger('suds.xsd.schema').setLevel(logging.CRITICAL)
    logging.getLogger('suds.wsdl').setLevel(logging.CRITICAL)

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)-25s %(name)s[%(process)d] : %(levelname)-8s %(message)s')
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
    csp_soap_client = client_soap(element_config_file)
    #CiscoCustomer.Customer(logger, csp_soap_client,cspconfigfile)
    Customer(logger, csp_soap_client,cspconfigfile)
    logger.info('Se cerrara el programa')
    sys.exit()