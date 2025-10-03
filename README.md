# NAS Directory Scanner - Backend Python# NAS Directory Scanner - Backend Python# NAS Directory Scanner - Backend Python# NAS Directory Scanner - Backend Python



A Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database with support for full and incremental scans.



[🇮🇹 Versione Italiana](#-versione-italiana) | [🇬🇧 English Version](#-english-version)A Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database with support for full and incremental scans.



---



## 📁 Project Structure[🇮🇹 Versione Italiana](#-versione-italiana) | [🇬🇧 English Version](#-english-version)A Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database with support for full and incremental scans.[🇮🇹 Versione Italiana](./README_IT.md) | [🇬🇧 English Version](./README_EN.md)



```

backend_python/

├── main.py                 # Main application entry point---

├── setup_venv.bat         # Windows setup script

├── setup_venv.sh          # Linux/Mac setup script

├── start.bat              # Windows start script

├── start.sh               # Linux/Mac start script## 📁 Project Structure[🇮🇹 Versione Italiana](#-versione-italiana) | [🇬🇧 English Version](#-english-version)---

├── requirements.txt       # Python dependencies

├── config.db              # SQLite configuration database

├── .gitignore            # Git ignore rules

├── .env.example          # Environment variables template```

├── src/                  # Source code modules

│   ├── __init__.pybackend_python/

│   ├── api_routes.py     # REST API endpoints

│   └── utility_folders.py # Utility functions├── main.py                 # Main application entry point---## Quick Start

├── docs/                 # Documentation

│   ├── API_DOCUMENTATION.md├── setup_venv.bat         # Windows setup script

│   ├── README_EN.md      # Extended English docs

│   └── README_IT.md      # Extended Italian docs├── setup_venv.sh          # Linux/Mac setup script

├── sql/                  # SQL scripts

│   └── init_db.sql       # Database initialization├── start.bat              # Windows start script

└── tests/                # Test files

    ├── __init__.py├── start.sh               # Linux/Mac start script## 🇬🇧 English Version### Description

    └── test_api.py       # API tests

```├── requirements.txt       # Python dependencies



---├── config.db              # SQLite configuration database



## 🇬🇧 English Version├── .gitignore            # Git ignore rules



### Description├── .env.example          # Environment variables template### DescriptionNAS Directory Scanner is a Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database.



NAS Directory Scanner is a robust Python service designed to monitor and index NAS directories. It performs recursive scans, storing comprehensive file and folder metadata in PostgreSQL with support for both complete and time-ranged incremental scans.├── src/                  # Source code modules



### ✨ Key Features│   ├── __init__.py



- 🔄 **Recursive Scanning**: Complete NAS directory traversal with subdirectories│   ├── api_routes.py     # REST API endpoints

- 📊 **PostgreSQL Storage**: Structured storage with timestamps and metadata

- ⚡ **Incremental Scans**: Time-range mode for modified folders only│   └── utility_folders.py # Utility functionsNAS Directory Scanner is a robust Python service designed to monitor and index NAS directories. It performs recursive scans, storing comprehensive file and folder metadata in PostgreSQL with support for both complete and time-ranged incremental scans.### Features

- 🔧 **Dynamic Configuration**: Database-driven settings (no code changes needed)

- 📈 **Real-time Monitoring**: Progress tracking with ETA and statistics├── docs/                 # Documentation

- 🛡️ **Robust Error Handling**: Automatic handling of corrupted files and permissions

- ⏱️ **Periodic Execution**: Configurable automatic scanning intervals│   ├── API_DOCUMENTATION.md

- 🎯 **Performance Optimized**: Smart skipping of unchanged files

- 🌐 **REST API**: Built-in API for monitoring and configuration (port 5050)│   ├── README_EN.md      # Extended English docs



### 🚀 Quick Start│   └── README_IT.md      # Extended Italian docs### ✨ Key Features- ✅ Recursive NAS directory scanning



#### Prerequisites├── sql/                  # SQL scripts



- Python 3.12+│   └── init_db.sql       # Database initialization- 📊 PostgreSQL database storage

- PostgreSQL 12+

- Network access to NAS└── tests/                # Test files



#### Installation    └── test_api.py       # API tests- 🔄 **Recursive Scanning**: Complete NAS directory traversal with subdirectories- ⚡ Incremental scans (time-range based)



**Option 1: Automatic Setup (Recommended)**```



```bash- 📊 **PostgreSQL Storage**: Structured storage with timestamps and metadata- 🔧 Dynamic database configuration

# Windows

setup_venv.bat---



# Linux/Mac- ⚡ **Incremental Scans**: Time-range mode for modified folders only- 📈 Real-time monitoring with progress tracking

chmod +x setup_venv.sh

./setup_venv.sh## 🇬🇧 English Version

```

- 🔧 **Dynamic Configuration**: Database-driven settings (no code changes needed)- 🛡️ Robust error handling

**Option 2: Manual Installation**

### Description

```bash

# Create virtual environment- 📈 **Real-time Monitoring**: Progress tracking with ETA and statistics- 🌐 REST API for monitoring and statistics

python -m venv venv

NAS Directory Scanner is a robust Python service designed to monitor and index NAS directories. It performs recursive scans, storing comprehensive file and folder metadata in PostgreSQL with support for both complete and time-ranged incremental scans.

# Activate virtual environment

# Windows- 🛡️ **Robust Error Handling**: Automatic handling of corrupted files and permissions

venv\Scripts\activate

# Linux/Mac### ✨ Key Features

source venv/bin/activate

- ⏱️ **Periodic Execution**: Configurable automatic scanning intervals### Installation

# Install dependencies

pip install -r requirements.txt- 🔄 **Recursive Scanning**: Complete NAS directory traversal with subdirectories

```

- 📊 **PostgreSQL Storage**: Structured storage with timestamps and metadata- 🎯 **Performance Optimized**: Smart skipping of unchanged files

#### Running the Service

- ⚡ **Incremental Scans**: Time-range mode for modified folders only

```bash

# Windows- 🔧 **Dynamic Configuration**: Database-driven settings (no code changes needed)- 🌐 **REST API**: Built-in API for monitoring and configuration```bash

start.bat

- 📈 **Real-time Monitoring**: Progress tracking with ETA and statistics

# Linux/Mac

./start.sh- 🛡️ **Robust Error Handling**: Automatic handling of corrupted files and permissionscd backend_python



# Or directly- ⏱️ **Periodic Execution**: Configurable automatic scanning intervals

python main.py

```- 🎯 **Performance Optimized**: Smart skipping of unchanged files### 🚀 Quick Start



### 📋 Configuration- 🌐 **REST API**: Built-in API for monitoring and configuration



The system uses a PostgreSQL `configurations` table for all settings:# Quick setup (recommended)



| Key | Type | Default | Description |### 🚀 Quick Start

|-----|------|---------|-------------|

| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | NAS directory to scan |#### Prerequisitessetup_venv.bat  # Windows

| `scan_interval` | integer | `10` | Interval in seconds between scans |

| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | File extensions to exclude |#### Prerequisites

| `periodically_scan` | boolean | `true` | Enable periodic scanning |

| `scan_type` | enum | `full` | Scan type: `full` or `range` |# or

| `scan_days_back` | integer | `30` | Days to scan back (for `range` mode) |

- Python 3.12+

### 🗄️ Database Structure

- PostgreSQL 12+- Python 3.12+./setup_venv.sh  # Linux/Mac

```sql

-- Files table- Network access to NAS

CREATE TABLE files (

    id SERIAL PRIMARY KEY,- PostgreSQL 12+

    filename TEXT NOT NULL,

    directory TEXT NOT NULL,#### Installation

    last_modified TIMESTAMP NOT NULL,

    UNIQUE(filename, directory)- Network access to NAS# Then run

);

**Option 1: Automatic Setup (Recommended)**

-- Folders table

CREATE TABLE folders (python main.py

    id SERIAL PRIMARY KEY,

    path TEXT NOT NULL UNIQUE,```bash

    last_modified TIMESTAMP NOT NULL

);# Windows#### Installation```



-- Configurations tablesetup_venv.bat

CREATE TABLE configurations (

    id SERIAL PRIMARY KEY,

    key TEXT NOT NULL UNIQUE,

    value TEXT NOT NULL,# Linux/Mac

    description TEXT,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMPchmod +x setup_venv.sh**Option 1: Automatic Setup (Recommended)**### Configuration

);

```./setup_venv.sh



### 📊 Scan Modes```



#### Full Scan

Scans all NAS folders and files on each execution.

**Option 2: Manual Installation**```bashAll settings are stored in the database `configurations` table:

```sql

UPDATE configurations SET value = 'full' WHERE key = 'scan_type';

```

```bash# Windows

#### Range Scan (Incremental)

Scans only folders modified in the last N days (much faster).# Create virtual environment



```sqlpython -m venv venvsetup_venv.bat| Key | Default | Description |

UPDATE configurations SET value = 'range' WHERE key = 'scan_type';

UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';

```

# Activate virtual environment|-----|---------|-------------|

### 🌐 REST API

# Windows

The service includes a built-in REST API running on `http://localhost:5050`:

venv\Scripts\activate# Linux/Mac| `nas_directory` | `\\NAS\scanner` | NAS directory path |

**Available Endpoints:**

- `GET /api/health` - Health check# Linux/Mac

- `GET /api/statistics` - System statistics

- `GET /api/configurations` - Get all configurationssource venv/bin/activatechmod +x setup_venv.sh| `scan_interval` | `10` | Seconds between scans |

- `PUT /api/configurations/{key}` - Update configuration

- `GET /api/scan/status` - Current scan status



**LAN Access:**# Install dependencies./setup_venv.sh| `exclude_extensions` | `[".tmp", ".bak"]` | File extensions to exclude |



The API is accessible from other devices on the network:pip install -r requirements.txt

```

http://<SERVER_IP>:5050/api/health``````| `scan_type` | `full` | `full` or `range` |

http://<SERVER_IP>:5050/api/statistics

```



See [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for full API details.#### Running the Service| `scan_days_back` | `30` | Days for range scan |



### 📈 Example Output



``````bash**Option 2: Manual Installation**

Loaded configurations:

  - NAS Directory: \\<NAS_IP>\<SHARE>\<FOLDER># Windows

  - Scan interval: 10 seconds

  - Excluded extensions: ['.tmp', '.bak']start.bat### Documentation

  - Periodic scan: True

  - Scan type: range

  - Time range: last 30 days

# Linux/Mac```bash

Scan mode: RANGE (last 30 days, from date: 2025-09-02 00:00:00)

Folders to scan in range: 127./start.sh

Total files in database: 316619

# Create virtual environment- [📡 API Documentation](./API_DOCUMENTATION.md)

Scan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8

# Or directly

Scan completed:

  - Total time: 00:40:33python main.pypython -m venv venv- [🇮🇹 Documentazione Italiana](./README_IT.md)

  - Files scanned: 316619/316619

  - Files inserted (new): 45```

  - Files updated: 23

  - Files skipped (unchanged): 316551- [🇬🇧 English Documentation](./README_EN.md)

```

### 📋 Configuration

### 🛠️ Architecture

# Activate virtual environment

- **Main Thread**: Handles periodic NAS scanning

- **API Thread**: Runs Flask REST API on port 5050 (daemon thread)The system uses a PostgreSQL `configurations` table for all settings:

- **Dual Database**: PostgreSQL for data + SQLite for configurations

# Windows### License

### 📚 Documentation

| Key | Type | Default | Description |

- [Full English Documentation](docs/README_EN.md)

- [API Documentation](docs/API_DOCUMENTATION.md)|-----|------|---------|-------------|venv\Scripts\activate

- [Italian Documentation](docs/README_IT.md)

| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | NAS directory to scan |

### 📝 License

| `scan_interval` | integer | `10` | Interval in seconds between scans |# Linux/MacMIT License

MIT License

| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | File extensions to exclude |

---

| `periodically_scan` | boolean | `true` | Enable periodic scanning |source venv/bin/activate

## 🇮🇹 Versione Italiana

| `scan_type` | enum | `full` | Scan type: `full` or `range` |

### Descrizione

| `scan_days_back` | integer | `30` | Days to scan back (for `range` mode) |# Install dependencies

NAS Directory Scanner è un servizio Python robusto progettato per monitorare e indicizzare directory su NAS. Esegue scansioni ricorsive, salvando metadati completi di file e cartelle in PostgreSQL con supporto per scansioni complete e incrementali basate su range temporali.

pip install -r requirements.txt

### ✨ Caratteristiche Principali

### 🗄️ Database Structure```

- 🔄 **Scansione Ricorsiva**: Attraversamento completo delle directory NAS con sottocartelle

- 📊 **Archiviazione PostgreSQL**: Storage strutturato con timestamp e metadati

- ⚡ **Scansioni Incrementali**: Modalità range temporale per cartelle modificate

- 🔧 **Configurazione Dinamica**: Impostazioni guidate dal database (nessuna modifica al codice)```sql#### Running the Service

- 📈 **Monitoraggio Real-time**: Tracking progresso con ETA e statistiche

- 🛡️ **Gestione Errori Robusta**: Gestione automatica di file corrotti e permessi-- Files table

- ⏱️ **Esecuzione Periodica**: Intervalli di scansione automatica configurabili

- 🎯 **Ottimizzato per Performance**: Skip intelligente di file non modificatiCREATE TABLE files (```bash

- 🌐 **REST API**: API integrata per monitoraggio e configurazione (porta 5050)

    id SERIAL PRIMARY KEY,# Windows

### 🚀 Avvio Rapido

    filename TEXT NOT NULL,start.bat

#### Prerequisiti

    directory TEXT NOT NULL,

- Python 3.12+

- PostgreSQL 12+    last_modified TIMESTAMP NOT NULL,# Linux/Mac

- Accesso di rete al NAS

    UNIQUE(filename, directory)./start.sh

#### Installazione

);

**Opzione 1: Setup Automatico (Raccomandato)**

# Or directly

```bash

# Windows-- Folders tablepython main.py

setup_venv.bat

CREATE TABLE folders (```

# Linux/Mac

chmod +x setup_venv.sh    id SERIAL PRIMARY KEY,

./setup_venv.sh

```    path TEXT NOT NULL UNIQUE,### 📋 Configuration



**Opzione 2: Installazione Manuale**    last_modified TIMESTAMP NOT NULL



```bash);The system uses a PostgreSQL `configurations` table for all settings:

# Crea virtual environment

python -m venv venv



# Attiva virtual environment-- Configurations table| Key | Type | Default | Description |

# Windows

venv\Scripts\activateCREATE TABLE configurations (|-----|------|---------|-------------|

# Linux/Mac

source venv/bin/activate    id SERIAL PRIMARY KEY,| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | NAS directory to scan |



# Installa dipendenze    key TEXT NOT NULL UNIQUE,| `scan_interval` | integer | `10` | Interval in seconds between scans |

pip install -r requirements.txt

```    value TEXT NOT NULL,| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | File extensions to exclude |



#### Esecuzione del Servizio    description TEXT,| `periodically_scan` | boolean | `true` | Enable periodic scanning |



```bash    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP| `scan_type` | enum | `full` | Scan type: `full` or `range` |

# Windows

start.bat);| `scan_days_back` | integer | `30` | Days to scan back (for `range` mode) |



# Linux/Mac```

./start.sh

### 🗄️ Database Structure

# Oppure direttamente

python main.py### 📊 Scan Modes

```

```sql

### 📋 Configurazione

#### Full Scan-- Files table

Il sistema utilizza una tabella PostgreSQL `configurations` per tutte le impostazioni:

Scans all NAS folders and files on each execution.CREATE TABLE files (

| Chiave | Tipo | Default | Descrizione |

|--------|------|---------|-------------|    id SERIAL PRIMARY KEY,

| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | Directory del NAS da scansionare |

| `scan_interval` | integer | `10` | Intervallo in secondi tra le scansioni |```sql    filename TEXT NOT NULL,

| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | Estensioni file da escludere |

| `periodically_scan` | boolean | `true` | Abilita scansione periodica |UPDATE configurations SET value = 'full' WHERE key = 'scan_type';    directory TEXT NOT NULL,

| `scan_type` | enum | `full` | Tipo scansione: `full` o `range` |

| `scan_days_back` | integer | `30` | Giorni da scansionare (modalità `range`) |```    last_modified TIMESTAMP NOT NULL,



### 🗄️ Struttura Database    UNIQUE(filename, directory)



```sql#### Range Scan (Incremental));

-- Tabella file

CREATE TABLE files (Scans only folders modified in the last N days (much faster).

    id SERIAL PRIMARY KEY,

    filename TEXT NOT NULL,-- Folders table

    directory TEXT NOT NULL,

    last_modified TIMESTAMP NOT NULL,```sqlCREATE TABLE folders (

    UNIQUE(filename, directory)

);UPDATE configurations SET value = 'range' WHERE key = 'scan_type';    id SERIAL PRIMARY KEY,



-- Tabella cartelleUPDATE configurations SET value = '30' WHERE key = 'scan_days_back';    path TEXT NOT NULL UNIQUE,

CREATE TABLE folders (

    id SERIAL PRIMARY KEY,```    last_modified TIMESTAMP NOT NULL

    path TEXT NOT NULL UNIQUE,

    last_modified TIMESTAMP NOT NULL);

);

### 🌐 REST API

-- Tabella configurazioni

CREATE TABLE configurations (-- Configurations table

    id SERIAL PRIMARY KEY,

    key TEXT NOT NULL UNIQUE,The service includes a built-in REST API running on `http://localhost:5000`:CREATE TABLE configurations (

    value TEXT NOT NULL,

    description TEXT,    id SERIAL PRIMARY KEY,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);- `GET /api/health` - Health check    key TEXT NOT NULL UNIQUE,

```

- `GET /api/statistics` - System statistics    value TEXT NOT NULL,

### 📊 Modalità di Scansione

- `GET /api/configurations` - Get all configurations    description TEXT,

#### Scansione Completa

Scansiona tutte le cartelle e file del NAS ad ogni esecuzione.- `PUT /api/configurations/{key}` - Update configuration    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP



```sql- `GET /api/scan/status` - Current scan status);

UPDATE configurations SET value = 'full' WHERE key = 'scan_type';

``````



#### Scansione Range (Incrementale)See [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for full details.

Scansiona solo le cartelle modificate negli ultimi N giorni (molto più veloce).

### 📊 Scan Modes

```sql

UPDATE configurations SET value = 'range' WHERE key = 'scan_type';### 📈 Example Output

UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';

```#### Full Scan



### 🌐 REST API```Scans all NAS folders and files on each execution.



Il servizio include un'API REST integrata su `http://localhost:5050`:Loaded configurations:



**Endpoint Disponibili:**  - NAS Directory: \\<NAS_IP>\<SHARE>\<FOLDER>```sql

- `GET /api/health` - Controllo stato

- `GET /api/statistics` - Statistiche sistema  - Scan interval: 10 secondsUPDATE configurations SET value = 'full' WHERE key = 'scan_type';

- `GET /api/configurations` - Ottieni tutte le configurazioni

- `PUT /api/configurations/{key}` - Aggiorna configurazione  - Excluded extensions: ['.tmp', '.bak']```

- `GET /api/scan/status` - Stato scansione corrente

  - Periodic scan: True

**Accesso LAN:**

  - Scan type: range#### Range Scan (Incremental)

L'API è accessibile da altri dispositivi in rete:

```  - Time range: last 30 daysScans only folders modified in the last N days (much faster).

http://<IP_SERVER>:5050/api/health

http://<IP_SERVER>:5050/api/statistics

```

Scan mode: RANGE (last 30 days, from date: 2025-09-02 00:00:00)```sql

Vedi [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) per dettagli completi sull'API.

Folders to scan in range: 127UPDATE configurations SET value = 'range' WHERE key = 'scan_type';

### 📈 Output Esempio

Total files in database: 316619UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';

```

Configurazioni caricate:```

  - Directory NAS: \\<NAS_IP>\<SHARE>\<FOLDER>

  - Intervallo scansione: 10 secondiScan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8

  - Estensioni escluse: ['.tmp', '.bak']

  - Scansione periodica: True### 🌐 REST API

  - Tipo scansione: range

  - Range temporale: ultimi 30 giorniScan completed:



Modalità scansione: RANGE (ultimi 30 giorni, dalla data: 2025-09-02 00:00:00)  - Total time: 00:40:33The service includes a built-in REST API running on `http://localhost:5000`:

Cartelle da scansionare nel range: 127

File totali nel database: 316619  - Files scanned: 316619/316619



Scan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8  - Files inserted (new): 45- `GET /api/health` - Health check



Scansione completata:  - Files updated: 23- `GET /api/statistics` - System statistics

  - Tempo totale: 00:40:33

  - File scansionati: 316619/316619  - Files skipped (unchanged): 316551- `GET /api/configurations` - Get all configurations

  - File inseriti (nuovi): 45

  - File aggiornati: 23```- `PUT /api/configurations/{key}` - Update configuration

  - File saltati (non modificati): 316551

```- `GET /api/scan/status` - Current scan status



### 🛠️ Architettura### 🛠️ Architecture



- **Thread Principale**: Gestisce la scansione periodica del NASSee [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full details.

- **Thread API**: Esegue l'API REST Flask sulla porta 5050 (daemon thread)

- **Database Doppio**: PostgreSQL per dati + SQLite per configurazioni- **Main Thread**: Handles periodic NAS scanning



### 📚 Documentazione- **API Thread**: Runs Flask REST API (daemon thread)### 📈 Example Output



- [Documentazione Completa Italiana](docs/README_IT.md)- **Dual Database**: PostgreSQL for data + SQLite for configurations

- [Documentazione API](docs/API_DOCUMENTATION.md)

- [English Documentation](docs/README_EN.md)```



### 📝 Licenza### 📚 DocumentationLoaded configurations:



MIT License  - NAS Directory: \\<NAS_IP>\<SHARE>\<FOLDER>



---- [Full English Documentation](docs/README_EN.md)  - Scan interval: 10 seconds



## 🤝 Contributing- [API Documentation](docs/API_DOCUMENTATION.md)  - Excluded extensions: ['.tmp', '.bak']



Contributions are welcome! Please feel free to submit a Pull Request.- [Italian Documentation](docs/README_IT.md)  - Periodic scan: True



## 📧 Support  - Scan type: range



For issues and questions, please open an issue on GitHub.### 📝 License  - Time range: last 30 days



---



## 🔧 Technical NotesMIT LicenseScan mode: RANGE (last 30 days, from date: 2025-09-02 00:00:00)



### Port ConfigurationFolders to scan in range: 127



The REST API runs on port **5050** (not the default Flask 5000) to avoid conflicts with:---Total files in database: 316619

- Other Flask applications

- AirPlay services (macOS)

- Other common development servers

## 🇮🇹 Versione ItalianaScan: 209692/316619 (66.2%) ETA:15m23s | Ins:45 Upd:23 Skip:209624 | Fold+:12 ~:8

### Network Access



The API server binds to `0.0.0.0`, making it accessible from:

- **Local machine**: `http://localhost:5050`### DescrizioneScan completed:

- **LAN devices**: `http://<server-ip>:5050`

  - Total time: 00:40:33

Find your server IP:

```bashNAS Directory Scanner è un servizio Python robusto progettato per monitorare e indicizzare directory su NAS. Esegue scansioni ricorsive, salvando metadati completi di file e cartelle in PostgreSQL con supporto per scansioni complete e incrementali basate su range temporali.  - Files scanned: 316619/316619

# Windows

ipconfig  - Files inserted (new): 45



# Linux/Mac### ✨ Caratteristiche Principali  - Files updated: 23

ifconfig

# or  - Files skipped (unchanged): 316551

ip addr show

```- 🔄 **Scansione Ricorsiva**: Attraversamento completo delle directory NAS con sottocartelle```



### Security Considerations- 📊 **Archiviazione PostgreSQL**: Storage strutturato con timestamp e metadati



⚠️ **Important**: The API currently has no authentication. For production use, consider:- ⚡ **Scansioni Incrementali**: Modalità range temporale per cartelle modificate### 🛠️ Architecture

- Adding API key authentication

- Implementing rate limiting- 🔧 **Configurazione Dinamica**: Impostazioni guidate dal database (nessuna modifica al codice)

- Using HTTPS with SSL certificates

- Restricting access via firewall rules- 📈 **Monitoraggio Real-time**: Tracking progresso con ETA e statistiche- **Main Thread**: Handles periodic NAS scanning

- Setting up a reverse proxy (nginx/Apache)

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
