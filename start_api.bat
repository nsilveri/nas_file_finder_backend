@echo off
REM Script per avviare il NAS Scanner con API REST integrata

echo ========================================
echo   NAS Directory Scanner con API
echo ========================================
echo.

REM Controlla se esiste il virtual environment
if not exist "venv\Scripts\python.exe" (
    echo ERRORE: Virtual environment non trovato!
    echo.
    echo Esegui prima setup_venv.bat per configurare l'ambiente.
    echo.
    pause
    exit /b 1
)

echo Avvio del NAS Scanner...
echo   - Scansione NAS in background
echo   - API Server su http://localhost:5000
echo.
echo Premi Ctrl+C per fermare il programma
echo.
echo ========================================
echo.

REM Attiva il virtual environment e avvia main.py
call venv\Scripts\activate.bat
python main.py

pause
