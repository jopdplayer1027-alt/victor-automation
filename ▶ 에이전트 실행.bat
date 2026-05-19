@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo  ================================================
echo   인원요청서 자동 생성 에이전트
echo  ================================================
echo   슬랙 메시지를 붙여넣고 Enter 입력
echo  ================================================
echo.

set PYTHONUTF8=1
call .venv\Scripts\activate.bat
claude

pause
