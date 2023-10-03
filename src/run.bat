@echo off
echo "Compressing file!"
@REM Print the file being converted
python "%~dp0\compress.py %*"
