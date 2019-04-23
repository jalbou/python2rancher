Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install vscode -y
choco install git -y
choco install postman -y
choco install notepadplusplus.install -y
choco install python3 -y
Set-ExecutionPolicy RemoteSigned
C:\Python37\python.exe .\Python_minecraftk8s\loadUserEnv.py