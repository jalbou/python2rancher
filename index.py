### Minecraft to rancher/k8s workload & storage class management functions by Jeremy Albou ### 
import requests
import sys
import argparse
import json
import urllib3
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
#print(args)
#print(args.projectID)
workloadName = args.workloadName
projectID = args.projectID
count = args.count
## This function is used to fetch a workload by his name.
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
   # print(url)
   # print(response)
    return response.text
## This function is used to create a workload for a given name and projectID.
def setNewWorkload(workloadName,projectID):
    url = "https://192.168.55.107/v3/project/"+projectID+"/workloads"
    rawPayload =  {
    "containers": [
        {
        "allowPrivilegeEscalation": 'false',
        "environment": {
        "EULA": 'TRUE',
        "SERVER_PORT": '8081'
        },
        "image": 'itzg/minecraft-server',
        "imagePullPolicy": 'Always',
        "initContainer": 'false',
        "name": workloadName,
        "ports": [
        {
        "containerPort": '8081',
        "dnsName": workloadName+'-nodeport',
        "kind": 'NodePort',
        "name": '8081tcp01',
        "protocol": 'TCP',
        "sourcePort": '0',
        "type": '/v3/project/schemas/containerPort'
        }
        ],
        "readOnly": 'false',
        "resources": {
        "type": '/v3/project/schemas/resourceRequirements'
        },
        "restartCount":'0',
        "runAsNonRoot": 'false',
        "stdin": 'true',
        "stdinOnce": 'false',
        "terminationMessagePath": '/dev/termination-log',
        "terminationMessagePolicy": 'File',
        "tty": 'true',
        "type": '/v3/project/schemas/container'
        }
    ],
    "dnsPolicy": 'ClusterFirst',
    "hostIPC": 'false',
    "hostNetwork": "false",
    "hostPID": "false",
    "labels": {
        "workload.user.cattle.io/workloadselector": 'statefulSet-default-'+workloadName
    },
    "name": workloadName,
    "namespaceId": 'default',
    "ownerReferences": [ ],
    "projectId": projectID,
    "publicEndpoints": [ ],
    "readinessGates": [ ],
    "restartPolicy": "Always",
    "scale": 1,
    "schedulerName": "default-scheduler",
    "selector": {
        "matchLabels": {
            "workload.user.cattle.io/workloadselector": "statefulSet-default-"+workloadName
        },
        "type": "/v3/project/schemas/labelSelector"
    },
    "state": "active",
    "statefulSetConfig": {
        "podManagementPolicy": "OrderedReady",
        "revisionHistoryLimit": '10',
        "serviceName": workloadName,
        "strategy": "RollingUpdate"
    },
    "statefulSetStatus": {
        "collisionCount": '0',
        "currentReplicas": '1',
        "observedGeneration": '1',
        "readyReplicas": '1',
        "replicas": '1',
        "type": "/v3/project/schemas/statefulSetStatus",
        "updatedReplicas": '1'
    },
    "sysctls": [ ],
    "terminationGracePeriodSeconds": '30',
    "transitioning": "no",
    "transitioningMessage": "",
    "volumes": [ ],
    "workloadAnnotations": {
        "field.cattle.io/creatorId": "user-k6jnq"
    },
    "workloadLabels": {
        "cattle.io/creator": "norman",
        "workload.user.cattle.io/workloadselector": "statefulSet-default-"+workloadName
    }
    }
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
    #print(response.text)
    #print(url)
    #print(payload)
    #print(payload["containers"])
#getWorkload("toto")
#def setRemoveWorkload(workloadName,projectID)
i=0
while i < count:
    i += 1
    isWorkload = getWorkload(workloadName+str(i),projectID)
    jsonfile = json.loads(isWorkload)
    basetype= jsonfile["baseType"]
    if basetype == "error":
        print("Status found:"+basetype)
        print("No workload existing for "+workloadName+str(i))
        setNewWorkload(workloadName+str(i),projectID)
    else:
        print("Status found :"+basetype)
        print("Workload existing for "+workloadName+str(i))




