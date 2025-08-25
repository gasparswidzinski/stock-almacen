@echo off
echo ==========================================
echo   Generador de ejecutables - Stock Almacen
echo ==========================================
cd /d %~dp0

REM Limpiar compilaciones anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist main.spec del /f main.spec

echo.
echo ====== Generando version CARPETA (onedir) ======
pyinstaller --noconsole --clean main.py

echo.
echo ====== Generando version ARCHIVO UNICO (onefile) ======
pyinstaller --noconsole --onefile --clean main.py

echo.
echo ==========================================
echo   Proceso finalizado
echo   Revisar carpeta dist\
echo   - dist\main\main.exe   (CARPETA - recomendado)
echo   - dist\main.exe        (ARCHIVO UNICO)
echo ==========================================
pause
