@echo off
chcp 65001 >nul
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Necesitas instalar Node.js 20.6 o superior en tu ordenador.
  echo https://nodejs.org/
  pause
  exit /b 1
)
if not exist ".env" (
  node configurar-ia.mjs
  if errorlevel 1 (
    pause
    exit /b 1
  )
)
echo Abre http://127.0.0.1:4173 en tu navegador.
node --env-file=.env server.mjs
pause
