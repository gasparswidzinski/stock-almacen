@echo off
echo ==========================================
echo   Generando version PORTABLE (onefile)
echo ==========================================
cd /d %~dp0

REM Limpiar compilaciones anteriores
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist main.spec del /f main.spec
if exist pendrive_build rmdir /s /q pendrive_build

REM Crear .exe unico
pyinstaller --noconsole --onefile --clean main.py

REM Crear carpeta lista para copiar al pendrive
mkdir pendrive_build
copy dist\main.exe pendrive_build\stock_almacen.exe

echo.
echo ==========================================
echo   EXE PORTABLE LISTO!
echo   Archivo final: pendrive_build\stock_almacen.exe
echo   Copialo a tu pendrive y listo :)
echo ==========================================
pause
