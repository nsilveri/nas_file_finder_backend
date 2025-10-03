# NAS Directory Scanner - Backend Python

## 🇬🇧 English Version

### Description

NAS Directory Scanner is a Python service that performs recursive scanning of NAS directories, saving file and folder information to a PostgreSQL database. The system offers complete or incremental scans based on time ranges, with dynamic configuration through SQLite (config.db).

### Main Features

- ✅ **Recursive Scanning**: Complete NAS directory scan with all subdirectories
- 📊 **PostgreSQL Database**: Structured storage of files and folders with timestamps
- ⚡ **Incremental Scans**: Time range mode to scan only recently modified folders
- 🔧 **Dynamic Configuration**: All settings configurable via database
- 📈 **Real-time Monitoring**: Progress bar, statistics, and estimated time remaining
- 🛡️ **Robust Error Handling**: Automatic handling of corrupted files, invalid paths, and permission errors
- ⏱️ **Periodic Scanning**: Automatic execution at configurable intervals
- 🎯 **Performance Optimizations**: Skips already updated files to reduce database writes

### Requirements

- Python 3.12+
- PostgreSQL 12+
- Network access to NAS

### Installation

```bash
# Clone the repository
cd backend_python

# OPTION 1: Automatic setup with virtual environment (RECOMMENDED)
# Windows
setup_venv.bat

# Linux/Mac
chmod +x setup_venv.sh
./setup_venv.sh

# OPTION 2: Manual installation
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

The system uses **SQLite (config.db)** to manage all settings:

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `nas_directory` | string | `\\<NAS_IP>\<SHARE>\<FOLDER>` | NAS directory to scan |
| `scan_interval` | integer | `10` | Interval in seconds between scans |
| `exclude_extensions` | JSON array | `[".tmp", ".bak"]` | File extensions to exclude |
| `periodically_scan` | boolean | `true` | Enable periodic scanning |
| `scan_type` | enum | `full` | Scan type: `full` or `range` |
| `scan_days_back` | integer | `30` | Days to scan (for `range` only) |
| `db_host` | string | - | PostgreSQL server address |
| `db_port` | integer | `5432` | PostgreSQL port |
| `db_name` | string | `nas_scanner` | PostgreSQL database name |
| `db_user` | string | - | PostgreSQL username |
| `db_password` | string | - | PostgreSQL password |

### Database Structure

**PostgreSQL (nas_scanner) - Data Storage:**

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
```

**SQLite (config.db) - Configuration Storage:**

All system configurations are stored locally in `config.db`:
- Scanner settings (directory, interval, exclusions)
- Scan mode configuration (full/range)
- PostgreSQL connection credentials
- Updated automatically at runtime

### Usage

```bash
# Activate virtual environment (if not already active)
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Run the service
python main.py
```

### Scan Modes

#### Full Scan (`scan_type = 'full'`)
Scans all NAS folders and files on each execution.

```sql
-- Update via SQLite config.db
UPDATE configurations SET value = 'full' WHERE key = 'scan_type';
```

Or use the API:
```bash
curl -X PUT http://localhost:5050/api/configurations/scan_type \
  -H "Content-Type: application/json" \
  -d '{"value": "full"}'
```

#### Range Scan (`scan_type = 'range'`)
Scans only folders modified in the last N days.

```sql
-- Update via SQLite config.db
UPDATE configurations SET value = 'range' WHERE key = 'scan_type';
UPDATE configurations SET value = '30' WHERE key = 'scan_days_back';  -- Last 30 days
```

Or use the API:
```bash
curl -X PUT http://localhost:5050/api/configurations/scan_type \
  -H "Content-Type: application/json" \
  -d '{"value": "range"}'
```

### Example Output

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

--- Partial Summary ---
  - Files scanned: 209692/316619 (66.2%)
  - Elapsed time: 25m 10s
  - Estimated time remaining: 00:15:23
  - Files inserted (new): 45
  - Files updated: 23
  - Files skipped (already updated): 209624
  - New folders: 12
  - Updated folders: 8
------------------------

Scan completed:
  - Scan type: RANGE
  - Time range: last 30 days
  - Start date: 2025-09-02 00:00:00
  - Folders in range: 127
  - Folders skipped (out of range): 1523
  - Total time: 00:40:33
  - Files scanned: 316619/316619
  - Files inserted (new): 45
  - Files updated: 23
  - Files skipped (already updated): 316551
  - New folders: 12
  - Updated folders: 115
```

### Utility Functions

The `utility_folders.py` module includes helper functions:

- `scan_folders_only()`: Initial folder-only scan
- `compare_folder_db_vs_nas()`: Compare DB with filesystem
- `compare_subfolders_db_vs_nas()`: Recursive subfolder comparison
- `truncate_last_modified_to_seconds()`: Timestamp normalization

### Error Handling

The system automatically handles:
- ❌ Files with invalid paths
- ❌ Special characters in filenames
- ❌ Paths too long (>260 characters on Windows)
- ❌ Corrupted or out-of-range timestamps
- ❌ Permission denied errors

### Performance

- **Pre-write Check**: Verifies if file is already updated before writing to DB
- **Incremental Scans**: Range mode to reduce load
- **Batch Updates**: Single commit at scan completion
- **Smart Skip**: Skips already processed files with same `last_modified`

### Frontend Configuration

Example REST API for frontend:

```python
# GET /api/config - Get all configurations
{
  "nas_directory": "\\\\<NAS_IP>\\<SHARE>\\<FOLDER>",
  "scan_interval": 10,
  "exclude_extensions": [".tmp", ".bak"],
  "periodically_scan": true,
  "scan_type": "range",
  "scan_days_back": 30
}

# PUT /api/config - Update configurations
{
  "scan_type": "range",
  "scan_days_back": 7
}
```

### License

MIT License
