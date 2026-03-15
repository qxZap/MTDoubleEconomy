@echo off
setlocal enabledelayedexpansion

REM Paths
set DELIVERY_DIR=DeliveryPoint
set LOG_FILE=quattro_failed.log

REM Clear previous log
if exist "%LOG_FILE%" del "%LOG_FILE%"

echo Converting JSON to UASSET...

for %%F in (%DELIVERY_DIR%\*.json) do (
    set BASENAME=%%~nF
    set SUCCESS=0

    for /L %%A in (1,1,1) do (
        if !SUCCESS! EQU 0 (
            UAssetGUI.exe fromjson "%%F" "%DELIVERY_DIR%\!BASENAME!.uasset" MotorTown718

            if exist "%DELIVERY_DIR%\!BASENAME!.uasset" (
                set SUCCESS=1
                del "%%F"
            )
        )
    )

    if !SUCCESS! EQU 0 (
        echo FAILED: %%~nxF
        echo %%~nxF>>"%LOG_FILE%"
    )
)

echo.
if exist "%LOG_FILE%" (
    echo Conversion finished WITH FAILURES.
    echo Failed files logged in %LOG_FILE%
) else (
    echo Conversion finished successfully. No failures.
)

pause
