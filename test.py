import json
raw ={"FQDN": "192.168.100.114", "workloadName": "web1", "port": "30862", "status": 200}
result = json.loads(raw)
print(str(result["FQDN"]))