@echo off
setlocal enabledelayedexpansion

set OUTPUT_DIR=.\output
set TARGET_DIR=..\X_qxZap_CapitalistEconomy_P\MotorTown\Content\DataAsset\Vehicles\

for %%E in (uasset uexp) do (
    for %%F in ("%OUTPUT_DIR%\*.%%E") do (
        move "%%F" "%TARGET_DIR%" >nul
        if errorlevel 1 (
            echo Failed to move %%F
        ) else (
            echo Moved %%F to %TARGET_DIR%
        )
    )
)