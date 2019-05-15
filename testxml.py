import xml.etree.ElementTree as ET
import pathlib
import os
XMLConfig = ET.parse('Templates/minecraft-NSX.xml')
root = XMLConfig.getroot()
print(root.findall("./member/port"))
for port in root.findall('./member/port'): 
    new_port = "6000"
    port.text = new_port
    port.set('updated', 'yes')
    print(port.text)

print(ET.tostring(root))