@echo off
REM Enable WoL
REG ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v "EnableWol" /t REG_DWORD /d "1" /f

REM Set Linux as default boot entry
bcdedit /set {bootmgr} path \EFI\ubuntu\grubx64.efi
