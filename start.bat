@echo off
title OPC Brain - 一人公司智能大脑
cd /d "D:\opc-brain"

echo ========================================
echo   OPC Brain - 一人公司智能大脑
echo   正在启动...
echo ========================================
echo.

:: 检查依赖
python -c "import fastapi" 2>nul
if %errorlevel% neq 0 (
    echo [1/3] 首次运行，安装依赖中...
    python -m pip install -r requirements.txt
    echo.
) else (
    echo [1/3] 依赖已就绪
)

echo [2/3] 启动服务...
start "OPC Brain Server" cmd /c "python -m uvicorn main:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

echo [3/3] 创建公网隧道...
start "OPC Brain Tunnel" cmd /c "npx localtunnel@latest --port 8000"

echo.
echo ========================================
echo   OPC Brain 已启动！
echo.
echo   本地访问: http://localhost:8000
echo   隧道地址: 查看 "OPC Brain Tunnel" 窗口
echo.
echo   关闭本窗口即停止服务
echo ========================================
echo.
pause
