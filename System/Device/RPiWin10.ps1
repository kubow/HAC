<# Used to connect inside Raspberry Pi #>
Set-Item WSMan:\localhost\Client\TrustedHosts -Value RPi2Win10Dev
<# IP: 172.20.31.138 Password: Aaa123456bcd789 #>
<# Enter-PSSession -ComputerName RPi2Win10Dev -Credential RPi2Win10Dev\Administrator #>
Enter-PSSession -ComputerName RPi2Win10Dev -Credential RPi2Win10Dev\Administrator
<# several basic commands #> 
tlist
Get-Service
IoTStartup list
<# Registry HKEY_CURRENT_USER #>
cd hkcu:
<# Cycle services - stop, restart ... #>
Restart-Service DHCP
<# Prepare things on MiniPC #>
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
Import-Module NetTCPIP
Get-NetTCPSetting
Get-NetRoute
Get-NetUDPEndpoint



schtasks /run /tn StartMsvsmon

Startup /d

<# Used for restart and stop #>
Stop-Computer -WsmanAuthentication Basic -computer 172.20.31.113 -Credential 172.20.31.113\Administrator
Restart-computer -WsmanAuthentication Basic
<# installing other things #>
$env:DNX_UNSTABLE_FEED = "https://www.myget.org/F/aspnetmaster"
dnvm upgrade
dnvm update-self

