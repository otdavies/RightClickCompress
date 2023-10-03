@echo off
:: Check for administrative privileges
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Please run as administrator.
    pause
    exit
)

:: Change directory to the location of the batch file
cd /d "%~dp0"

:: Run the install.py script
python src\install.py

:: Pause to see any output before closing
pause
