# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_DevicePool.py
# *
# * Cisco AXL Python
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

# Import Modules
# Import Modules
import sys
import os
from unittest.case import _AssertRaisesContext

import suds
import ssl

from prettytable import PrettyTable
#from configobj import ConfigObj
#from suds.client import Client

def Add(logger,csp_soap_client,cucm_variable_axl):
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
    logger.debug('Se ha entrado en la funcion Add del archivo cspaxl_DevicePool.py')
    axl_cucm = {}
    axl_cucm['name'] = 'DP_' + cucm_variable_axl['Country'] + '_' + cucm_variable_axl['SiteCode']
    axl_cucm['dateTimeSettingName'] = 'Device'
    
    # Limitamos el numero de caracteres de las variables
    axl_cucm['alertingName'] = axl_cucm['alertingName'][:50]
    axl_cucm['asciiAlertingName'] = axl_cucm['asciiAlertingName'][:32]
    #axl_cucm_Line['parkMonForwardNoRetrieveDn'] = axl_cucm_Line['parkMonForwardNoRetrieveDn'][:50]
    #axl_cucm_Line['parkMonForwardNoRetrieveIntDn'] = axl_cucm_Line['parkMonForwardNoRetrieveIntDn'][:50]

    # Comprobamos que la extension no existe
    try:
        csp_soap_returnedTags = {'pattern': '', 'routePartitionName': '', 'description': '', 'shareLineAppearanceCssName': ''}
        csp_soap_searchCriteria = {'pattern': cucm_variable_axl['DirectoryNumber'],'routePartitionName':'INTERNA'}
        result = csp_soap_client.service.listLine(csp_soap_searchCriteria,csp_soap_returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': result}

    else:
        if (len(result['return']) == 0):
            logger.info("La extension " + cucm_variable_axl['DirectoryNumber'] + " no existe en el CUCM")
        else:
            logger.error("La extension " + cucm_variable_axl['DirectoryNumber'] + " existe en el CUCM")
            return {'Status': False, 'Detail': cucm_variable_axl['DirectoryNumber']}
    # Damos de alta la L�nea
    try:
        result = csp_soap_client.service.addLine(axl_cucm)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['UUID','pattern','routePartitionName'])
        csp_table.add_row([result['return'][:], axl_cucm['pattern'], axl_cucm['routePartitionName']])
        csp_table_response = csp_table.get_string(fields=['UUID', 'pattern', 'routePartitionName'],
                                                  sortby="UUID").encode('latin-1')
        return {'Status':True,'Detail':csp_table_response}

def Get(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Get(logger,csp_soap_client,cucm_variable_axl)
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