import subprocess, sys
p = subprocess.Popen(["powershell.exe", 
              "C:\\Users\\jeremy\\Documents\\dev\\setUserEnv.ps1"], 
              stdout=sys.stdout)
p.communicate()
