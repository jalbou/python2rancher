### Minecraft to rancher/k8s workload & storage class management functions by Jeremy Albou ### 
import requests
import sys
import argparse
import json
import urllib3
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
args = parser.parse_args()
#print(args)
#print(args.projectID)
workloadName = args.workloadName
projectID = args.projectID
count = args.count
## This function is used to fetch a workload by his name.
#def setRemoveWorkload(workloadName,projectID)
i=0
while i < count:
    i += 1
    isWorkload = minecraftk8s.getWorkload(workloadName+str(i),projectID)
    jsonfile = json.loads(isWorkload)
    basetype= jsonfile["baseType"]
    if basetype == "error":
        print("Status found:"+basetype)
        print("No workload existing for "+workloadName+str(i))
        minecraftk8s.setNewWorkload(workloadName+str(i),projectID)
    else:
        print("Status found :"+basetype)
        print("Workload existing for "+workloadName+str(i))




