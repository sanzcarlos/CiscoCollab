# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_Phone.py
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
import os
import suds
import ssl

from prettytable import PrettyTable

def Add(logger,csp_soap_client,cucm_variable_axl,cspconfigfile):
    # *------------------------------------------------------------------
    # * function Add(logger,csp_soap_client,cucm_variable_axl)
    # *
    # * Copyright (C) 2016 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

    # Mandatory (pattern,usage)
    logger.debug('Se ha entrado en la funcion Add del archivo cspaxl_Phone.py')
    axl_cucm_Temp = {}
    axl_cucm_Temp['class'] = 'Phone'
    if cucm_variable_axl['IPPhone'][0:3] == 'SIP':
        axl_cucm_Temp['product'] = 'Third-party SIP Device (Advanced)'
    else:
        axl_cucm_Temp['product'] = 'Cisco ' + cucm_variable_axl['IPPhone']
    axl_cucm_Temp['protocolSide'] = 'User'
    if cucm_variable_axl['IPPhone'][0:2] == '39' or \
        cucm_variable_axl['IPPhone'][0:2] == '78' or \
        cucm_variable_axl['IPPhone'][0:7] == 'ATA 190' or \
        cucm_variable_axl['IPPhone'][0:2] == '88' or \
        cucm_variable_axl['IPPhone'][0:2] == '99' or \
        cucm_variable_axl['IPPhone'][0:3] == 'SIP':
        axl_cucm_Protocol = 'SIP'
    else:
        axl_cucm_Protocol = 'SCCP'

    logger.debug('El protocolo utilizado por el telefono es: %s ' % (axl_cucm_Protocol))

    if cucm_variable_axl['IPPhone'][0:2] == '39' or \
        cucm_variable_axl['IPPhone'][0:3] == 'ATA':
        csp_axl_max = '2'
        csp_axl_busy = '1'
    else:
        csp_axl_max = '4'
        csp_axl_busy = '2'
    if cucm_variable_axl['CallWaiting'] == 'NO':
        csp_axl_busy = '1'
    axl_cucm_Temp['protocol'] = axl_cucm_Protocol
    if cucm_variable_axl['IPPhone'][0:3] == 'SIP':
        axl_cucm_Temp['securityProfileName'] = 'Third-party SIP Device Advanced - Standard SIP Non-Secure Profile'
    else:
        axl_cucm_Temp['securityProfileName'] = 'Cisco ' + cucm_variable_axl['IPPhone'] + ' - Standard ' + axl_cucm_Protocol + ' Non-Secure Profile'
    axl_cucm_Temp['locationName'] = cucm_variable_axl['Country'] + '_' + cucm_variable_axl['SiteCode']
    axl_cucm_Temp['devicePoolName'] = 'DP_' + axl_cucm_Temp['locationName']
    axl_cucm_Temp['useTrustedRelayPoint'] = 'Default'
    axl_cucm_Temp['commonDeviceConfigName'] = cspconfigfile['INFO']['customer'].upper() + '_' + cucm_variable_axl['Country']
    axl_cucm_Temp['commonPhoneConfigName'] = cspconfigfile['INFO']['customer'].upper()
    axl_cucm_Temp['builtInBridgeStatus'] = 'Default'
    axl_cucm_Temp['packetCaptureMode'] = 'None'
    if cucm_variable_axl['userPrincipalName'] != '':
        axl_cucm_Temp['ownerUserName'] = cucm_variable_axl['userPrincipalName']
        axl_cucm_Temp['digestUser'] = cucm_variable_axl['userPrincipalName']
    if cucm_variable_axl['IPPhone'][0:3] != 'SIP':
        axl_cucm_Temp['softkeyTemplateName'] = cucm_variable_axl['softkeyTemplateName']
    axl_cucm_Temp['subscribeCallingSearchSpaceName'] = cucm_variable_axl['CSSForward']
    #axl_cucm_Temp['userLocale'] = 'Spanish Spain'
    if cucm_variable_axl['IPPhone'][0:3] == 'ATA':
        axl_cucm_Temp['name'] = 'ATA' + cucm_variable_axl['MACAddress']
    else:
        axl_cucm_Temp['name'] = 'SEP' + cucm_variable_axl['MACAddress']
    axl_cucm_Temp['description'] = cucm_variable_axl['DirectoryNumber'] + ' - ' + cucm_variable_axl['FirstName'] + ' ' + cucm_variable_axl['Surname']
    axl_cucm_Temp_label = cucm_variable_axl['DirectoryNumber'] + ' - ' + cucm_variable_axl['FirstName']

    # Añadimos la linea
    axl_cucm_Temp_display = cucm_variable_axl['FirstName'] + ' ' + cucm_variable_axl['Surname']

    axl_cucm_Temp['lines'] = {
        'line': {'index': '1',
                 'display': axl_cucm_Temp_display[0:30],
                 'displayAscii': axl_cucm_Temp_display[0:30],
                 'e164Mask': cucm_variable_axl['OutgoingDID'],
                 'label': axl_cucm_Temp_label[0:30],
                 'dirn': {'pattern': cucm_variable_axl['DirectoryNumber'], 'routePartitionName': cucm_variable_axl['Partition']},
                 #'associatedEndusers': {'enduser': {'userId': csp_enduser['sAMAccountName'][0]}},
                 'maxNumCalls': csp_axl_max,
                 'busyTrigger': csp_axl_busy}}

    # Limitamos el numero de caracteres de las variables
    axl_cucm_Temp['name'] = axl_cucm_Temp['name'][:128]
    axl_cucm_Temp['description'] = axl_cucm_Temp['description'][:128]
    #axl_cucm_Temp['versionStamp'] = axl_cucm_Temp['versionStamp'][:128]
    #axl_cucm_Temp['mlppDomainId'] = axl_cucm_Temp['mlppDomainId'][:128]

    # Comprobamos que el telefono no existe
    try:
        csp_soap_returnedTags = {'name':'','description':'','devicePoolName':'','callingSearchSpaceName':''}
        csp_soap_searchCriteria = {'name': axl_cucm_Temp['name']}
        result = csp_soap_client.service.listPhone(csp_soap_searchCriteria,csp_soap_returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}

    else:
        if (len(result['return']) == 0):
            logger.info('El telefono %s no existe en el CUCM' % (axl_cucm_Temp['name']))
        else:
            logger.info('El telefono %s existe en el CUCM' % (axl_cucm_Temp['name']))
            return {'Status': False, 'Detail': axl_cucm_Temp['name']}

    # Damos de alta el telefono
    try:
        result = csp_soap_client.service.addPhone(axl_cucm_Temp)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['UUID','Device Name','description'])
        csp_table.add_row([result['return'][:],axl_cucm_Temp['name'], axl_cucm_Temp['description'] ])
        csp_table_response = csp_table.get_string(fields=['UUID','Device Name','description'], sortby="UUID").encode('latin-1')
        return {'Status': True,'Detail':csp_table_response}

def Get(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Get(logger,csp_soap_client,cucm_variable_axl)
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

    # Mandatory (pattern,usage,routePartitionName)

    logger.info ('El valor de la variable es: %s' % (cucm_variable_axl))
    axl_cucm_Temp_Get = {}
    axl_cucm_Temp_Get['name'] = 'SEP0CD0F821AF24'

    try:
        result = csp_soap_client.service.getPhone(name=cucm_variable_axl)
    except:
        logger.debug(sys.exc_info())
        logger.error(str(sys.exc_info()[1],'uft-8'))
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        print (result)
        '''
        csp_table = PrettyTable(['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'])
        csp_table.add_row([0,result['return']['processNode']['name'],result['return']['processNode']['description'],result['return']['processNode']['mac'],result['return']['processNode']['ipv6Name'],result['return']['processNode']['nodeUsage'],result['return']['processNode']['lbmHubGroup'],result['return']['processNode']['processNodeRole'] ])
        csp_table_response = csp_table.get_string(fields=['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'], sortby="id").encode('latin-1')
        '''
        return {'Status': True,'Detail':result}

def List(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function List(logger,csp_soap_client,cucm_variable_axl)
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

    # Mandatory (pattern,usage,routePartitionName)

    try:
        csp_soap_returnedTags = {'name': '', 'description': '', 'ownerUserName': ''}
        csp_soap_searchCriteria = {'name': '%' + cucm_variable_axl + '%'}
        result = csp_soap_client.service.listPhone(csp_soap_searchCriteria,csp_soap_returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['id','name','description','ownerUserName'])
        for x in range(0, len(result['return']['phone'])):
            csp_table.add_row([x,result['return']['phone'][x]['name'],result['return']['phone'][x]['description'],result['return']['phone'][x]['ownerUserName']['value'] ])
        csp_table_response = csp_table.get_string(fields=['id','name','description','ownerUserName'], sortby="id").encode('latin-1')
        logger.info('\n\n' + str(csp_table_response,'latin-1')  + '\n')
        return {'Status':True,'Detail':csp_table_response}

'''
def Remove(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Remove(logger,csp_soap_client,cucm_variable_axl)
    # *
    # * Copyright (C) 2016 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

    # Mandatory (pattern,usage,routePartitionName)
    try:
        result = csp_soap_client.service.removeTransPattern(pattern=cucm_variable_axl['pattern'],routePartitionName=cucm_variable_axl['routePartitionName'])
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['UUID','pattern','routePartitionName'])
        csp_table.add_row([result['return'][:],cucm_variable_axl['pattern'], cucm_variable_axl['routePartitionName'] ])
        csp_table_response = csp_table.get_string(fields=['UUID','pattern','routePartitionName'], sortby="UUID").encode('latin-1')
        return {'Status':True,'Detail':csp_table_response}
'''
'''
def Update(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Update(logger,csp_soap_client,cucm_variable_axl)
    # *
    # * Copyright (C) 2016 Carlos Sanz <carlos.sanzpenas@gmail.com>
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

    # Mandatory (pattern,usage,routePartitionName)
'''