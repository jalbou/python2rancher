import requests
import sys
import urllib3
import pathlib
import os
import xml.etree.ElementTree as ET
def createPool():
    XMLConfig = ET.parse('Templates/minecraft-NSX.xml')
    root = XMLConfig.getroot()
    name = root.find('name')
    name.text = "LBTEST1"
    name.set('approved', 'yes')
    for port in root.findall('./member/port'): 
        new_port = "6000"
        port.text = new_port
        port.set('updated', 'yes')
    for monitorPort in root.findall('./member/monitorPort'): 
        new_monitorPort = "6000"
        monitorPort.text = new_monitorPort
        monitorPort.set('updated','yes')
    headers = {
        #'Authorization': os.environ.get('NSXAuth'),
        #'Postman-Token': os.environ.get('NSXToken'),
        'Postman-Token': "9fa28756-13f7-4e74-911e-c81b9f1ce4ae,56751d0f-4037-4117-9c8e-6dc4d31446bd",
        'Authorization': "Basic Y2hhbWFhXHN2Yy1uc3gtbGRwOkluZnJhMjAxOSEwMSE=",
        'Accept': "application/xml",
        'Content-Type': "text/xml",
        'User-Agent': "PostmanRuntime/7.11.0",       
        'Host': "nsx2.chamaa.local",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache" 
    }

    url = "https://nsx2.chamaa.local/api/4.0/edges/edge-20/loadbalancer/config/pools/"

    payload = ET.tostring(root)
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    print(response.content)
    
    
createPool()
