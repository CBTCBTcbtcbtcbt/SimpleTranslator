@echo off
:: 检查是否已经是管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 已获得管理员权限，正在启动程序...
    cd /d "%~dp0"
    .venv\Scripts\python.exe simpletranslator.py
) else (
    echo 请求管理员权限...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
)
