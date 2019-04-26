### Rancher Create workload from json workload template ###
#Module to manage https requests
import requests
import sys
import json
#Module to manage HTTPS python config
import urllib3
#Custom librarie to manage Minecraft workloads on a given k8s cluster managed by Rancher
import python2rancher as rancher
import os
import re
urllib3.disable_warnings()
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
    'headers': headers
}
       #Set HTTP Header for Rancher API Calls
def create(workloadName):
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
        'workloadTemplate':workloadName,
        'headers': headers
    }
    #Set HTTP Header for Rancher API Calls
    #Get A list of actual workload matching the template workload requested using a regex filter
    workloads = rancher.getAllWorkloadName(RancherObj)
    regex = re.compile(RancherObj['workloadTemplate'])
    filteredList = list(filter(regex.match, workloads))
    filteredList.sort(reverse=True)
    if not filteredList:
        firstOccurence = 0
    else:
        firstOccurence =int(re.findall(r'\d', str(filteredList[0]))[0])
    workload = workloadName+str(firstOccurence+1)
    isWorkload = rancher.getWorkload(RancherObj,workload)
    isStorageClass = rancher.getStorageClass(RancherObj)
    if isWorkload == 404 or isStorageClass==404:
        if  isStorageClass == 404:
            print('Storage Class storageclass'+workloadName+' not found , creating ... ')
            rancher.setNewStorageClass(RancherObj)
        if  isWorkload == 404:
            print('Workload '+workload+' not found , creating ... ')
            rancher.setNewPVC(RancherObj,workload)
            rancher.setNewWorkload(RancherObj,workload)
            newWorkload = rancher.getWorkload(RancherObj,workload)
            return workloadName+"created, the service is available on "+(str(json.loads(newWorkload.content)))
        else:
            print("Workload "+workload+" already existing. Escaping...")
                
def remove(workloadName):
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
        'workloadTemplate':workloadName,
        'headers': headers
    }
       #Set HTTP Header for Rancher API Calls
    return rancher.removeWorkload(RancherObj,workloadName)

rancher.getWorkload(RancherObj,'web1')

def get(workloadName):
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
        'workloadTemplate':workloadName,
        'headers': headers
    }
       #Set HTTP Header for Rancher API Calls
    return rancher.getWorkload(RancherObj,workloadName)
    