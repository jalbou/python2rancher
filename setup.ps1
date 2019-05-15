<# $RancherAuth = Read-Host -Prompt 'Enter your Rancher API Bearer'
$RancherToken = Read-Host -Prompt 'Enter your Rancher API Token'
$NSXAuth = Read-Host -Prompt 'Enter your NSX API Bearer'
$NSXToken = Read-Host -Prompt 'Enter your NSX API Token'
## TO DO : TEST the presence of chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install vscode -y
choco install git -y
choco install postman -y
choco install notepadplusplus.install -y
choco install python3 -y #>
#[Environment]::SetEnvironmentVariable("RancherAuth","Basic "+$RancherAuth,"user")
[Environment]::SetEnvironmentVariable("RancherClusterID","c-nx2zg","user")
[Environment]::SetEnvironmentVariable("RancherProjectID",'c-nx2zg:p-5qb6d',"user")
[Environment]::SetEnvironmentVariable("RancherEndpoint","ran01.chamaa.local","user")
#[Environment]::SetEnvironmentVariable("RancherToken",$RancherToken,"user")
#[Environment]::SetEnvironmentVariable("NSXAuth",$NSXAuth,"user")
#[Environment]::SetEnvironmentVariable("NSXToken",$NSXToken,"user")