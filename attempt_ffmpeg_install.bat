@echo off

:: Change directory to the location of the batch file
cd /d "%~dp0"

:: Run the install.py script
python src\install_ffmpeg.py
pause