import requests
import sys
import urllib3
import pathlib
import os
import xml.etree.ElementTree as ET
def createLoadBalancerPool(port,poolName,NSXObj):
    XMLConfig = ET.parse('Templates/minecraft-NSX.xml')
    root = XMLConfig.getroot()
    name = root.find('name')
    name.text = poolName
    name.set('approved', 'yes')
    for port in root.findall('./member/port'): 
        new_port = port
        port.text = new_port
        port.set('updated', 'yes')
    for monitorPort in root.findall('./member/monitorPort'): 
        new_monitorPort = port
        monitorPort.text = new_monitorPort
        monitorPort.set('updated','yes')
    headers = {
        #'Authorization': os.environ.get('NSXAuth'),
        #'Postman-Token': os.environ.get('NSXToken'),
        'Postman-Token': "9fa28756-13f7-4e74-911e-c81b9f1ce4ae,56751d0f-4037-4117-9c8e-6dc4d31446bd",
        'Authorization': "Basic Y2hhbWFhXHN2Yy1uc3gtbGRwOkluZnJhMjAxOSEwMSE=",
        'Accept': "application/xml",
        'Content-Type': "text/xml",  
        'Host': "nsx2.chamaa.local",
        'accept-encoding': "gzip, deflate",
        'cache-control': "no-cache" 
    }

    url = "https://nsx2.chamaa.local/api/4.0/edges/edge-20/loadbalancer/config/pools/"

    payload = ET.tostring(root)
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    print(response.content)
