@echo off
setlocal
title AI Video Clip Maker - Android APK Builder
cd /d "%~dp0frontend"

echo ==========================================
echo   AI VIDEO CLIP MAKER - ANDROID BUILDER
echo ==========================================
echo.
where node >nul 2>nul || (echo Node.js missing. Install from https://nodejs.org/ & pause & exit /b 1)
where npm >nul 2>nul || (echo npm missing. Reinstall Node.js. & pause & exit /b 1)

echo [1/4] Installing project dependencies...
call npm install
if errorlevel 1 goto failed

echo [2/4] Preparing Android project...
if not exist "android" (
  call npm run android:init
) else (
  call npm run android:sync
)
if errorlevel 1 goto failed

echo [3/4] Syncing Android assets...
call npm run android:sync
if errorlevel 1 goto failed

echo [4/4] Opening Android Studio...
call npm run android:open
if errorlevel 1 goto failed

echo.
echo Android Studio is opening. Wait for Gradle sync to finish.
echo Then select Build ^> Build Bundle(s) / APK(s) ^> Build APK(s).
echo APK output is usually android\app\build\outputs\apk\debug\app-debug.apk
pause
exit /b 0

:failed
echo.
echo Build preparation failed. Check internet, Node.js, and Android Studio installation.
pause
exit /b 1
