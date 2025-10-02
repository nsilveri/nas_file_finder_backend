# NAS Directory Scanner - Backend Python# NAS Directory Scanner - Backend Python



A Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database with support for full and incremental scans.[🇮🇹 Versione Italiana](./README_IT.md) | [🇬🇧 English Version](./README_EN.md)



[🇮🇹 Versione Italiana](#-versione-italiana) | [🇬🇧 English Version](#-english-version)---



---## Quick Start



## 🇬🇧 English Version### Description



### DescriptionNAS Directory Scanner is a Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database.



NAS Directory Scanner is a robust Python service designed to monitor and index NAS directories. It performs recursive scans, storing comprehensive file and folder metadata in PostgreSQL with support for both complete and time-ranged incremental scans.### Features



### ✨ Key Features- ✅ Recursive NAS directory scanning

- 📊 PostgreSQL database storage

- 🔄 **Recursive Scanning**: Complete NAS directory traversal with subdirectories- ⚡ Incremental scans (time-range based)

- 📊 **PostgreSQL Storage**: Structured storage with timestamps and metadata- 🔧 Dynamic database configuration

- ⚡ **Incremental Scans**: Time-range mode for modified folders only- 📈 Real-time monitoring with progress tracking

- 🔧 **Dynamic Configuration**: Database-driven settings (no code changes needed)- 🛡️ Robust error handling

- 📈 **Real-time Monitoring**: Progress tracking with ETA and statistics- 🌐 REST API for monitoring and statistics

- 🛡️ **Robust Error Handling**: Automatic handling of corrupted files and permissions

- ⏱️ **Periodic Execution**: Configurable automatic scanning intervals### Installation

- 🎯 **Performance Optimized**: Smart skipping of unchanged files

- 🌐 **REST API**: Built-in API for monitoring and configuration```bash

cd backend_python

### 🚀 Quick Start

# Quick setup (recommended)

#### Prerequisitessetup_venv.bat  # Windows

# or

- Python 3.12+./setup_venv.sh  # Linux/Mac

- PostgreSQL 12+

- Network access to NAS# Then run

python main.py

#### Installation```



**Option 1: Automatic Setup (Recommended)**### Configuration



```bashAll settings are stored in the database `configurations` table:

# Windows

setup_venv.bat| Key | Default | Description |

|-----|---------|-------------|

# Linux/Mac| `nas_directory` | `\\NAS\scanner` | NAS directory path |

chmod +x setup_venv.sh| `scan_interval` | `10` | Seconds between scans |

./setup_venv.sh| `exclude_extensions` | `[".tmp", ".bak"]` | File extensions to exclude |

```| `scan_type` | `full` | `full` or `range` |

| `scan_days_back` | `30` | Days for range scan |

**Option 2: Manual Installation**

### Documentation

```bash

# Create virtual environment- [📡 API Documentation](./API_DOCUMENTATION.md)

python -m venv venv- [🇮🇹 Documentazione Italiana](./README_IT.md)

- [🇬🇧 English Documentation](./README_EN.md)

# Activate virtual environment

# Windows### License

venv\Scripts\activate

# Linux/MacMIT License

source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Running the Service

```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# Or directly
python main.py
```

### 📋 Configuration

The system uses a PostgreSQL `configurations` table for all settings:

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | NAS directory to scan |
| `scan_interval` | integer | `10` | Interval in seconds between scans |
| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | File extensions to exclude |
| `periodically_scan` | boolean | `true` | Enable periodic scanning |
| `scan_type` | enum | `full` | Scan type: `full` or `range` |
| `scan_days_back` | integer | `30` | Days to scan back (for `range` mode) |

### 🗄️ Database Structure

```sql
-- Files table
CREATE TABLE files (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    directory TEXT NOT NULL,
    last_modified TIMESTAMP NOT NULL,
    UNIQUE(filename, directory)
);

-- Folders table
CREATE TABLE folders (
    id SERIAL PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    last_modified TIMESTAMP NOT NULL
);

-- Configurations table
CREATE TABLE configurations (
    id SERIAL PRIMARY KEY,
    key TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 📊 Scan Modes

#### Full Scan
Scans all NAS folders and files on each execution.

```sql
UPDATE configurations SET value = 'full' WHERE key = 'scan_type';
```

#### Range Scan (Incremental)
Scans only folders modified in the last N days (much faster).

```sql
UPDATE configurations SET value = 'range' WHERE key = 'scan_type';
UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';
```

### 🌐 REST API

The service includes a built-in REST API running on `http://localhost:5000`:

- `GET /api/health` - Health check
- `GET /api/statistics` - System statistics
- `GET /api/configurations` - Get all configurations
- `PUT /api/configurations/{key}` - Update configuration
- `GET /api/scan/status` - Current scan status

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full details.

### 📈 Example Output

```
Loaded configurations:
  - NAS Directory: \\<NAS_IP>\<SHARE>\<FOLDER>
  - Scan interval: 10 seconds
  - Excluded extensions: ['.tmp', '.bak']
  - Periodic scan: True
  - Scan type: range
  - Time range: last 30 days

Scan mode: RANGE (last 30 days, from date: 2025-09-02 00:00:00)
Folders to scan in range: 127
Total files in database: 316619

Scan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8

Scan completed:
  - Total time: 00:40:33
  - Files scanned: 316619/316619
  - Files inserted (new): 45
  - Files updated: 23
  - Files skipped (unchanged): 316551
```

### 🛠️ Architecture

- **Main Thread**: Handles periodic NAS scanning
- **API Thread**: Runs Flask REST API (daemon thread)
- **Dual Database**: PostgreSQL for data + SQLite for configurations

### 📝 License

MIT License

---

## 🇮🇹 Versione Italiana

### Descrizione

NAS Directory Scanner è un servizio Python robusto progettato per monitorare e indicizzare directory su NAS. Esegue scansioni ricorsive, salvando metadati completi di file e cartelle in PostgreSQL con supporto per scansioni complete e incrementali basate su range temporali.

### ✨ Caratteristiche Principali

- 🔄 **Scansione Ricorsiva**: Attraversamento completo delle directory NAS con sottocartelle
- 📊 **Archiviazione PostgreSQL**: Storage strutturato con timestamp e metadati
- ⚡ **Scansioni Incrementali**: Modalità range temporale per cartelle modificate
- 🔧 **Configurazione Dinamica**: Impostazioni guidate dal database (nessuna modifica al codice)
- 📈 **Monitoraggio Real-time**: Tracking progresso con ETA e statistiche
- 🛡️ **Gestione Errori Robusta**: Gestione automatica di file corrotti e permessi
- ⏱️ **Esecuzione Periodica**: Intervalli di scansione automatica configurabili
- 🎯 **Ottimizzato per Performance**: Skip intelligente di file non modificati
- 🌐 **REST API**: API integrata per monitoraggio e configurazione

### 🚀 Avvio Rapido

#### Prerequisiti

- Python 3.12+
- PostgreSQL 12+
- Accesso di rete al NAS

#### Installazione

**Opzione 1: Setup Automatico (Raccomandato)**

```bash
# Windows
setup_venv.bat

# Linux/Mac
chmod +x setup_venv.sh
./setup_venv.sh
```

**Opzione 2: Installazione Manuale**

```bash
# Crea virtual environment
python -m venv venv

# Attiva virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
```

#### Esecuzione del Servizio

```bash
# Windows
start.bat

# Linux/Mac
./start.sh

# Oppure direttamente
python main.py
```

### 📋 Configurazione

Il sistema utilizza una tabella PostgreSQL `configurations` per tutte le impostazioni:

| Chiave | Tipo | Default | Descrizione |
|--------|------|---------|-------------|
| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | Directory del NAS da scansionare |
| `scan_interval` | integer | `10` | Intervallo in secondi tra le scansioni |
| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | Estensioni file da escludere |
| `periodically_scan` | boolean | `true` | Abilita scansione periodica |
| `scan_type` | enum | `full` | Tipo scansione: `full` o `range` |
| `scan_days_back` | integer | `30` | Giorni da scansionare (modalità `range`) |

### 🗄️ Struttura Database

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

### 📊 Modalità di Scansione

#### Scansione Completa
Scansiona tutte le cartelle e file del NAS ad ogni esecuzione.

```sql
UPDATE configurations SET value = 'full' WHERE key = 'scan_type';
```

#### Scansione Range (Incrementale)
Scansiona solo le cartelle modificate negli ultimi N giorni (molto più veloce).

```sql
UPDATE configurations SET value = 'range' WHERE key = 'scan_type';
UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';
```

### 🌐 REST API

Il servizio include un'API REST integrata su `http://localhost:5000`:

- `GET /api/health` - Controllo stato
- `GET /api/statistics` - Statistiche sistema
- `GET /api/configurations` - Ottieni tutte le configurazioni
- `PUT /api/configurations/{key}` - Aggiorna configurazione
- `GET /api/scan/status` - Stato scansione corrente

Vedi [API_DOCUMENTATION.md](API_DOCUMENTATION.md) per dettagli completi.

### 📈 Output Esempio

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

Scansione completata:
  - Tempo totale: 00:40:33
  - File scansionati: 316619/316619
  - File inseriti (nuovi): 45
  - File aggiornati: 23
  - File saltati (non modificati): 316551
```

### 🛠️ Architettura

- **Thread Principale**: Gestisce la scansione periodica del NAS
- **Thread API**: Esegue l'API REST Flask (daemon thread)
- **Database Doppio**: PostgreSQL per dati + SQLite per configurazioni

### 📝 Licenza

MIT License

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.
