@echo off
setlocal enabledelayedexpansion

echo Running quattroStorage.py...
python quattroStorage.py
if errorlevel 1 (
    echo Python step failed. Aborting.
    pause
    exit /b 1
)

echo Running quattroConvert.bat...
call quattroConvert.bat

:WAIT_FOR_DONE
echo.
echo ==================================================
echo Check for failures and solve them manually.
echo When you are finished, press any key
echo ==================================================
pause


echo.
echo Proceeding to copy step...

call quattroCopy.bat

echo.
echo All steps completed successfully.
pause
