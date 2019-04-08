import requests
import sys
import argparse
import json
import urllib3

## This function is used to create a new Minecraft workload on a specific k8s cluster and assign it a new dynamic storage class
def setNewWorkload(workloadName,projectID,endpoint,rancherAuth,rancherToken):
    url = "https://"+endpoint+"/v3/project/"+projectID+"/workloads"
    # Read new Workload JSON config file
    with open('workloadConfig.json', 'r') as f:
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
    rawJSON['projectId'] = projectID
    payload=json.dumps(rawJSON, indent=4, sort_keys=True)
    #Set HTTP Header
    headers = {
        'Content-Type': "application/json",
        'Authorization': rancherAuth,
        'cache-control': "no-cache",
        'Postman-Token': rancherToken
    }
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    #if (response == ) :
    #print(response.text)

## This function is used to fetch a workload by his name, return 404 if any ressource was found
def getWorkload(workloadName,projectID,endpoint,rancherAuth,rancherToken):
    url = 'https://'+endpoint+'/v3/project/'+projectID+'/workloads/statefulset:default:'+workloadName 
    payload = ""
    #Set HTTP Header
    headers = {
    'Content-Type': "application/json",
    'Authorization': rancherAuth,
    'cache-control': "no-cache",
    'Postman-Token': rancherToken
    }
    response = requests.request("GET", url, data=payload, headers=headers ,verify=False)
    return response.text
    print(response)