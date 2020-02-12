# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_CallingPartyTransformationPattern.py
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
    logger.debug('Se ha entrado en la funcion Add del archivo cspaxl_CallingPartyTransformationPattern.py')
    axl_cucm = {}
    axl_cucm['pattern'] = cucm_variable_axl['Pattern']
    axl_cucm['routePartitionName'] = cucm_variable_axl['Partition']
    axl_cucm['description'] = cucm_variable_axl['Pattern'] + ' - ' + cucm_variable_axl['callingPartyTransformationMask']
    axl_cucm['callingPartyTransformationMask'] = cucm_variable_axl['callingPartyTransformationMask']
    
    # Comprobamos que el Calling Party Transformation Pattern no existe
    try:
        csp_soap_returnedTags = {'pattern': '', 'routePartitionName': ''}
        csp_soap_searchCriteria = {'pattern': cucm_variable_axl['Pattern'],'routePartitionName':cucm_variable_axl['Partition']}
        result = csp_soap_client.service.listCallingPartyTransformationPattern(csp_soap_searchCriteria,csp_soap_returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': result}
    else:
        if (len(result['return']) == 0):
            logger.info('El Calling Party Transformation Pattern: %s en la Partition %s no existe en el CUCM' % (cucm_variable_axl['Pattern'],cucm_variable_axl['Partition']))
        else:
            logger.error('El Calling Party Transformation Pattern: %s en la Partition %s existe en el CUCM' % (cucm_variable_axl['Pattern'],cucm_variable_axl['Partition']))
            return {'Status': False, 'Detail': cucm_variable_axl['Pattern']}
    # Damos de alta el Calling Party Transformation Pattern
    try:
        result = csp_soap_client.service.addCallingPartyTransformationPattern(axl_cucm)
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

'''
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
'''

'''
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