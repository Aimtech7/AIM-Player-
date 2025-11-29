
@echo off
REM Build standalone EXE with PyInstaller
pyinstaller --noconfirm --onefile --windowed --icon=assets/icon.ico app.py
echo Build finished. Check the dist\ directory.
pause
