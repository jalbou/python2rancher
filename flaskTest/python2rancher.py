import requests
import sys
import json
import urllib3
import pathlib

## This function is used to create a new workload on a specific k8s cluster and assign it a new dynamic storage class for a given workload template
def setNewWorkload(RancherObj,workloadName):
    url = 'https://'+RancherObj['rancherEndpoint']+'/v3/project/'+RancherObj['rancherProjectID']+'/workloads'
    # Read new Workload JSON config file
    workloadTemplatePath = 'Templates/'+RancherObj['workloadTemplate']+'.json'
    with open(workloadTemplatePath, 'r') as f:
        rawJSON = json.load(f)
    #Set JSON config file according workload arguments
    rawJSON['containers'][0]['name'] = workloadName
    rawJSON['containers'][0]['ports'][0]['dnsName'] = workloadName+'-nodeport'
    rawJSON['selector']['matchLabels']['workload.user.cattle.io/workloadselector'] = "statefulSet-default-"+workloadName
    rawJSON['name']= workloadName
    rawJSON['workloadLabels']['workload.user.cattle.io/workloadselector'] = 'statefulSet-default-'+workloadName
    rawJSON['labels']['workload.user.cattle.io/workloadselector'] = 'statefulSet-default-'+workloadName
    rawJSON['workload.user.cattle.io/workloadselector'] = 'statefulSet-default-'+workloadName
    rawJSON['statefulSetConfig']['serviceName'] = workloadName
    rawJSON['volumes'][0]['name'] = 'volume'+workloadName
    rawJSON['volumes'][0]['persistentVolumeClaim']['persistentVolumeClaimId'] = 'default:volume'+workloadName
    rawJSON['projectId'] = RancherObj['rancherProjectID']
    payload=json.dumps(rawJSON, indent=4, sort_keys=True)
    response = requests.request("POST",url, data=payload, headers=RancherObj['headers'],verify=False)
#Error Handling here

## This function is used to create a new Persitant Volume claim on a given storage class
def setNewPVC(RancherObj,workloadName):
    url = 'https://'+RancherObj['rancherEndpoint']+'/v3/project/'+RancherObj['rancherProjectID']+'/persistentvolumeclaims' 
    # Read new Workload JSON config file
    workloadTemplatePath = 'Templates/'+RancherObj['workloadTemplate']+'-PVC.json'
    with open(workloadTemplatePath, 'r') as f:
        rawJSON = json.load(f)
    rawJSON['name'] = 'volume'+workloadName
    rawJSON['projectId'] = RancherObj['rancherProjectID']
    rawJSON['storageClassId'] = 'storageclass'+RancherObj['workloadTemplate']
    payload=json.dumps(rawJSON, indent=4, sort_keys=True)
    response = requests.request("POST",url, data=payload, headers=RancherObj['headers'],verify=False)
#Error Handling here

## This function is used to create a storage class for a specific k8s cluster
def setNewStorageClass(RancherObj):
    url = 'https://'+RancherObj['rancherEndpoint']+'/v3/cluster/'+RancherObj['rancherClusterID']+'/storageClasses/'
    print('url : '+url)
    # Read new Workload JSON config file
    storageClassTemplatePath = 'Templates/'+RancherObj['workloadTemplate']+'-storageclass.json'
    with open(storageClassTemplatePath, 'r') as f:
        rawJSON = json.load(f)
    #Set JSON config file according workload arguments
    rawJSON['name'] = 'storageclass'+RancherObj['workloadTemplate']
    payload=json.dumps(rawJSON, indent=4, sort_keys=True)
    response = requests.request("POST",url, data=payload, headers=RancherObj['headers'],verify=False)
    print(response.content)

## This function is used to fetch a workload by his name, return 404 if any ressource was found and 202 if something exist
def getWorkload(RancherObj,workloadName):
    url = 'https://'+RancherObj['rancherEndpoint']+'/v3/project/'+RancherObj['rancherProjectID']+'/workloads/statefulset:default:'+workloadName
    payload = ""
    response = requests.get(url, data=payload, headers=RancherObj['headers'] ,verify=False)
    return response.status_code

## This function is used to fetch a storage class by his name, return 404 if any ressource was found and 202 if something exist
def getStorageClass(RancherObj):
    url = 'https://'+RancherObj['rancherEndpoint']+'/v3/cluster/'+RancherObj['rancherClusterID']+'/storageClasses/storageclass'+RancherObj['workloadTemplate']
    payload = ""
    response = requests.get(url, data=payload, headers=RancherObj['headers'] ,verify=False)
    return response.status_code

## This function is used to fetch all storage classes for a given cluster name return an JSON object containing basic storage infos
def getAllStorageClass(RancherObj):
    url = 'https://'+RancherObj['rancherEndpoint']+'/v3/cluster/'+RancherObj['rancherClusterID']+'/storageClasses'
    payload = ""
    response = requests.get(url, data=payload, headers=RancherObj['headers'] ,verify=False)
    content = response.content
    workloadList = json.loads(content)
    result=[]
    for storageClass in workloadList['data']:
        result.append(storageClass['id'])
    return result

## This function is used to fetch all workloads for a given workload name return an JSON object containing basic workload infos
def getAllWorkloadName(RancherObj):
    url = 'https://'+RancherObj['rancherEndpoint']+'/v3/project/'+RancherObj['rancherProjectID']+'/workloads/'
    payload = ""
    response = requests.get(url, data=payload, headers=RancherObj['headers'] ,verify=False)
    content = response.content
    workloadList = json.loads(content)
    result=[]
    for container in workloadList['data']:
        for name in container['containers']:
            result.append(name['name'])
    return result

## This function is used to delete a workload by his name, return 404 if any ressource was found and 204 was deleted
def removeWorkload(RancherObj,workloadName):
    isWorkload = getWorkload(RancherObj,workloadName)
    if isWorkload == 404:
        print('Workload '+workloadName+' does not exist')
        return isWorkload
    else:
        url = 'https://'+RancherObj['rancherEndpoint']+'/v3/project/'+RancherObj['rancherProjectID']+'/workloads/statefulset:default:'+workloadName
        response = requests.delete(url,headers=RancherObj['headers'] ,verify=False)
        status_code = response.status_code
        return status_code
    
## This function is used to delete a storage class by his name, return 404 if any ressource was found and 204 was deleted
def removeStorageClass(RancherObj):
    isStorageClass = getStorageClass(RancherObj)
    if isStorageClass == 404:
        print('StorageClass '+RancherObj['workloadTemplate']+' does not exist')
        return isStorageClass
    else:
        url = 'https://'+RancherObj['rancherEndpoint']+'/v3/cluster/'+RancherObj['rancherClusterID']+'/storageClasses/storageclass'+RancherObj['workloadTemplate']
        response = requests.request("DELETE",url,headers=RancherObj['headers'] ,verify=False)
        status_code = response.status_code
        return status_code
