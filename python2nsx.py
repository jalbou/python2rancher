import requests
import sys
import urllib3
import pathlib
import os
import xml.etree.ElementTree as ET

def createLoadBalancerPool(portnumber,poolname):
    XMLConfig = ET.parse('Templates/minecraft-NSXPool.xml')
    root = XMLConfig.getroot()
    name = root.find('name')
    name.text = poolname
    name.set('approved', 'yes')
    for port in root.findall('./member/port'): 
        new_port = portnumber
        port.text = new_port
        port.set('updated', 'yes')
    for monitorPort in root.findall('./member/monitorPort'): 
        new_monitorPort = portnumber
        monitorPort.text = new_monitorPort
        monitorPort.set('updated','yes')
    headers = {
        'Authorization': os.environ.get('NSXAuth'),
        'Postman-Token': os.environ.get('NSXToken'),
        'Accept': "application/xml",
        'Content-Type': "text/xml",  
        'Host': "nsx2.chamaa.local",
        'accept-encoding': "gzip, deflate",
        'cache-control': "no-cache" 
    }

    url = "https://nsx2.chamaa.local/api/4.0/edges/edge-20/loadbalancer/config/pools/"
    #print("port "+port)
    print("poolname "+poolname)
    payload = ET.tostring(root)
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    print(payload)
    print(response.content)
    
def createNATRule(portnumber,natRuleName):
    XMLConfig = ET.parse('Templates/minecraft-NSXNAT.xml')
    root = XMLConfig.getroot()
    for nat in root.findall('./natRule/description'):
        nat.text = natRuleName
        nat.set('updated', 'yes')
    for originalPort in root.findall('./natRule/originalPort'):
        originalPort.text = portnumber
        originalPort.set('updated', 'yes')
    for translatedPort in root.findall('./natRule/translatedPort'):
        translatedPort.text = portnumber
        translatedPort.set('updated', 'yes')
    headers = {
        'Authorization': os.environ.get('NSXAuth'),
        'Postman-Token': os.environ.get('NSXToken'),
        'Accept': "application/xml",
        'Content-Type': "text/xml",  
        'Host': "nsx2.chamaa.local",
        'accept-encoding': "gzip, deflate",
        'cache-control': "no-cache" 
    }
    url = "https://nsx2.chamaa.local/api/4.0/edges/edge-20/nat/config/rules"
   
    print("NAT Rule Name "+natRuleName)
    payload = ET.tostring(root)
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    print(payload)
    print(response.content)