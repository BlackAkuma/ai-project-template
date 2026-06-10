@echo off
rem One-click Cockpit (BL-4): starts the governance dashboard on THIS repo and opens the browser.
cd /d "%~dp0"
start "GPM Cockpit" /min python engine\api.py
timeout /t 2 /nobreak >nul
start http://127.0.0.1:8777
