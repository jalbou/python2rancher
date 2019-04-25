$RancherAuth = Read-Host -Prompt 'Enter your Rancher API Bearer'
$RancherToken = Read-Host -Prompt 'Enter your Rancher API Token'
## TO DO : TEST the presence of chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install vscode -y
choco install git -y
choco install postman -y
choco install notepadplusplus.install -y
choco install python3 -y
[Environment]::SetEnvironmentVariable("RancherAuth","Basic "+$RancherAuth,"user")
[Environment]::SetEnvironmentVariable("RancherClusterID","c-czlqw","user")
[Environment]::SetEnvironmentVariable("RancherProjectID",'c-czlqw:p-tfzmg',"user")
[Environment]::SetEnvironmentVariable("RancherEndpoint","ran01.chamaa.local","user")
[Environment]::SetEnvironmentVariable("RancherToken",$RancherToken,"user")