@echo off
title ZeroFilter Anti-Idle Supervisor
cd /d "%~dp0\.."
echo ==========================================================
echo    ZEROFILTER ANTI-IDLE DAEMON SUPERVISOR ACTIVATED
echo ==========================================================

:loop
echo [%date% %time%] Launching Anti-Idle Engine...
python -u engine\anti_idle.py
echo [%date% %time%] Process exited with code %errorlevel%. Resurrecting in 3 seconds...
timeout /t 3 /nobreak >nul
goto loop
