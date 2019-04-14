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
import python2rancher as rancher
import os
import re
urllib3.disable_warnings()
### Creating argument helper and positioner ### 
parser = argparse.ArgumentParser()
parser.add_argument("-w","--workloadName", type=str,
                    help="Name of the Workload template")
parser.add_argument("-c", "--count", type=int,
                    help="Number of desired deployments")
parser.add_argument("-p", "--projectID", type=str,
                    help="Project ID Number")
parser.add_argument("-d", "--destroy", type=bool,
                    help="Project ID Number")      
args = parser.parse_args()
#Get Rancher API cred from system variable enviroments
headers = {
    'Content-Type': "application/json",
    'Authorization': os.environ.get('RancherAuth'),
    'cache-control': "no-cache",
    'Postman-Token': os.environ.get('RancherToken')
}
RancherObj =  {
    'rancherEndpoint':os.environ.get('RancherEndpoint'),
    'rancherClusterID':os.environ.get('RancherClusterID'),
    'rancherProjectID':os.environ.get('RancherProjectID'),
    'workloadTemplate':args.workloadName,
    'headers': headers
}
count = args.count
#Set HTTP Header for Rancher API Calls
if str(args.destroy) == "None":
    i=0
    #Get A list of actual workload matching the template workload requested using a regex filter
    workloads = rancher.getAllWorkloadName(RancherObj)
    regex = re.compile(RancherObj['workloadTemplate'])
    filteredList = list(filter(regex.match, workloads))
    filteredList.sort(reverse=True)
    if not filteredList:
        firstOccurence = 0
    else:
        firstOccurence =int(re.findall(r'\d', str(filteredList[0]))[0])
        print(firstOccurence)
    while i < count:
        i += 1
        workloadName = args.workloadName+str(firstOccurence+i)
        isWorkload = rancher.getWorkload(RancherObj,workloadName)
        isStorageClass = rancher.getStorageClass(RancherObj)
        if isWorkload == 404 or isStorageClass==404:
            if  isStorageClass == 404:
                print('Storage Class storageclass'+workloadName+' not found , creating ... ')
                rancher.setNewStorageClass(RancherObj)
            if  isWorkload == 404:
                print('Workload '+workloadName+' not found , creating ... ')
                rancher.setNewPVC(RancherObj,workloadName)
                rancher.setNewWorkload(RancherObj,workloadName)
        else:
            print("Workload "+workloadName+" already existing. Escaping...")
else :
    
    workloadName = args.workloadName
    rancher.setNewWorkload(RancherObj,workloadName)
    # rancher.removeStorageClass(workloadName,rancherEndpoint,rancherClusterID,rancherAuth,rancherToken,headers)
    # rancher.removeWorkload(workloadName,rancherEndpoint,rancherProjectID,rancherAuth,rancherToken,headers)

#allworkloads = rancher.getAllWorkloadName(rancherEndpoint,rancherProjectID,rancherAuth,rancherToken,headers)
#allStorageClass = rancher.getAllStorageClass(rancherEndpoint,rancherClusterID,rancherAuth,rancherToken,headers)