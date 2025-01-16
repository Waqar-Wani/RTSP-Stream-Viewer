@echo off

:: Change to the directory where the mediamtx.exe is located (relative path)
cd /d "mediamtx_v1.11.1_windows_amd64"

:: Start mediamtx.exe
start /b mediamtx.exe

:: Wait for 10 seconds to ensure mediamtx.exe has started
timeout /t 10 /nobreak > nul

:: Change to the directory where this batch file is located (RTSP folder)
cd /d "%~dp0"

:: Execute the Python script (streaming process) in the background
start /b python "Local Stream Test.py"

:: Pause to keep the window open
pause
