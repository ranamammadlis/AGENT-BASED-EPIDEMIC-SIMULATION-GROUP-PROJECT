@echo off
echo ========================================
echo SIR Epidemic Simulator - Build Tool
echo ========================================
echo.
echo This will build a standalone .exe file
echo.
pause

echo.
echo Step 1: Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo Step 2: Building executable with PyInstaller...
pyinstaller --onefile --windowed --name=SIR_Epidemic_Simulator sir_epidemic_simulator.py

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Your executable is located at:
echo   dist\SIR_Epidemic_Simulator.exe
echo.
echo You can now run this file on any Windows computer!
echo.
pause
