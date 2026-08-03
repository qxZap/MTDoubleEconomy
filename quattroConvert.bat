@echo off
setlocal enabledelayedexpansion

REM Paths
set DELIVERY_DIR=DeliveryPoint
set LOG_FILE=quattro_failed.log

REM Clear previous log
if exist "%LOG_FILE%" del "%LOG_FILE%"

REM quattroStorage.py now builds the assets itself, with the same mappings it
REM read them with. This only picks up JSON left behind by a failure, so you can
REM fix one by hand and convert it without re-running everything.
echo Converting leftover JSON to UASSET...

for %%F in (%DELIVERY_DIR%\*.json) do (
    set BASENAME=%%~nF
    set SUCCESS=0

    for /L %%A in (1,1,1) do (
        if !SUCCESS! EQU 0 (
            "D:\MT\UAssetGUI.exe" fromjson "%%F" "%DELIVERY_DIR%\!BASENAME!.uasset" MotorTown719

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
