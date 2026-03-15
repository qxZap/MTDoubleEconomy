@echo off
setlocal enabledelayedexpansion

echo Running Python script...
python run.py
if errorlevel 1 (
    echo Failed to run run.py
    exit /b 1
)

echo Running conversion script...
call convert.bat
if errorlevel 1 (
    echo Failed to run convert.bat
    exit /b 1
)

echo Running move script...
call move.bat
if errorlevel 1 (
    echo Failed to run move.bat
    exit /b 1
)

echo All scripts executed successfully.