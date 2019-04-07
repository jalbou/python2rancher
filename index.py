### Minecraft to rancher/k8s workload & storage class management functions by Jeremy Albou ### 
#Module to manage https requests
import requests
import sys
#Module to manage argument parsing
import argparse
import json
#Module to manage HTTPS python config
import urllib3
#Custom librarie to manage Minecraft workloads on a given k8s cluster managed by Rancher
import minecraftk8s as minecraftk8s
urllib3.disable_warnings()
### Creating argument helper and positioner ### 
parser = argparse.ArgumentParser()
parser.add_argument("-w","--workloadName", type=str,
                    help="Name of the Workload")
parser.add_argument("-c", "--count", type=int,
                    help="Number of desired deployments")
parser.add_argument("-p", "--projectID", type=str,
                    help="Project ID Number")
parser.add_argument("-e", "--endpoint", type=str,
                    help="API Endpoint URL")                  
args = parser.parse_args()

projectID = args.projectID
endpoint = args.endpoint
count = args.count
i=0
while i < count:
    i += 1
    workloadName = args.workloadName+str(i)
    isWorkload = minecraftk8s.getWorkload(workloadName,projectID,endpoint)
    jsonfile = json.loads(isWorkload)
    basetype= jsonfile["baseType"]
    if basetype == "error":
        print("Status found:"+basetype)
        print("No workload existing for "+workloadName)
        minecraftk8s.setNewWorkload(workloadName,projectID,endpoint)
    else:
        print("Status found :"+basetype)
        print("Workload existing for "+workloadName)




