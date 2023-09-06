@echo off
set /p month1="Enter file path for Month 1: "
set /p month2="Enter file path for Month 2: "

start powershell -Command "&{Get-AdUser -filter * -SearchBase \"[OU_OF_ALL_USERS]" | Select SamAccountName | Export-CSV ".\ADUsers.csv" -NoTypeInformation}" 
pause
python compareDayforceScript.py %month1% %month2%
pause