### Minecraft to rancher/k8s workload & storage class management functions by Jeremy Albou ### 
#Module to manage https requests
import requests
import sys
#Module to manage argument parsing
import argparse
import json
#Module to manage HTTPS python config
import urllib3
#Custom librarie to manage Minecraft workloads on a given k8s cluster managed by Rancher
import minecraftk8s as minecraftk8s
import os
urllib3.disable_warnings()
### Creating argument helper and positioner ### 
parser = argparse.ArgumentParser()
parser.add_argument("-w","--workloadName", type=str,
                    help="Name of the Workload")
parser.add_argument("-c", "--count", type=int,
                    help="Number of desired deployments")
parser.add_argument("-p", "--projectID", type=str,
                    help="Project ID Number")     
args = parser.parse_args()
#Get Rancher API cred from system variable enviroments
rancherAuth = os.environ.get('RancherAuth')
rancherToken = os.environ.get('RancherToken')
rancherEndpoint= os.environ.get('RancherEndpoint')
rancherClusterID = os.environ.get('RancherClusterID')
rancherProjectID = os.environ.get('RancherProjectID')
count = args.count
#Set HTTP Header for Rancher API Calls
headers = {
    'Content-Type': "application/json",
    'Authorization': rancherAuth,
    'cache-control': "no-cache",
    'Postman-Token': rancherToken
}
i=0
while i < count:
    i += 1
    workloadName = args.workloadName+str(i)
    isWorkload = minecraftk8s.getWorkload(workloadName,rancherEndpoint,rancherProjectID,rancherAuth,rancherToken,headers)
    isStorageClass = minecraftk8s.getStorageClass(workloadName,rancherEndpoint,rancherClusterID,rancherAuth,rancherToken,headers)
    isWorkLoadJSON = json.loads(isWorkload)
    isWorkLoadJSONBaseType= isWorkLoadJSON["baseType"]
    isStorageClassJSON=json.loads(isStorageCLass)
    isStorageClassJSONBaseType=  isStorageClassJSON["baseType"]
    if isWorkLoadJSONBaseType == "error":
        print("Status found:"+isWorkLoadJSONBaseType)
        print("No workload existing for "+workloadName)
        minecraftk8s.setNewWorkload(workloadName,rancherProjectID,rancherEndpoint,rancherAuth,rancherToken)
    else:
        print("Status found :"+isWorkLoadJSONBaseType)
        print("Workload existing for "+workloadName)