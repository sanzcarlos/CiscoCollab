# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_Line.py
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
# Import Modules
import sys
import os
from unittest.case import _AssertRaisesContext

import suds
import ssl

from prettytable import PrettyTable

def String2ASCI (logger,csp_text):
    # *------------------------------------------------------------------
    # * function String2ASCI(csp_text)
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

    return csp_text.replace('ñ','n').replace('Ñ','N').replace('ç','c').replace('Ç','C').replace('Á','A').replace('À','A').replace('Ä','A').replace('Â','A').replace('á','a').replace('à','a').replace('ä','a').replace('â','a').replace('É','E').replace('È','E').replace('Ë','E').replace('Ê','E').replace('é','e').replace('è','e').replace('ë','e').replace('ê','e').replace('Í','I').replace('Ì','I').replace('Ï','I').replace('Î','I').replace('í','i').replace('ì','i').replace('ï','i').replace('î','i').replace('Ó','O').replace('Ò','O').replace('Ö','O').replace('Ô','O').replace('ó','o').replace('ò','o').replace('ö','o').replace('ô','o').replace('Ú','U').replace('Ù','U').replace('Ü','U').replace('Û','U').replace('ú','u').replace('ù','u').replace('ü','u').replace('û','u')

def Add(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Add(logger,csp_soap_client,cucm_variable_axl)
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

    # Mandatory (pattern,usage)
    logger.debug('Se ha entrado en la funcion Add del archivo cspaxl_Line.py')
    axl_cucm_Line = {}
    axl_cucm_Line['pattern'] = cucm_variable_axl['DirectoryNumber']
    axl_cucm_Line['usage'] = 'Device'
    if cucm_variable_axl['CallPickupGroup'] == '':
        axl_cucm_Line['callPickupGroupName'] = ''
    else:
        axl_cucm_Line['callPickupGroupName'] = 'CPG_' + cucm_variable_axl['Country'] + '_' + cucm_variable_axl[
            'SiteCode'] + '_' + cucm_variable_axl['CallPickupGroup']
    axl_cucm_Line['routePartitionName'] = cucm_variable_axl['Partition']
    axl_cucm_Line['description'] = cucm_variable_axl['DirectoryNumber'] + ' - ' + cucm_variable_axl['FirstName'] + ' ' + cucm_variable_axl['Surname']
    axl_cucm_Line['alertingName'] = cucm_variable_axl['FirstName'] + ' ' + cucm_variable_axl['Surname']
    axl_cucm_Line['asciiAlertingName'] = String2ASCI(logger,axl_cucm_Line['alertingName'])

    #
    if cucm_variable_axl['VoiceMail'] == 'YES':
        axl_cucm_Line['voiceMailProfileName'] = 'VoiceMail'
    else:
        axl_cucm_Line['voiceMailProfileName'] = 'NoVoiceMail'
    # Rellenamos todos los Permisos para los desvios
    axl_cucm_Line['shareLineAppearanceCssName'] = cucm_variable_axl['CSS']
    axl_cucm_Line['callForwardAll'] = {'destination': '',
                                       'forwardToVoiceMail': 'false',
                                       'callingSearchSpaceName': cucm_variable_axl['CSSForward'],
                                       'secondaryCallingSearchSpaceName': cucm_variable_axl['CSSForward']}
    axl_cucm_Line['callForwardBusy'] = {'destination': '',
                                       'forwardToVoiceMail': 'false',
                                       'callingSearchSpaceName': cucm_variable_axl['CSSForward']}
    axl_cucm_Line['callForwardBusyInt'] = axl_cucm_Line['callForwardBusy']
    axl_cucm_Line['callForwardNoAnswer'] = axl_cucm_Line['callForwardBusy']
    axl_cucm_Line['callForwardNoAnswerInt'] = axl_cucm_Line['callForwardBusy']
    axl_cucm_Line['callForwardNoCoverage'] = axl_cucm_Line['callForwardBusy']
    axl_cucm_Line['callForwardNoCoverageInt'] = axl_cucm_Line['callForwardBusy']
    axl_cucm_Line['callForwardOnFailure'] = axl_cucm_Line['callForwardBusy']
    axl_cucm_Line['callForwardNotRegistered'] = axl_cucm_Line['callForwardBusy']
    axl_cucm_Line['callForwardNotRegisteredInt'] = axl_cucm_Line['callForwardBusy']

    # Limitamos el numero de caracteres de las variables
    axl_cucm_Line['alertingName'] = axl_cucm_Line['alertingName'][:50]
    axl_cucm_Line['asciiAlertingName'] = axl_cucm_Line['asciiAlertingName'][:32]
    #axl_cucm_Line['parkMonForwardNoRetrieveDn'] = axl_cucm_Line['parkMonForwardNoRetrieveDn'][:50]
    #axl_cucm_Line['parkMonForwardNoRetrieveIntDn'] = axl_cucm_Line['parkMonForwardNoRetrieveIntDn'][:50]

    # Comprobamos que la extension no existe
    try:
        csp_soap_returnedTags = {'pattern': '', 'routePartitionName': '', 'description': '', 'shareLineAppearanceCssName': ''}
        csp_soap_searchCriteria = {'pattern': cucm_variable_axl['DirectoryNumber'],'routePartitionName':cucm_variable_axl['Partition']}
        result = csp_soap_client.service.listLine(csp_soap_searchCriteria,csp_soap_returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': result}

    else:
        if (len(result['return']) == 0):
            logger.info('La extension %s no existe en el CUCM' % (cucm_variable_axl['DirectoryNumber']))
        else:
            logger.info('La extension %s existe en el CUCM' % (cucm_variable_axl['DirectoryNumber']))
            return {'Status': False, 'Detail': cucm_variable_axl['DirectoryNumber']}
    # Damos de alta la Linea
    try:
        result = csp_soap_client.service.addLine(axl_cucm_Line)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['UUID','pattern','routePartitionName'])
        csp_table.add_row([result['return'][:], axl_cucm_Line['pattern'], axl_cucm_Line['routePartitionName']])
        csp_table_response = csp_table.get_string(fields=['UUID', 'pattern', 'routePartitionName'],
                                                  sortby="UUID").encode('latin-1')
        return {'Status': True,'Detail':csp_table_response}
'''
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
    try:
        result = csp_soap_client.service.getProcessNode(name=cucm_variable_axl)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'])
        csp_table.add_row([0,result['return']['processNode']['name'],result['return']['processNode']['description'],result['return']['processNode']['mac'],result['return']['processNode']['ipv6Name'],result['return']['processNode']['nodeUsage'],result['return']['processNode']['lbmHubGroup'],result['return']['processNode']['processNodeRole'] ])
        csp_table_response = csp_table.get_string(fields=['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'], sortby="id").encode('latin-1')
        return {'Status':True,'Detail':csp_table_response}

def List(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function List(logger,csp_soap_client,cucm_variable_axl)
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
    returnedTags = {'name':'','description':'','mac':'','ipv6Name':'','nodeUsage':'','lbmHubGroup':'','processNodeRole':''}
    searchCriteria = {'name': '%' + cucm_variable_axl + '%'}

    try:
        result = csp_soap_client.service.listProcessNode(searchCriteria,returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'])
        for x in range(0, len(result['return']['processNode'])):
            csp_table.add_row([x,result['return']['processNode'][x]['name'],result['return']['processNode'][x]['description'],result['return']['processNode'][x]['mac'],result['return']['processNode'][x]['ipv6Name'],result['return']['processNode'][x]['nodeUsage'],result['return']['processNode'][x]['lbmHubGroup'],result['return']['processNode'][x]['processNodeRole'] ])
        csp_table_response = csp_table.get_string(fields=['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'], sortby="id").encode('latin-1')
        return {'Status':True,'Detail':csp_table_response}

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