import subprocess, sys
p = subprocess.Popen(["powershell.exe", 
              'C:\\Users\\jeremy\\Documents\\dev\\setUserEnv.ps1 '+args[0]+''+args[1]], 
              stdout=sys.stdout)
p.communicate()
