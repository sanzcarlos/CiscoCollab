# -*- coding: iso-8859-15 -*-
#
# *------------------------------------------------------------------
# * cucm_axl_Version.py
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
import sys

def Get(logger,csp_soap_client,cucm_variable_axl):
    # *------------------------------------------------------------------
    # * function Get(logger,csp_soap_client,cucm_variable_axl)
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


    #sys.tracebacklimit = 0
    # Mandatory (processNodeName)
    try:
        result = csp_soap_client.service.getCCMVersion(processNodeName=cucm_variable_axl)
    except:
        logger.debug(sys.exc_info())
        logger.error(sys.exc_info()[1])
        return {'Status':False,'Detail':sys.exc_info()[1]}
    else:
        '''
        print result

        (reply){
           return =
              (return){
                 componentVersion =
                    (componentVersion){
                       version = "8.6.2.25900(8)"
                    }
              }
         }

        print result['return']['componentVersion'].version

        8.6.2.25900(8)
        '''
        return {'Status':True,'Detail':result['return']['componentVersion'].version}