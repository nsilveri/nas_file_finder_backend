# NAS Directory Scanner - Backend Python

## 🇮🇹 Versione Italiana

### Descrizione

NAS Directory Scanner è un servizio Python che esegue la scansione ricorsiva di directory su NAS, salvando informazioni su file e cartelle in un database PostgreSQL. Il sistema offre scansioni complete o incrementali basate su range temporali, con configurazione dinamica tramite database.

### Caratteristiche Principali

- ✅ **Scansione Ricorsiva**: Scansione completa di directory NAS con tutti i sottodirectory
- 📊 **Database PostgreSQL**: Salvataggio strutturato di file e cartelle con timestamp
- ⚡ **Scansioni Incrementali**: Modalità range temporale per scansionare solo le cartelle modificate di recente
- 🔧 **Configurazione Dinamica**: Tutte le impostazioni configurabili tramite database
- 📈 **Monitoraggio in Tempo Reale**: Progress bar, statistiche e tempo rimanente stimato
- 🛡️ **Gestione Errori Robusta**: Gestione automatica di file corrotti, percorsi non validi e permessi negati
- ⏱️ **Scansione Periodica**: Esecuzione automatica a intervalli configurabili
- 🎯 **Ottimizzazioni Performance**: Salta file già aggiornati per ridurre scritture database

### Requisiti

- Python 3.12+
- PostgreSQL 12+
- Accesso di rete al NAS

### Installazione

```bash
# Clona il repository
cd backend_python

# OPZIONE 1: Setup automatico con virtual environment (RACCOMANDATO)
# Windows
setup_venv.bat

# Linux/Mac
chmod +x setup_venv.sh
./setup_venv.sh

# OPZIONE 2: Installazione manuale
# Crea virtual environment
python -m venv venv

# Attiva virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt
```

### Configurazione Database

Il sistema utilizza una tabella `configurations` per gestire tutte le impostazioni:

| Chiave | Tipo | Default | Descrizione |
|--------|------|---------|-------------|
| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | Directory del NAS da scansionare |
| `scan_interval` | integer | `10` | Intervallo in secondi tra le scansioni |
| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | Estensioni file da escludere |
| `periodically_scan` | boolean | `true` | Abilita scansione periodica |
| `scan_type` | enum | `full` | Tipo scansione: `full` o `range` |
| `scan_days_back` | integer | `30` | Giorni da scansionare (solo per `range`) |

### Struttura Database

```sql
-- Tabella file
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    directory TEXT NOT NULL,
    last_modified TIMESTAMP NOT NULL,
    UNIQUE(filename, directory)
);

-- Tabella cartelle
CREATE TABLE folders (
    id SERIAL PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    last_modified TIMESTAMP NOT NULL
);

-- Tabella configurazioni
CREATE TABLE configurations (
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Utilizzo

```bash
# Attiva il virtual environment (se non già attivo)
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Esegui il servizio
python main.py
```

### Modalità di Scansione

#### Scansione Completa (`scan_type = 'full'`)
Scansiona tutte le cartelle e file del NAS ad ogni esecuzione.

```sql
UPDATE configurations SET value = 'full' WHERE key = 'scan_type';
```

#### Scansione Range (`scan_type = 'range'`)
Scansiona solo le cartelle modificate negli ultimi N giorni.

```sql
UPDATE configurations SET value = 'range' WHERE key = 'scan_type';
UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';  -- Ultimi 30 giorni
```

### Output Esempio

```
Configurazioni caricate:
  - Directory NAS: \\<NAS_IP>\<SHARE>\<FOLDER>
  - Intervallo scansione: 10 secondi
  - Estensioni escluse: ['.tmp', '.bak']
  - Scansione periodica: True
  - Tipo scansione: range
  - Range temporale: ultimi 30 giorni

Modalità scansione: RANGE (ultimi 30 giorni, dalla data: 2025-09-02 00:00:00)
Cartelle da scansionare nel range: 127
File totali nel database: 316619

Scan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8

--- Riepilogo parziale ---
  - File scansionati: 209692/316619 (66.2%)
  - Tempo trascorso: 25m 10s
  - Tempo rimanente stimato: 00:15:23
  - File inseriti (nuovi): 45
  - File aggiornati: 23
  - File saltati (già aggiornati): 209624
  - Cartelle nuove: 12
  - Cartelle aggiornate: 8
------------------------

Scansione completata:
  - Tipo scansione: RANGE
  - Range temporale: ultimi 30 giorni
  - Data inizio: 2025-09-02 00:00:00
  - Cartelle nel range: 127
  - Cartelle saltate (fuori range): 1523
  - Tempo totale: 00:40:33
  - File scansionati: 316619/316619
  - File inseriti (nuovi): 45
  - File aggiornati: 23
  - File saltati (già aggiornati): 316551
  - Cartelle nuove: 12
  - Cartelle aggiornate: 115
```

### Funzioni Utility

Il modulo `utility_folders.py` include funzioni helper:

- `scan_folders_only()`: Scansione iniziale solo cartelle
- `compare_folder_db_vs_nas()`: Confronto tra DB e filesystem
- `compare_subfolders_db_vs_nas()`: Confronto ricorsivo sottocartelle
- `truncate_last_modified_to_seconds()`: Normalizzazione timestamp

### Gestione Errori

Il sistema gestisce automaticamente:
- ❌ File con percorsi non validi
- ❌ Caratteri speciali nel nome file
- ❌ Percorsi troppo lunghi (>260 caratteri su Windows)
- ❌ Timestamp corrotti o fuori range
- ❌ Permessi negati

### Performance

- **Controllo pre-scrittura**: Verifica se il file è già aggiornato prima di scrivere nel DB
- **Scansioni incrementali**: Modalità range per ridurre il carico
- **Batch updates**: Commit singolo al termine della scansione
- **Skip intelligente**: Salta file già processati con stesso `last_modified`

### Configurazione per il Frontend

Esempio di API REST per il frontend:

```python
# GET /api/config - Ottieni tutte le configurazioni
{
  "nas_directory": "\\\\<NAS_IP>\\<SHARE>\\<FOLDER>",
  "scan_interval": 10,
  "exclude_extensions": [".tmp", ".bak"],
  "periodically_scan": true,
  "scan_type": "range",
  "scan_days_back": 30
}

# PUT /api/config - Aggiorna configurazioni
{
  "scan_type": "range",
  "scan_days_back": 7
}
```

### Licenza

MIT License
