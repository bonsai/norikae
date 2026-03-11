@echo off
REM Generate GLB files for Micro:bit Smart Lock Servo Holder
REM Run this batch file to create 3D model files

cd /d "%~dp0"

echo ========================================
echo Micro:bit Smart Lock - GLB Generator
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.
echo Generating 3D model files...
echo.

python generate-glb.py

echo.
echo ========================================
echo Checking generated files...
echo ========================================

if exist "servo-holder-assembled.glb" (
    echo [OK] servo-holder-assembled.glb
    for %%A in ("servo-holder-assembled.glb") do echo      Size: %%~zA bytes
) else (
    echo [FAIL] servo-holder-assembled.glb not created
)

if exist "servo-holder-exploded.glb" (
    echo [OK] servo-holder-exploded.glb
    for %%A in ("servo-holder-exploded.glb") do echo      Size: %%~zA bytes
) else (
    echo [FAIL] servo-holder-exploded.glb not created
)

echo.
echo ========================================
echo How to view the GLB files:
echo ========================================
echo 1. Double-click on the .glb file (Windows 3D Viewer)
echo 2. Open in Blender (File > Import > glTF 2.0)
echo 3. Visit https://gltf.report/ and drag the file
echo 4. Visit https://sandbox.babylonjs.com/
echo.

pause
