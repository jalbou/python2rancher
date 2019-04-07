import requests
import sys
import argparse
import json
import urllib3
def setNewWorkload(workloadName,projectID):
    url = "https://192.168.55.107/v3/project/"+projectID+"/workloads"
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
        'Authorization': "Basic dG9rZW4tbHFyZHg6NXE2emxmd21iNHF4YjZydm5nOThoazg3N2ZxZGJrNm01Nmt2ZjdwZGRnNGxtbWtjNGpnOHF3",
        'cache-control': "no-cache",
        'Postman-Token': "3925edcb-d2cb-4477-8303-5094ba36886b"
    }
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    #if (response == ) :
    #print(response.text)

def getWorkload(workloadName,projectID):
    url = "https://192.168.55.107/v3/project/"+projectID+"/workloads/statefulset:default:"+workloadName 
    payload = ""
    headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic dG9rZW4tbHFyZHg6NXE2emxmd21iNHF4YjZydm5nOThoazg3N2ZxZGJrNm01Nmt2ZjdwZGRnNGxtbWtjNGpnOHF3",
    'cache-control': "no-cache",
    'Postman-Token': "3925edcb-d2cb-4477-8303-5094ba36886b"
    }
    response = requests.request("GET", url, data=payload, headers=headers ,verify=False)
   #print(url)
   #print(response)
    return response.text
    print(response)

getWorkload('toto','c-l5kcc:p-llwjz')