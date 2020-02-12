# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_User.py
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
    # Damos de alta un Usuario
    logger.debug('Se ha entrado en la funcion Add del archivo cspaxl_User.py')
    axl_cucm_EndUser = {}
    axl_cucm_EndUser['userid'] = cucm_variable_axl['userPrincipalName']
    axl_cucm_EndUser['selfService'] = cucm_variable_axl['DirectoryNumber']    
    axl_cucm_EndUser['attendeesAccessCode'] = cucm_variable_axl['DirectoryNumber']  
    axl_cucm_EndUser['enableUserToHostConferenceNow'] = 'true'
    axl_cucm_EndUser['associatedGroups'] = cucm_variable_axl['Customer'].upper() + '_EndUser'
    axl_cucm_EndUser['firstName'] = cucm_variable_axl['FirstName']
    if cucm_variable_axl['Surname'] == '':
        axl_cucm_EndUser['lastName'] = cucm_variable_axl['DirectoryNumber']
    else:
        axl_cucm_EndUser['lastName'] = cucm_variable_axl['Surname']
    axl_cucm_EndUser['password'] = cucm_variable_axl['userPrincipalName']
    axl_cucm_EndUser['pin'] = '123456'
    axl_cucm_EndUser['digestCredentials'] = cucm_variable_axl['userPrincipalName']
    axl_cucm_EndUser['telephoneNumber'] = cucm_variable_axl['DirectoryNumber']

    logger.info('El Usuario que se quiere dar de alta es: %s' % (axl_cucm_EndUser['userid']))

    # Comprobamos que el Usuario no existe
    try:
        csp_soap_returnedTags = {'userid':''}
        csp_soap_searchCriteria = {'userid': axl_cucm_EndUser['userid']}
        result = csp_soap_client.service.listUser(csp_soap_searchCriteria,csp_soap_returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        if (len(result['return']) == 0):
            logger.info('El Usuario %s no existe en el CUCM' % (axl_cucm_EndUser['userid']))
        else:
            logger.info('El Usuario %s existe en el CUCM' % (axl_cucm_EndUser['userid']))
            return {'Status': False, 'Detail': axl_cucm_EndUser['userid']}

    # Damos de alta el Usuario
    try:
        result = csp_soap_client.service.addUser(axl_cucm_EndUser)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['UUID','userid','firstName'])
        csp_table.add_row([result['return'][:],axl_cucm_EndUser['userid'], axl_cucm_EndUser['firstName'] ])
        csp_table_response = csp_table.get_string(fields=['UUID','userid','firstName'], sortby="UUID").encode('latin-1')
        return {'Status': True,'Detail':csp_table_response}

    '''
    try:
        result = csp_soap_client.service.addUser(axl_cucm_Line)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        csp_table = PrettyTable(['UUID','pattern','routePartitionName'])
        csp_table.add_row([result['return'][:], axl_cucm_Line['pattern'], axl_cucm_Line['routePartitionName']])
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
    # returnedTags = {'userid':''}
    # searchCriteria = {'userid': 'carlos.sanz'}
    try:
        logger.info(cucm_variable_axl)
        result = csp_soap_client.service.getUser('2477')
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        #csp_table = PrettyTable(['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'])
        #csp_table.add_row([0,result['return']['processNode']['name'],result['return']['processNode']['description'],result['return']['processNode']['mac'],result['return']['processNode']['ipv6Name'],result['return']['processNode']['nodeUsage'],result['return']['processNode']['lbmHubGroup'],result['return']['processNode']['processNodeRole'] ])
        #csp_table_response = csp_table.get_string(fields=['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'], sortby="id").encode('latin-1')
        print (result)
        csp_table_response = result['return']
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
    returnedTags = {'userid':'','associatedDevices':''}
    searchCriteria = {'userid': '%' + cucm_variable_axl + '%'}

    try:
        result = csp_soap_client.service.listUser(searchCriteria,returnedTags)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status': False, 'Detail': sys.exc_info()[1]}
    else:
        #csp_table = PrettyTable(['userid':'','associatedDevices':'','primaryExtension':'','ipccExtension':''])
        #for x in range(0, len(result['return']['processNode'])):
        #    csp_table.add_row([x,result['return']['processNode'][x]['name'],result['return']['processNode'][x]['description'],result['return']['processNode'][x]['mac'],result['return']['processNode'][x]['ipv6Name'],result['return']['processNode'][x]['nodeUsage'],result['return']['processNode'][x]['lbmHubGroup'],result['return']['processNode'][x]['processNodeRole'] ])
        #csp_table_response = csp_table.get_string(fields=['id','name','description','mac','ipv6Name','nodeUsage','lbmHubGroup','processNodeRole'], sortby="id").encode('latin-1')
        logger.info (result)
        csp_table_response = result
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