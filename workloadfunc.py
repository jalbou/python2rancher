### Rancher Create workload from json workload template ###
#Module to manage https requests
import requests
import sys
import json
#Module to manage HTTPS python config
import urllib3
#Custom librarie to manage Minecraft workloads on a given k8s cluster managed by Rancher
import python2rancher as rancher
import python2nsx as nsx
import os
import time
import re
urllib3.disable_warnings()

####  Added temporary for testing purpose ####
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
###############################################

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
    isStorageClass = rancher.getStorageClass(RancherObj)
    workloads = rancher.getAllWorkloadName(RancherObj)
    #Get A list of actual workload matching the template workload requested using a regex filter
    regex = re.compile(RancherObj['workloadTemplate'])
    filteredList = list(filter(regex.match, workloads))
    if not filteredList:
        firstOccurence = 0
    else:
        filteredList.sort(reverse=True)
        firstOccurence =int(re.findall(r'\d', str(filteredList[0]))[0])
    if  isStorageClass == 404:
        print('Storage Class storageclass'+workloadName+' not found , creating ... ')
        rancher.setNewStorageClass(RancherObj)
    workload = workloadName+str(firstOccurence+1)
    rancher.setNewPVC(RancherObj,workload)
    newWorkload = rancher.setNewWorkload(RancherObj,workload)
    if newWorkload in (200,201,202):
        time.sleep(1)
        newWorkloadInfo = rancher.getWorkload(RancherObj,workload)
        #nsx.createPool(newWorkloadInfo.port)
        print("port "+newWorkloadInfo['port'])
        return newWorkloadInfo
    else:
        print("There was an issue during creation of "+workload)
        return "There was an issue during creation of "+workload
    
               
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

#rancher.getPersistantVolume(RancherObj,"volumeminecraft1")
