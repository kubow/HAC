<#
    .Synopsis 
        Get the registry key values from remote computers.
        
    .Description
        This script helps you to get the get details of a given registry key from remote computer. 
		This script will give the if the registry exists or not, it’s value and type of valus.
 
    .Parameter ComputerName    
        Computer name(s) for which you want to get the disk space details.
        
    
    .Notes
        NAME:      Get-DiskSpaceDetails.ps1
        AUTHOR:    Sitaram Pamarthi
		WEBSITE:   http://techibee.com

#>

[cmdletbinding()]
param (
	[parameter(Mandatory=$true)]
	[String]$RegistryKey,
	[parameter(ValueFromPipeline=$true,ValueFromPipelineByPropertyName=$true)]
	[String[]]$ComputerName = $env:ComputerName,
	[parameter(Mandatory=$true)]
	[String]$KeyProperty
)

Begin  {
	$RegistryKey -match "(?<BaseKey>\w+)\\(?<SubKey>.+)" | Out-Null

	switch($Matches.BaseKey) {
		"HKEY_LOCAL_MACHINE" 	{$BaseKey = "LocalMachine"} 
		"HKEY_USERS" 			{$BaseKey = "Users"} 
		"HKEY_CLASSES_ROOT" 	{$BaseKey = "ClassesRoot"}
		"HKEY_CURRENT_USER" 	{$BaseKey = "CurrentUser"}
		"HKEY_CURRENT_CONFIG" 	{$BaseKey = "CurrentConfig"}
		default {
			write-host "Unable to determine base key type. Exiting"
			exit(1)
		}
	}
}

process {
	foreach($Computer in $ComputerName) {
		$Computer = $Computer.ToUpper()
		if(Test-Connection -ComputerName $Computer -count 1 -ea 0) {
			$flag = $false
			try {
				$BaseKeyObj = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey($BaseKey, $computer)
				$KeyObj = $BaseKeyObj.OpenSubKey($Matches.SubKey)
				if($KeyObj) {
					foreach ($Property in $KeyObj.GetValueNames()) {
						if($KeyProperty -contains $Property) {
							$flag = $true
						}
						
					}
				} else {
					Write-Verbose "$($Matches.SubKey) not found on $Computer"
				}
			
			} catch {
				Write-Verbose "Failed to query the registry on Computer: $Computer"
			}
			
			$PropertyType=""
			$PropertyValue=""
			if($flag) {
				$PropertyType  = $KeyObj.GetValueKind($KeyProperty)
				$PropertyValue = $KeyObj.GetValue($KeyProperty)
			}
			$OutputObj = New-Object PSObject -Prop (
			@{
				ComputerName = $Computer.ToUpper()
				PropertyName = $KeyProperty
				PropertyValue = $PropertyValue
				PropertyType = $PropertyType
				IsPresent = $flag
			})
			
			$OutputObj
		} else {
			Write-Verbose "$Computer is not reachable"
		}
	}
}
end {
}	
	
