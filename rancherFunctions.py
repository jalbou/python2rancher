import requests
import sys
import json
import urllib3
import pathlib

## This function is used to create a new workload on a specific k8s cluster and assign it a new dynamic storage class for a given workload template
def setNewWorkload(workloadName,rancherProjectID,rancherEndpoint,rancherAuth,rancherToken,headers,workloadTemplate):
    url = "https://"+rancherEndpoint+"/v3/project/"+rancherProjectID+"/workloads"
    # Read new Workload JSON config file
    workloadTemplatePath = 'Templates/'+workloadTemplate+'.json'
    print(workloadTemplatePath)
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
    rawJSON['projectId'] = rancherProjectID
    payload=json.dumps(rawJSON, indent=4, sort_keys=True)
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
#Error Handling here

## This function is used to create a new workload on a specific k8s cluster and assign it a new dynamic storage class for a given workload template
def setNewStorageClass(rancherEndpoint,rancherClusterID,rancherAuth,rancherToken,headers,workloadTemplate,workloadName):
    url = 'https://'+rancherEndpoint+'/v3/cluster/'+rancherClusterID+'/storageClasses/'
    # Read new Workload JSON config file
    storageClassTemplatePath = 'Templates/'+workloadTemplate+'-storageclass.json'
    print(storageClassTemplatePath)
    with open(storageClassTemplatePath, 'r') as f:
        rawJSON = json.load(f)
    #Set JSON config file according workload arguments
    rawJSON['name'] = 'storageclass'+workloadName
    payload=json.dumps(rawJSON, indent=4, sort_keys=True)
    response = requests.post(url, data=payload, headers=headers,verify=False)

## This function is used to fetch a workload by his name, return 404 if any ressource was found and 202 if something exist
def getWorkload(workloadName,rancherEndpoint,rancherProjectID,rancherAuth,rancherToken,headers):
    url = 'https://'+rancherEndpoint+'/v3/project/'+rancherProjectID+'/workloads/statefulset:default:'+workloadName
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers ,verify=False)
    return response.status_code

## This function is used to fetch a storage class by his name, return 404 if any ressource was found and 202 if something exist
def getStorageClass(workloadName,rancherEndpoint,rancherClusterID,rancherAuth,rancherToken,headers):
    url = 'https://'+rancherEndpoint+'/v3/cluster/'+rancherClusterID+'/storageClasses/storageclass'+workloadName
    payload = ""
    response = requests.get(url, data=payload, headers=headers ,verify=False)
    return response.status_code

## This function is used to fetch all storage classes for a given cluster name return an JSON object containing basic storage infos
def getAllStorageClass(rancherEndpoint,rancherClusterID,rancherAuth,rancherToken,headers):
    url = 'https://'+rancherEndpoint+'/v3/cluster/'+rancherClusterID+'/storageClasses'
    payload = ""
    response = requests.get(url, data=payload, headers=headers ,verify=False)
    content = response.content
    workloadList = json.loads(content)
    result=[]
    for storageClass in workloadList['data']:
        result.append(storageClass['id'])
    print(result)
    return result

## This function is used to fetch all workloads for a given workload name return an JSON object containing basic workload infos
def getAllWorkloadName(rancherEndpoint,rancherProjectID,rancherAuth,rancherToken,headers):
    url = 'https://'+rancherEndpoint+'/v3/project/'+rancherProjectID+'/workloads/'
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers ,verify=False)
    content = response.content
    workloadList = json.loads(content)
    result=[]
    for container in workloadList['data']:
        for name in container['containers']:
            result.append(name['name'])
    return result