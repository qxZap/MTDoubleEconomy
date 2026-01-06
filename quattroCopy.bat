@echo off

set DELIVERY_DIR=DeliveryPoint
set TARGET_DIR=X_qxZap_CapitalistEconomy_QuattroStorage_P\MotorTown\Content\Objects\Mission\Delivery\DeliveryPoint

REM Ensure target exists
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
)

echo Copying UASSET files...
copy "%DELIVERY_DIR%\*.uasset" "%TARGET_DIR%" /Y
copy "%DELIVERY_DIR%\*.uexp" "%TARGET_DIR%" /Y

echo Copy complete.
pause
