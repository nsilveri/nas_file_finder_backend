# NAS Directory Scanner - Backend Python# NAS Directory Scanner - Backend Python# NAS Directory Scanner - Backend Python



A Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database with support for full and incremental scans.



[🇮🇹 Versione Italiana](#-versione-italiana) | [🇬🇧 English Version](#-english-version)A Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database with support for full and incremental scans.[🇮🇹 Versione Italiana](./README_IT.md) | [🇬🇧 English Version](./README_EN.md)



---



## 📁 Project Structure[🇮🇹 Versione Italiana](#-versione-italiana) | [🇬🇧 English Version](#-english-version)---



```

backend_python/

├── main.py                 # Main application entry point---## Quick Start

├── setup_venv.bat         # Windows setup script

├── setup_venv.sh          # Linux/Mac setup script

├── start.bat              # Windows start script

├── start.sh               # Linux/Mac start script## 🇬🇧 English Version### Description

├── requirements.txt       # Python dependencies

├── config.db              # SQLite configuration database

├── .gitignore            # Git ignore rules

├── .env.example          # Environment variables template### DescriptionNAS Directory Scanner is a Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database.

├── src/                  # Source code modules

│   ├── __init__.py

│   ├── api_routes.py     # REST API endpoints

│   └── utility_folders.py # Utility functionsNAS Directory Scanner is a robust Python service designed to monitor and index NAS directories. It performs recursive scans, storing comprehensive file and folder metadata in PostgreSQL with support for both complete and time-ranged incremental scans.### Features

├── docs/                 # Documentation

│   ├── API_DOCUMENTATION.md

│   ├── README_EN.md      # Extended English docs

│   └── README_IT.md      # Extended Italian docs### ✨ Key Features- ✅ Recursive NAS directory scanning

├── sql/                  # SQL scripts

│   └── init_db.sql       # Database initialization- 📊 PostgreSQL database storage

└── tests/                # Test files

    └── test_api.py       # API tests- 🔄 **Recursive Scanning**: Complete NAS directory traversal with subdirectories- ⚡ Incremental scans (time-range based)

```

- 📊 **PostgreSQL Storage**: Structured storage with timestamps and metadata- 🔧 Dynamic database configuration

---

- ⚡ **Incremental Scans**: Time-range mode for modified folders only- 📈 Real-time monitoring with progress tracking

## 🇬🇧 English Version

- 🔧 **Dynamic Configuration**: Database-driven settings (no code changes needed)- 🛡️ Robust error handling

### Description

- 📈 **Real-time Monitoring**: Progress tracking with ETA and statistics- 🌐 REST API for monitoring and statistics

NAS Directory Scanner is a robust Python service designed to monitor and index NAS directories. It performs recursive scans, storing comprehensive file and folder metadata in PostgreSQL with support for both complete and time-ranged incremental scans.

- 🛡️ **Robust Error Handling**: Automatic handling of corrupted files and permissions

### ✨ Key Features

- ⏱️ **Periodic Execution**: Configurable automatic scanning intervals### Installation

- 🔄 **Recursive Scanning**: Complete NAS directory traversal with subdirectories

- 📊 **PostgreSQL Storage**: Structured storage with timestamps and metadata- 🎯 **Performance Optimized**: Smart skipping of unchanged files

- ⚡ **Incremental Scans**: Time-range mode for modified folders only

- 🔧 **Dynamic Configuration**: Database-driven settings (no code changes needed)- 🌐 **REST API**: Built-in API for monitoring and configuration```bash

- 📈 **Real-time Monitoring**: Progress tracking with ETA and statistics

- 🛡️ **Robust Error Handling**: Automatic handling of corrupted files and permissionscd backend_python

- ⏱️ **Periodic Execution**: Configurable automatic scanning intervals

- 🎯 **Performance Optimized**: Smart skipping of unchanged files### 🚀 Quick Start

- 🌐 **REST API**: Built-in API for monitoring and configuration

# Quick setup (recommended)

### 🚀 Quick Start

#### Prerequisitessetup_venv.bat  # Windows

#### Prerequisites

# or

- Python 3.12+

- PostgreSQL 12+- Python 3.12+./setup_venv.sh  # Linux/Mac

- Network access to NAS

- PostgreSQL 12+

#### Installation

- Network access to NAS# Then run

**Option 1: Automatic Setup (Recommended)**

python main.py

```bash

# Windows#### Installation```

setup_venv.bat



# Linux/Mac

chmod +x setup_venv.sh**Option 1: Automatic Setup (Recommended)**### Configuration

./setup_venv.sh

```



**Option 2: Manual Installation**```bashAll settings are stored in the database `configurations` table:



```bash# Windows

# Create virtual environment

python -m venv venvsetup_venv.bat| Key | Default | Description |



# Activate virtual environment|-----|---------|-------------|

# Windows

venv\Scripts\activate# Linux/Mac| `nas_directory` | `\\NAS\scanner` | NAS directory path |

# Linux/Mac

source venv/bin/activatechmod +x setup_venv.sh| `scan_interval` | `10` | Seconds between scans |



# Install dependencies./setup_venv.sh| `exclude_extensions` | `[".tmp", ".bak"]` | File extensions to exclude |

pip install -r requirements.txt

``````| `scan_type` | `full` | `full` or `range` |



#### Running the Service| `scan_days_back` | `30` | Days for range scan |



```bash**Option 2: Manual Installation**

# Windows

start.bat### Documentation



# Linux/Mac```bash

./start.sh

# Create virtual environment- [📡 API Documentation](./API_DOCUMENTATION.md)

# Or directly

python main.pypython -m venv venv- [🇮🇹 Documentazione Italiana](./README_IT.md)

```

- [🇬🇧 English Documentation](./README_EN.md)

### 📋 Configuration

# Activate virtual environment

The system uses a PostgreSQL `configurations` table for all settings:

# Windows### License

| Key | Type | Default | Description |

|-----|------|---------|-------------|venv\Scripts\activate

| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | NAS directory to scan |

| `scan_interval` | integer | `10` | Interval in seconds between scans |# Linux/MacMIT License

| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | File extensions to exclude |

| `periodically_scan` | boolean | `true` | Enable periodic scanning |source venv/bin/activate

| `scan_type` | enum | `full` | Scan type: `full` or `range` |

| `scan_days_back` | integer | `30` | Days to scan back (for `range` mode) |# Install dependencies

pip install -r requirements.txt

### 🗄️ Database Structure```



```sql#### Running the Service

-- Files table

CREATE TABLE files (```bash

    id SERIAL PRIMARY KEY,# Windows

    filename TEXT NOT NULL,start.bat

    directory TEXT NOT NULL,

    last_modified TIMESTAMP NOT NULL,# Linux/Mac

    UNIQUE(filename, directory)./start.sh

);

# Or directly

-- Folders tablepython main.py

CREATE TABLE folders (```

    id SERIAL PRIMARY KEY,

    path TEXT NOT NULL UNIQUE,### 📋 Configuration

    last_modified TIMESTAMP NOT NULL

);The system uses a PostgreSQL `configurations` table for all settings:



-- Configurations table| Key | Type | Default | Description |

CREATE TABLE configurations (|-----|------|---------|-------------|

    id SERIAL PRIMARY KEY,| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | NAS directory to scan |

    key TEXT NOT NULL UNIQUE,| `scan_interval` | integer | `10` | Interval in seconds between scans |

    value TEXT NOT NULL,| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | File extensions to exclude |

    description TEXT,| `periodically_scan` | boolean | `true` | Enable periodic scanning |

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP| `scan_type` | enum | `full` | Scan type: `full` or `range` |

);| `scan_days_back` | integer | `30` | Days to scan back (for `range` mode) |

```

### 🗄️ Database Structure

### 📊 Scan Modes

```sql

#### Full Scan-- Files table

Scans all NAS folders and files on each execution.CREATE TABLE files (

    id SERIAL PRIMARY KEY,

```sql    filename TEXT NOT NULL,

UPDATE configurations SET value = 'full' WHERE key = 'scan_type';    directory TEXT NOT NULL,

```    last_modified TIMESTAMP NOT NULL,

    UNIQUE(filename, directory)

#### Range Scan (Incremental));

Scans only folders modified in the last N days (much faster).

-- Folders table

```sqlCREATE TABLE folders (

UPDATE configurations SET value = 'range' WHERE key = 'scan_type';    id SERIAL PRIMARY KEY,

UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';    path TEXT NOT NULL UNIQUE,

```    last_modified TIMESTAMP NOT NULL

);

### 🌐 REST API

-- Configurations table

The service includes a built-in REST API running on `http://localhost:5000`:CREATE TABLE configurations (

    id SERIAL PRIMARY KEY,

- `GET /api/health` - Health check    key TEXT NOT NULL UNIQUE,

- `GET /api/statistics` - System statistics    value TEXT NOT NULL,

- `GET /api/configurations` - Get all configurations    description TEXT,

- `PUT /api/configurations/{key}` - Update configuration    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

- `GET /api/scan/status` - Current scan status);

```

See [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for full details.

### 📊 Scan Modes

### 📈 Example Output

#### Full Scan

```Scans all NAS folders and files on each execution.

Loaded configurations:

  - NAS Directory: \\<NAS_IP>\<SHARE>\<FOLDER>```sql

  - Scan interval: 10 secondsUPDATE configurations SET value = 'full' WHERE key = 'scan_type';

  - Excluded extensions: ['.tmp', '.bak']```

  - Periodic scan: True

  - Scan type: range#### Range Scan (Incremental)

  - Time range: last 30 daysScans only folders modified in the last N days (much faster).



Scan mode: RANGE (last 30 days, from date: 2025-09-02 00:00:00)```sql

Folders to scan in range: 127UPDATE configurations SET value = 'range' WHERE key = 'scan_type';

Total files in database: 316619UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';

```

Scan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8

### 🌐 REST API

Scan completed:

  - Total time: 00:40:33The service includes a built-in REST API running on `http://localhost:5000`:

  - Files scanned: 316619/316619

  - Files inserted (new): 45- `GET /api/health` - Health check

  - Files updated: 23- `GET /api/statistics` - System statistics

  - Files skipped (unchanged): 316551- `GET /api/configurations` - Get all configurations

```- `PUT /api/configurations/{key}` - Update configuration

- `GET /api/scan/status` - Current scan status

### 🛠️ Architecture

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full details.

- **Main Thread**: Handles periodic NAS scanning

- **API Thread**: Runs Flask REST API (daemon thread)### 📈 Example Output

- **Dual Database**: PostgreSQL for data + SQLite for configurations

```

### 📚 DocumentationLoaded configurations:

  - NAS Directory: \\<NAS_IP>\<SHARE>\<FOLDER>

- [Full English Documentation](docs/README_EN.md)  - Scan interval: 10 seconds

- [API Documentation](docs/API_DOCUMENTATION.md)  - Excluded extensions: ['.tmp', '.bak']

- [Italian Documentation](docs/README_IT.md)  - Periodic scan: True

  - Scan type: range

### 📝 License  - Time range: last 30 days



MIT LicenseScan mode: RANGE (last 30 days, from date: 2025-09-02 00:00:00)

Folders to scan in range: 127

---Total files in database: 316619



## 🇮🇹 Versione ItalianaScan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8



### DescrizioneScan completed:

  - Total time: 00:40:33

NAS Directory Scanner è un servizio Python robusto progettato per monitorare e indicizzare directory su NAS. Esegue scansioni ricorsive, salvando metadati completi di file e cartelle in PostgreSQL con supporto per scansioni complete e incrementali basate su range temporali.  - Files scanned: 316619/316619

  - Files inserted (new): 45

### ✨ Caratteristiche Principali  - Files updated: 23

  - Files skipped (unchanged): 316551

- 🔄 **Scansione Ricorsiva**: Attraversamento completo delle directory NAS con sottocartelle```

- 📊 **Archiviazione PostgreSQL**: Storage strutturato con timestamp e metadati

- ⚡ **Scansioni Incrementali**: Modalità range temporale per cartelle modificate### 🛠️ Architecture

- 🔧 **Configurazione Dinamica**: Impostazioni guidate dal database (nessuna modifica al codice)

- 📈 **Monitoraggio Real-time**: Tracking progresso con ETA e statistiche- **Main Thread**: Handles periodic NAS scanning

- 🛡️ **Gestione Errori Robusta**: Gestione automatica di file corrotti e permessi- **API Thread**: Runs Flask REST API (daemon thread)

- ⏱️ **Esecuzione Periodica**: Intervalli di scansione automatica configurabili- **Dual Database**: PostgreSQL for data + SQLite for configurations

- 🎯 **Ottimizzato per Performance**: Skip intelligente di file non modificati

- 🌐 **REST API**: API integrata per monitoraggio e configurazione### 📝 License



### 🚀 Avvio RapidoMIT License



#### Prerequisiti---



- Python 3.12+## 🇮🇹 Versione Italiana

- PostgreSQL 12+

- Accesso di rete al NAS### Descrizione



#### InstallazioneNAS Directory Scanner è un servizio Python robusto progettato per monitorare e indicizzare directory su NAS. Esegue scansioni ricorsive, salvando metadati completi di file e cartelle in PostgreSQL con supporto per scansioni complete e incrementali basate su range temporali.



**Opzione 1: Setup Automatico (Raccomandato)**### ✨ Caratteristiche Principali



```bash- 🔄 **Scansione Ricorsiva**: Attraversamento completo delle directory NAS con sottocartelle

# Windows- 📊 **Archiviazione PostgreSQL**: Storage strutturato con timestamp e metadati

setup_venv.bat- ⚡ **Scansioni Incrementali**: Modalità range temporale per cartelle modificate

- 🔧 **Configurazione Dinamica**: Impostazioni guidate dal database (nessuna modifica al codice)

# Linux/Mac- 📈 **Monitoraggio Real-time**: Tracking progresso con ETA e statistiche

chmod +x setup_venv.sh- 🛡️ **Gestione Errori Robusta**: Gestione automatica di file corrotti e permessi

./setup_venv.sh- ⏱️ **Esecuzione Periodica**: Intervalli di scansione automatica configurabili

```- 🎯 **Ottimizzato per Performance**: Skip intelligente di file non modificati

- 🌐 **REST API**: API integrata per monitoraggio e configurazione

**Opzione 2: Installazione Manuale**

### 🚀 Avvio Rapido

```bash

# Crea virtual environment#### Prerequisiti

python -m venv venv

- Python 3.12+

# Attiva virtual environment- PostgreSQL 12+

# Windows- Accesso di rete al NAS

venv\Scripts\activate

# Linux/Mac#### Installazione

source venv/bin/activate

**Opzione 1: Setup Automatico (Raccomandato)**

# Installa dipendenze

pip install -r requirements.txt```bash

```# Windows

setup_venv.bat

#### Esecuzione del Servizio

# Linux/Mac

```bashchmod +x setup_venv.sh

# Windows./setup_venv.sh

start.bat```



# Linux/Mac**Opzione 2: Installazione Manuale**

./start.sh

```bash

# Oppure direttamente# Crea virtual environment

python main.pypython -m venv venv

```

# Attiva virtual environment

### 📋 Configurazione# Windows

venv\Scripts\activate

Il sistema utilizza una tabella PostgreSQL `configurations` per tutte le impostazioni:# Linux/Mac

source venv/bin/activate

| Chiave | Tipo | Default | Descrizione |

|--------|------|---------|-------------|# Installa dipendenze

| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | Directory del NAS da scansionare |pip install -r requirements.txt

| `scan_interval` | integer | `10` | Intervallo in secondi tra le scansioni |```

| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | Estensioni file da escludere |

| `periodically_scan` | boolean | `true` | Abilita scansione periodica |#### Esecuzione del Servizio

| `scan_type` | enum | `full` | Tipo scansione: `full` o `range` |

| `scan_days_back` | integer | `30` | Giorni da scansionare (modalità `range`) |```bash

# Windows

### 🗄️ Struttura Databasestart.bat



```sql# Linux/Mac

-- Tabella file./start.sh

CREATE TABLE files (

    id SERIAL PRIMARY KEY,# Oppure direttamente

    filename TEXT NOT NULL,python main.py

    directory TEXT NOT NULL,```

    last_modified TIMESTAMP NOT NULL,

    UNIQUE(filename, directory)### 📋 Configurazione

);

Il sistema utilizza una tabella PostgreSQL `configurations` per tutte le impostazioni:

-- Tabella cartelle

CREATE TABLE folders (| Chiave | Tipo | Default | Descrizione |

    id SERIAL PRIMARY KEY,|--------|------|---------|-------------|

    path TEXT NOT NULL UNIQUE,| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | Directory del NAS da scansionare |

    last_modified TIMESTAMP NOT NULL| `scan_interval` | integer | `10` | Intervallo in secondi tra le scansioni |

);| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | Estensioni file da escludere |

| `periodically_scan` | boolean | `true` | Abilita scansione periodica |

-- Tabella configurazioni| `scan_type` | enum | `full` | Tipo scansione: `full` o `range` |

CREATE TABLE configurations (| `scan_days_back` | integer | `30` | Giorni da scansionare (modalità `range`) |

    id SERIAL PRIMARY KEY,

    key TEXT NOT NULL UNIQUE,### 🗄️ Struttura Database

    value TEXT NOT NULL,

    description TEXT,```sql

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP-- Tabella file

);CREATE TABLE files (

```    id SERIAL PRIMARY KEY,

    filename TEXT NOT NULL,

### 📊 Modalità di Scansione    directory TEXT NOT NULL,

    last_modified TIMESTAMP NOT NULL,

#### Scansione Completa    UNIQUE(filename, directory)

Scansiona tutte le cartelle e file del NAS ad ogni esecuzione.);



```sql-- Tabella cartelle

UPDATE configurations SET value = 'full' WHERE key = 'scan_type';CREATE TABLE folders (

```    id SERIAL PRIMARY KEY,

    path TEXT NOT NULL UNIQUE,

#### Scansione Range (Incrementale)    last_modified TIMESTAMP NOT NULL

Scansiona solo le cartelle modificate negli ultimi N giorni (molto più veloce).);



```sql-- Tabella configurazioni

UPDATE configurations SET value = 'range' WHERE key = 'scan_type';CREATE TABLE configurations (

UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';    id SERIAL PRIMARY KEY,

```    key TEXT NOT NULL UNIQUE,

    value TEXT NOT NULL,

### 🌐 REST API    description TEXT,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Il servizio include un'API REST integrata su `http://localhost:5000`:);

```

- `GET /api/health` - Controllo stato

- `GET /api/statistics` - Statistiche sistema### 📊 Modalità di Scansione

- `GET /api/configurations` - Ottieni tutte le configurazioni

- `PUT /api/configurations/{key}` - Aggiorna configurazione#### Scansione Completa

- `GET /api/scan/status` - Stato scansione correnteScansiona tutte le cartelle e file del NAS ad ogni esecuzione.



Vedi [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) per dettagli completi.```sql

UPDATE configurations SET value = 'full' WHERE key = 'scan_type';

### 📈 Output Esempio```



```#### Scansione Range (Incrementale)

Configurazioni caricate:Scansiona solo le cartelle modificate negli ultimi N giorni (molto più veloce).

  - Directory NAS: \\<NAS_IP>\<SHARE>\<FOLDER>

  - Intervallo scansione: 10 secondi```sql

  - Estensioni escluse: ['.tmp', '.bak']UPDATE configurations SET value = 'range' WHERE key = 'scan_type';

  - Scansione periodica: TrueUPDATE configurations SET value = '30' WHERE key = 'scan_days_back';

  - Tipo scansione: range```

  - Range temporale: ultimi 30 giorni

### 🌐 REST API

Modalità scansione: RANGE (ultimi 30 giorni, dalla data: 2025-09-02 00:00:00)

Cartelle da scansionare nel range: 127Il servizio include un'API REST integrata su `http://localhost:5000`:

File totali nel database: 316619

- `GET /api/health` - Controllo stato

Scan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8- `GET /api/statistics` - Statistiche sistema

- `GET /api/configurations` - Ottieni tutte le configurazioni

Scansione completata:- `PUT /api/configurations/{key}` - Aggiorna configurazione

  - Tempo totale: 00:40:33- `GET /api/scan/status` - Stato scansione corrente

  - File scansionati: 316619/316619

  - File inseriti (nuovi): 45Vedi [API_DOCUMENTATION.md](API_DOCUMENTATION.md) per dettagli completi.

  - File aggiornati: 23

  - File saltati (non modificati): 316551### 📈 Output Esempio

```

```

### 🛠️ ArchitetturaConfigurazioni caricate:

  - Directory NAS: \\<NAS_IP>\<SHARE>\<FOLDER>

- **Thread Principale**: Gestisce la scansione periodica del NAS  - Intervallo scansione: 10 secondi

- **Thread API**: Esegue l'API REST Flask (daemon thread)  - Estensioni escluse: ['.tmp', '.bak']

- **Database Doppio**: PostgreSQL per dati + SQLite per configurazioni  - Scansione periodica: True

  - Tipo scansione: range

### 📚 Documentazione  - Range temporale: ultimi 30 giorni



- [Documentazione Completa Italiana](docs/README_IT.md)Modalità scansione: RANGE (ultimi 30 giorni, dalla data: 2025-09-02 00:00:00)

- [Documentazione API](docs/API_DOCUMENTATION.md)Cartelle da scansionare nel range: 127

- [English Documentation](docs/README_EN.md)File totali nel database: 316619



### 📝 LicenzaScan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8



MIT LicenseScansione completata:

  - Tempo totale: 00:40:33

---  - File scansionati: 316619/316619

  - File inseriti (nuovi): 45

## 🤝 Contributing  - File aggiornati: 23

  - File saltati (non modificati): 316551

Contributions are welcome! Please feel free to submit a Pull Request.```



## 📧 Support### 🛠️ Architettura



For issues and questions, please open an issue on GitHub.- **Thread Principale**: Gestisce la scansione periodica del NAS

- **Thread API**: Esegue l'API REST Flask (daemon thread)
- **Database Doppio**: PostgreSQL per dati + SQLite per configurazioni

### 📝 Licenza

MIT License

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.
