@echo off
call .venv\Scripts\activate

echo Building EXE...
pyinstaller jp_overlay.spec

echo.
echo Build finished.

REM -----------------------------
REM Locate the EXE inside dist
REM -----------------------------
set EXE_NAME=JPOverlay.exe
set DIST_DIR=dist
set BUILD_DIR=build

if not exist "%DIST_DIR%\%EXE_NAME%" (
    echo ERROR: EXE not found in dist folder.
    pause
    exit /b
)

REM -----------------------------
REM Create a safe output folder
REM -----------------------------
set OUTPUT_DIR=Release
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM -----------------------------
REM Copy EXE to Release folder
REM -----------------------------
copy "%DIST_DIR%\%EXE_NAME%" "%OUTPUT_DIR%\%EXE_NAME%" /Y

echo EXE copied to Release folder.

REM -----------------------------
REM Delete build and dist folders
REM -----------------------------
echo Cleaning up build folders...
rmdir /s /q "%DIST_DIR%"
rmdir /s /q "%BUILD_DIR%"

echo Cleanup complete.

REM -----------------------------
REM Add EXE to Windows Startup
REM -----------------------------
echo Adding EXE to Windows Startup...

set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set STARTUP_EXE=%STARTUP_FOLDER%\%EXE_NAME%

REM If EXE already exists in Startup, delete it
if exist "%STARTUP_EXE%" (
    echo Old startup EXE found. Deleting...
    del "%STARTUP_EXE%"
)

REM Copy new EXE to Startup
copy "%OUTPUT_DIR%\%EXE_NAME%" "%STARTUP_FOLDER%\%EXE_NAME%" /Y

echo Startup entry updated.

echo.
echo Build complete. Final EXE is in the Release folder.
pause