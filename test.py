### Minecraft to rancher/k8s workload & storage class management functions by Jeremy Albou ### 
import requests
import sys
import argparse
import json

### Creating argument helper and positioner ### 
parser = argparse.ArgumentParser()
parser.add_argument("-w","--workloadName", type=str,
                    help="Name of the Workload")
parser.add_argument("-c", "--count", type=int,
                    help="Number of desired deployments")
parser.add_argument("-p", "--projectID", type=str,
                    help="Project ID Number")
args = parser.parse_args()
#print(args)
#print(args.projectID)

## This function is used to fetch a workload by his name.
def getWorkload(workloadName,projectID):
    url = "https://192.168.55.107/v3/project/"+projectID+"/workloads/deployment:default:"+workloadName 
    payload = ""
    headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic dG9rZW4tbHFyZHg6NXE2emxmd21iNHF4YjZydm5nOThoazg3N2ZxZGJrNm01Nmt2ZjdwZGRnNGxtbWtjNGpnOHF3",
    'cache-control': "no-cache",
    'Postman-Token': "3925edcb-d2cb-4477-8303-5094ba36886b"
    }
    response = requests.request("GET", url, data=payload, headers=headers ,verify=False)
    print(response.text)
    return response.text

## This function is used to create a workload for a given name and projectID.
def setWorkload(workloadName,projectID):
    url = "https://192.168.55.107/v3/project/"+projectID+"/workloads"
    rawPayload = 
    payload = json.dumps(rawPayload)
    ##payload = json.loads(dumpedPayload)
    ##print(payload)
    headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic dG9rZW4tbHFyZHg6NXE2emxmd21iNHF4YjZydm5nOThoazg3N2ZxZGJrNm01Nmt2ZjdwZGRnNGxtbWtjNGpnOHF3",
    'cache-control': "no-cache",
    'Postman-Token': "3925edcb-d2cb-4477-8303-5094ba36886b"
    }
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    print(response.text)
    #print(url)
    #print(payload)
    #print(payload["containers"])
#getWorkload("toto")
setWorkload('minecraft1','c-l5kcc:p-llwjz')