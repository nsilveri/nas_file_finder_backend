#!/bin/bash
# Script per avviare il NAS Scanner con API REST integrata

echo "========================================"
echo "  NAS Directory Scanner con API"
echo "========================================"
echo ""

# Controlla se esiste il virtual environment
if [ ! -f "venv/bin/python" ]; then
    echo "ERRORE: Virtual environment non trovato!"
    echo ""
    echo "Esegui prima setup_venv.sh per configurare l'ambiente."
    echo ""
    exit 1
fi

echo "Avvio del NAS Scanner..."
echo "  - Scansione NAS in background"
echo "  - API Server su http://localhost:5000"
echo ""
echo "Premi Ctrl+C per fermare il programma"
echo ""
echo "========================================"
echo ""

# Attiva il virtual environment e avvia main.py
source venv/bin/activate
python main.py
