@echo off

:: Change directory to the location of the batch file
cd /d "%~dp0"

:: Run the install.py script
python src\install.py

:: Pause to see any output before closing
echo Installed! Try right clicking on some images or videos.
pause
