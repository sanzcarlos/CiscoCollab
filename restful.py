#import requests
import json
import xml

#from requests.auth import HTTPBasicAuth
#from xmlutils.xml2json import xml2json

#url = 'http://10.160.82.156/adminapi/resource/carlos.sanz'

#url = 'http://10.160.82.156/adminapi/agentstats'
#url = 'http://10.160.82.156/adminapi/application'
#url = 'http://10.160.82.156/adminapi/areaCode'
#url = 'http://10.160.82.156/adminapi/callControlGroup'

#username = 'appuccx'
#password = 'COL4pp11uccx%11'

#r = requests.get(url, auth=HTTPBasicAuth(username, password))
'''
try:
    csp_xml_filename = 'csv/uccxapi.xml'
    csp_xml_file = open(csp_xml_filename, 'w')
except:
    sys.exit()
else:
    print r.content
    print ("\n")
    csp_xml_file.write(r.content)
    csp_xml_file.close()

    converter = xml2json(csp_xml_filename, encoding="utf-8")

    # Creamos una variable (tipo dict) con los datos xml
    temp = json.loads(converter.get_json())

    print temp
'''
#axl_cucm_Line = 'Carlos Sanz Penas - Es una persona de Acuntia y no tiene que configurar el CUCM'
#print axl_cucm_Line
#axl_cucm_Line = axl_cucm_Line[:50]
#print axl_cucm_Line

import requests
import os
import logging
import ssl
from suds.cache import NoCache

ssl._create_default_https_context = ssl._create_unverified_context
logging.getLogger('suds.client').setLevel(logging.DEBUG)

wsdl = 'file:///' + os.getcwd().replace ("\\","//") + '//Schema//CUCM//11.5//AXLAPI.wsdl'
csp_location = 'https://10.160.82.152:8443/axl/'
csp_username = 'appcucm'
csp_password = 'COL4pp11cucm%11'

xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/10.5">
  <soapenv:Header/>
    <soapenv:Body>
      <ns:getUser>
        <userid>carlos.sanz </userid>
      </ns:getUser>
    </soapenv:Body>
  </soapenv:Envelope>"""
headers = {'Content-Type': 'text/xml',
           'SOAPAction': '"CUCM:DB ver=10.5 getUSer"'}
req=requests.post('https://10.160.82.152:8443/axl/', auth=(csp_username,csp_password), data=xml, headers=headers, verify=False)

print (req)