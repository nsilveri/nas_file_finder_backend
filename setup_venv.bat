@echo off
echo ========================================
echo Setup Virtual Environment
echo ========================================
echo.

REM Verifica che Python sia installato
echo [0/4] Verifica installazione Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato. Installa Python e riprova.
    pause
    exit /b 1
)
python --version
echo.

REM Rimuovi vecchio venv se esiste
if exist venv (
    echo Rimozione vecchio virtual environment...
    rmdir /s /q venv
    echo.
)

REM Crea il virtual environment
echo [1/4] Creazione virtual environment...
python -m venv venv --clear
if errorlevel 1 (
    echo ERRORE: Impossibile creare il virtual environment
    echo Prova a eseguire: python -m pip install --upgrade pip
    pause
    exit /b 1
)
echo Virtual environment creato con successo!
echo.

REM Attiva il virtual environment
echo [2/4] Attivazione virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRORE: Impossibile attivare il virtual environment
    pause
    exit /b 1
)
echo Virtual environment attivato!
echo.

REM Aggiorna pip
echo [3/4] Aggiornamento pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo ATTENZIONE: Impossibile aggiornare pip, continuo comunque...
)
echo Pip aggiornato!
echo.

REM Installa le dipendenze
echo [4/4] Installazione dipendenze...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRORE: Impossibile installare le dipendenze
    echo Verifica che il file requirements.txt esista
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup completato con successo!
echo ========================================
echo.
echo Per attivare il virtual environment:
echo   venv\Scripts\activate
echo.
echo Per eseguire il programma:
echo   python main.py
echo.
pause
