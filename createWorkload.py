### Rancher Create workload from json workload template ###
#Module to manage https requests
import requests
import sys
#Module to manage argument parsing
import argparse
import json
#Module to manage HTTPS python config
import urllib3
#Custom librarie to manage Minecraft workloads on a given k8s cluster managed by Rancher
import rancherFunctions as rancher
import os
urllib3.disable_warnings()
### Creating argument helper and positioner ### 
parser = argparse.ArgumentParser()
parser.add_argument("-w","--workloadName", type=str,
                    help="Name of the Workload template")
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
workloadTemplate = args.workloadName
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
    isWorkload = rancher.getWorkload(workloadName,rancherEndpoint,rancherProjectID,rancherAuth,rancherToken,headers)
    isStorageClass = rancher.getStorageClass(workloadName,rancherEndpoint,rancherClusterID,rancherAuth,rancherToken,headers)
    if  isWorkload == 404 or isStorageClass==404:
        if  isStorageClass == 404:
             print('Storage Class storageclass'+workloadName+' not found , creating ... ')
             rancher.setNewStorageClass(rancherEndpoint,rancherClusterID,rancherAuth,rancherToken,headers,workloadTemplate,workloadName)
        if  isWorkload == 404:
             print('Workload '+workloadName+' not found , creating ... ')
             rancher.setNewWorkload(workloadName,rancherProjectID,rancherEndpoint,rancherAuth,rancherToken,headers,workloadTemplate)
    else:
        print("Workload already existing. Escaping...")

#allworkloads = rancher.getAllWorkloadName(rancherEndpoint,rancherProjectID,rancherAuth,rancherToken,headers)
#allStorageClass = rancher.getAllStorageClass(rancherEndpoint,rancherClusterID,rancherAuth,rancherToken,headers)