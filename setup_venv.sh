#!/bin/bash

echo "========================================"
echo "Setup Virtual Environment"
echo "========================================"
echo ""

# Crea il virtual environment
echo "[1/3] Creazione virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERRORE: Impossibile creare il virtual environment"
    exit 1
fi
echo "Virtual environment creato con successo!"
echo ""

# Attiva il virtual environment
echo "[2/3] Attivazione virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERRORE: Impossibile attivare il virtual environment"
    exit 1
fi
echo "Virtual environment attivato!"
echo ""

# Installa le dipendenze
echo "[3/3] Installazione dipendenze..."
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERRORE: Impossibile installare le dipendenze"
    exit 1
fi
echo ""

echo "========================================"
echo "Setup completato con successo!"
echo "========================================"
echo ""
echo "Per attivare il virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "Per eseguire il programma:"
echo "  python main.py"
echo ""
