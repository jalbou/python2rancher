$RancherAuth = Read-Host -Prompt 'Enter your Rancher API Bearer'
$RancherToken = Read-Host -Prompt 'Enter your Rancher API Token'
[Environment]::SetEnvironmentVariable("RancherAuth","Basic "+$RancherAuth,"user")
[Environment]::SetEnvironmentVariable("RancherClusterID","c-czlqw","user")
[Environment]::SetEnvironmentVariable("RancherEndpoint","ran01.chamaa.local","user")
[Environment]::SetEnvironmentVariable("RancherToken",$RancherToken,"user")

