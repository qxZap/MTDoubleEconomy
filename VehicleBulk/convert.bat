@echo off
setlocal enabledelayedexpansion

set OUTPUT_DIR=.\output

for %%F in ("%OUTPUT_DIR%\*.json") do (
    set "JSON_FILE=%%F"
    set "BASE_NAME=%%~nF"
    set "UASET_FILE=%OUTPUT_DIR%\!BASE_NAME!.uasset"
    
    UAssetGUI.exe fromjson "!JSON_FILE!" "!UASET_FILE!" MotorTown718T9
    
    if exist "!UASET_FILE!" (
        del "!JSON_FILE!"
    ) else (
        echo Failed to create !UASET_FILE! from !JSON_FILE!. Not deleting JSON.
    )
)