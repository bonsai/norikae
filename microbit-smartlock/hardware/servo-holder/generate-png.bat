@echo off
REM Generate PNG files for Micro:bit Smart Lock Servo Holder
cd /d "%~dp0"
echo Generating PNG files...
python generate-png.py
pause
