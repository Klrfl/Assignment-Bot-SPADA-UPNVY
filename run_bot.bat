@echo off
:: Move the command prompt into the folder where THIS batch file is located
cd /d "%~dp0"

:: Print the path so we can see where we are
echo Current Folder: %cd%

:: Run the script
python botSPADA.py 

:: Keep the window open so we can read the error if it fails
pause