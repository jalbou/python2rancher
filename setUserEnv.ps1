#Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
#choco install vscode
#choco install git
#choco install postman
#choco install notepadplusplus.install
#choco install python3

Set-ExecutionPolicy RemoteSigned
$RancherAuth = Read-Host -Prompt 'Enter your Rancher API Bearer'
$RancherToken = Read-Host -Prompt 'Enter your Rancher API Token'
[Environment]::SetEnvironmentVariable("RancherAuth","Basic "+$RancherAuth,"user")
[Environment]::SetEnvironmentVariable("RancherClusterID","c-czlqw","user")
[Environment]::SetEnvironmentVariable("RancherEndpoint","ran01.chamaa.local","user")
[Environment]::SetEnvironmentVariable("RancherToken",$RancherToken,"user")

