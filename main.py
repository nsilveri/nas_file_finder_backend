from datetime import datetime
import os
import sys
import time
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from src.utility_folders import compare_subfolders_db_vs_nas
import threading
from flask import Flask
from flask_cors import CORS
import sqlite3
import json
from src.api_routes import register_routes

# SQLite configuration for local settings
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.db')

# Global variables for PostgreSQL database (loaded from SQLite at startup)
DB_HOST = None
DB_PORT = None
DB_USER = None
DB_PASSWORD = None
DB_NAME = None
NAS_DIR = None
PERIODICALLY_SCAN = True

# Flask API configuration
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

def get_db_connection():
    """Creates and returns a PostgreSQL database connection."""
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)


def get_sqlite_connection():
    """Creates and returns a SQLite database connection for configurations."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def run_flask_api():
    """Runs the Flask server in a separate thread."""
    # Register all API routes from external module
    register_routes(app, get_db_connection, get_sqlite_connection)
    
    print("\n" + "="*50)
    print("🌐 API REST Server started on http://0.0.0.0:5050")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=5050, debug=False, use_reloader=False)

def create_database_if_not_exists():
    """Creates the database if it doesn't exist."""
    conn = psycopg2.connect(dbname='postgres', user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f'CREATE DATABASE {DB_NAME}')
        print(f"Database '{DB_NAME}' created.")
    cur.close()
    conn.close()


def init_database_tables():
    """Executes the init_db.sql script to create tables."""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(script_dir, 'init_db.sql')
    
    if not os.path.exists(sql_file):
        print(f"WARNING: File {sql_file} not found!")
        return False
    
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        cur.execute(sql_script)
        conn.commit()
        cur.close()
        conn.close()
        print("Database tables initialized successfully from init_db.sql")
        return True
    except Exception as e:
        print(f"Error initializing tables: {e}")
        return False



def scan_and_save(directory, exclude_extensions=None, scan_type='full', scan_days_back=30):
    """Scans all NAS content and saves to database.
    
    Args:
        directory: Directory to scan
        exclude_extensions: List of file extensions to exclude
        scan_type: 'full' for complete scan, 'range' for time-based scan
        scan_days_back: Number of days back for range scan (default: 30)
    """
    if exclude_extensions is None:
        exclude_extensions = []
    from datetime import datetime, timedelta
    import sys
    
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    
    # Scan counters
    files_scanned = 0
    files_total = 0
    files_inserted = 0
    files_updated = 0
    files_skipped = 0
    folders_inserted = 0
    folders_updated = 0
    folders_skipped = 0
    last_print_time = time.time()
    scan_start_time = time.time()  # Scan start time
    print_interval = 5  # Print summary every 5 seconds
    
    # Determine folders to scan based on scan type
    folders_to_scan = set()
    scan_from_date = None
    
    if scan_type == 'range':
        # Calculate start date from number of days
        scan_from_date = datetime.now() - timedelta(days=scan_days_back)
        print(f"Scan mode: RANGE (last {scan_days_back} days, from date: {scan_from_date.strftime('%Y-%m-%d %H:%M:%S')})")
        # Retrieve only folders modified after specified date
        cur.execute("""
            SELECT path FROM folders 
            WHERE last_modified >= %s
            ORDER BY last_modified DESC
        """, (scan_from_date,))
        folders_to_scan = set(row[0] for row in cur.fetchall())
        print(f"Folders to scan in range: {len(folders_to_scan)}")
    else:
        print("Scan mode: FULL")
        scan_type = 'full'  # Force full if no valid parameters
    
    # Count total files from database (much faster)
    print("Counting total files from database...", end='', flush=True)
    if scan_type == 'range' and folders_to_scan:
        # Count only files in range folders
        placeholders = ','.join(['%s'] * len(folders_to_scan))
        cur.execute(f"SELECT COUNT(*) FROM files WHERE directory IN ({placeholders})", tuple(folders_to_scan))
    else:
        cur.execute("SELECT COUNT(*) FROM files")
    result = cur.fetchone()
    files_total = result[0] if result else 0
    print(f"\rTotal files in database: {files_total}    ")
    
    for root, dirs, files in os.walk(directory):
        # If range scan, skip folders not in range
        if scan_type == 'range' and folders_to_scan and root not in folders_to_scan:
            folders_skipped += 1
            continue
        
        try:
            dir_mtime = os.path.getmtime(root)
            dir_mtime_dt = datetime.fromtimestamp(dir_mtime)
        except Exception:
            continue
        
        # Variable to track most recent file in folder
        most_recent_file_time = None
        folder_has_changes = False
        
        # Check if folder already exists in DB
        cur.execute("SELECT last_modified FROM folders WHERE path = %s", (root,))
        existing_folder = cur.fetchone()
        
        # Exclude directory if it contains at least one file with excluded extension
        if any(file.lower().endswith(tuple(exclude_extensions)) for file in files):
            continue
        
        # Scan all files in folder
        for file in files:
            file_path = os.path.join(root, file)
            try:
                last_modified = os.path.getmtime(file_path)
                last_modified_dt = datetime.fromtimestamp(last_modified)
            except (OSError, ValueError, OverflowError) as e:
                # Skip files with invalid paths or problematic timestamps
                # print(f"File access error {file_path}: {e}")
                continue
            
            files_scanned += 1
            
            # Print complete summary every N seconds
            current_time = time.time()
            if current_time - last_print_time >= print_interval:
                # Calculate estimated remaining time
                elapsed_time = current_time - scan_start_time
                if files_scanned > 0 and files_total > 0:
                    avg_time_per_file = elapsed_time / files_scanned
                    files_remaining = files_total - files_scanned
                    estimated_time_remaining = avg_time_per_file * files_remaining
                    
                    # Format remaining time
                    hours = int(estimated_time_remaining // 3600)
                    minutes = int((estimated_time_remaining % 3600) // 60)
                    seconds = int(estimated_time_remaining % 60)
                    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    time_str = "N/A"
                
                # New line and print summary
                print(f"\n\n--- Partial summary ---")
                print(f"  - Files scanned: {files_scanned}/{files_total} ({(files_scanned / files_total * 100) if files_total > 0 else 0:.1f}%)")
                print(f"  - Elapsed time: {int(elapsed_time // 60)}m {int(elapsed_time % 60)}s")
                print(f"  - Estimated remaining: {time_str}")
                print(f"  - Files inserted (new): {files_inserted}")
                print(f"  - Files updated: {files_updated}")
                print(f"  - Files skipped (already up-to-date): {files_skipped}")
                print(f"  - New folders: {folders_inserted}")
                print(f"  - Updated folders: {folders_updated}")
                print(f"------------------------")
                last_print_time = current_time
            
            # Print progress on same line (compact version)
            percentage = (files_scanned / files_total * 100) if files_total > 0 else 0
            
            # Calculate remaining time for compact display
            elapsed_time = current_time - scan_start_time
            if files_scanned > 0 and files_total > 0:
                avg_time_per_file = elapsed_time / files_scanned
                files_remaining = files_total - files_scanned
                estimated_time_remaining = avg_time_per_file * files_remaining
                eta_minutes = int(estimated_time_remaining // 60)
                eta_seconds = int(estimated_time_remaining % 60)
                eta_str = f"ETA:{eta_minutes}m{eta_seconds}s"
            else:
                eta_str = "ETA:N/A"
            
            # Use \r to return to line start and clear rest with spaces
            progress_msg = f"\rScan: {files_scanned}/{files_total} ({percentage:.1f}%) {eta_str} | Ins:{files_inserted} Upd:{files_updated} Skip:{files_skipped} | Fold+:{folders_inserted} ~:{folders_updated}"
            # Add spaces to clear any remaining characters from previous line
            sys.stdout.write(progress_msg + " " * 10)
            sys.stdout.flush()
            
            # Check if file already exists in DB with same last_modified
            cur.execute(
                "SELECT last_modified FROM files WHERE filename = %s AND directory = %s",
                (file, root)
            )
            existing_record = cur.fetchone()
            
            if existing_record:
                existing_last_modified = existing_record[0]
                # Round both timestamps to seconds for comparison
                if int(existing_last_modified.timestamp()) == int(last_modified):
                    # File already present and up-to-date, skip
                    files_skipped += 1
                else:
                    # File modified
                    files_updated += 1
                    folder_has_changes = True
            else:
                # New file
                files_inserted += 1
                folder_has_changes = True
            
            # Track most recent file in folder
            if most_recent_file_time is None or last_modified > most_recent_file_time:
                most_recent_file_time = last_modified
            
            # Execute INSERT/UPDATE only if file is new or modified
            if existing_record is None or int(existing_record[0].timestamp()) != int(last_modified):
                cur.execute(
                    sql.SQL("""
                        INSERT INTO files (filename, directory, last_modified)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (filename, directory) DO UPDATE SET last_modified = EXCLUDED.last_modified
                    """),
                    (file, root, last_modified_dt)
                )
        
        # Update folder with most recent file's last_modified if there were changes
        if most_recent_file_time is not None:
            try:
                folder_last_modified = datetime.fromtimestamp(most_recent_file_time)
            except (OSError, ValueError, OverflowError):
                # If timestamp is invalid, use directory timestamp
                folder_last_modified = dir_mtime_dt
        else:
            # If no files, use directory timestamp itself
            folder_last_modified = dir_mtime_dt
        
        # Update/Insert folder in folders table
        cur.execute(
            sql.SQL("""
                INSERT INTO folders (path, last_modified)
                VALUES (%s, %s)
                ON CONFLICT (path) DO UPDATE SET last_modified = EXCLUDED.last_modified
                RETURNING (xmax = 0) AS inserted
            """),
            (root, folder_last_modified)
        )
        result = cur.fetchone()
        if result and result[0]:  # Se xmax = 0, è un INSERT
            folders_inserted += 1
        elif existing_folder:
            # Controlla se il last_modified è cambiato
            if existing_folder[0] != folder_last_modified:
                folders_updated += 1
    
    # Stampa finale con a capo
    total_elapsed_time = time.time() - scan_start_time
    hours = int(total_elapsed_time // 3600)
    minutes = int((total_elapsed_time % 3600) // 60)
    seconds = int(total_elapsed_time % 60)
    
    print(f"\n\nScansione completata:")
    print(f"  - Tipo scansione: {scan_type.upper()}")
    if scan_type == 'range':
        print(f"  - Range temporale: ultimi {scan_days_back} giorni")
        print(f"  - Data inizio: {scan_from_date.strftime('%Y-%m-%d %H:%M:%S') if scan_from_date else 'N/A'}")
        print(f"  - Cartelle nel range: {len(folders_to_scan) if folders_to_scan else 0}")
        print(f"  - Cartelle saltate (fuori range): {folders_skipped}")
    print(f"  - Tempo totale: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print(f"  - File scansionati: {files_scanned}/{files_total}")
    print(f"  - File inseriti (nuovi): {files_inserted}")
    print(f"  - File aggiornati: {files_updated}")
    print(f"  - File saltati (già aggiornati): {files_skipped}")
    print(f"  - Cartelle nuove: {folders_inserted}")
    print(f"  - Cartelle aggiornate: {folders_updated}")
    
    conn.commit()
    cur.close()
    conn.close()

def load_dir_mtimes_from_db():
    """Carica le date di modifica delle cartelle dalla tabella folders."""
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("SELECT path, last_modified FROM folders")
    results = cur.fetchall()
    cur.close()
    conn.close()
    from datetime import datetime
    dir_mtimes = {}
    for path, last_modified in results:
        if last_modified is not None:
            # Use only integer part of seconds
            dir_mtimes[path] = int(last_modified.timestamp())
    return dir_mtimes


# ==================== SQLITE CONFIGURATION MANAGEMENT ====================

def init_sqlite_config_db():
    """Initializes the SQLite database for configurations."""
    conn = get_sqlite_connection()
    cur = conn.cursor()
    
    # Create configurations table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS configurations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("SQLite configuration database initialized.")


def init_configurations():
    """Initializes default configurations in SQLite database if they don't exist."""
    conn = get_sqlite_connection()
    cur = conn.cursor()
    
    # Default configurations
    default_configs = [
        ('nas_directory', r'\\NAS\folder', 'NAS directory to scan'),
        ('scan_interval', '10', 'Interval in seconds between scans'),
        ('exclude_extensions', json.dumps(['.tmp', '.bak']), 'File extensions to exclude (JSON array)'),
        ('periodically_scan', 'true', 'Enable periodic scanning (true/false)'),
        ('scan_type', 'full', 'Scan type: "full" (complete) or "range" (time-based)'),
        ('scan_days_back', '30', 'Number of days to go back for "range" scan (e.g., 30 = last 30 days)'),
        ('db_host', 'localhost', 'PostgreSQL database host'),
        ('db_port', '5432', 'PostgreSQL database port'),
        ('db_name', 'nas_scanner', 'PostgreSQL database name'),
        ('db_user', 'postgres', 'PostgreSQL database user'),
        ('db_password', '', 'PostgreSQL database password'),
    ]
    
    for key, value, description in default_configs:
        cur.execute("""
            INSERT OR IGNORE INTO configurations (key, value, description)
            VALUES (?, ?, ?)
        """, (key, value, description))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Configurations initialized in SQLite database.")


def get_config(key, default=None):
    """Retrieves a configuration from SQLite database."""
    try:
        conn = get_sqlite_connection()
        cur = conn.cursor()
        cur.execute("SELECT value FROM configurations WHERE key = ?", (key,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result['value'] if result else default
    except Exception as e:
        print(f"Error retrieving configuration '{key}': {e}")
        return default


def update_config(key, value):
    """Updates a configuration in SQLite database."""
    try:
        conn = get_sqlite_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE configurations 
            SET value = ?, updated_at = CURRENT_TIMESTAMP
            WHERE key = ?
        """, (value, key))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Configuration '{key}' updated successfully.")
        return True
    except Exception as e:
        print(f"Error updating configuration '{key}': {e}")
        return False


def get_all_configs():
    """Retrieves all configurations from SQLite database."""
    try:
        conn = get_sqlite_connection()
        cur = conn.cursor()
        cur.execute("SELECT key, value, description, updated_at FROM configurations")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return {row['key']: {'value': row['value'], 'description': row['description'], 'updated_at': row['updated_at']} for row in results}
    except Exception as e:
        print(f"Error retrieving configurations: {e}")
        return {}


# ==================== END CONFIGURATION MANAGEMENT ====================

if __name__ == '__main__':
    # Initialize SQLite database for configurations
    init_sqlite_config_db()
    
    # Initialize default configurations
    init_configurations()
    
    # Load configurations from SQLite database
    from datetime import datetime, timedelta
    
    # Load PostgreSQL database configurations from SQLite
    db_host = get_config('db_host', DB_HOST)
    db_port = get_config('db_port', DB_PORT)
    db_name = get_config('db_name', DB_NAME)
    db_user = get_config('db_user', DB_USER)
    db_password = get_config('db_password', DB_PASSWORD)
    
    # Update global variables with configuration values
    DB_HOST = db_host
    DB_PORT = db_port
    DB_NAME = db_name
    DB_USER = db_user
    DB_PASSWORD = db_password
    
    # Create PostgreSQL database if it doesn't exist
    create_database_if_not_exists()
    
    # Initialize PostgreSQL tables from SQL file
    init_database_tables()
    
    # Start REST API in separate thread
    api_thread = threading.Thread(target=run_flask_api, daemon=True)
    api_thread.start()
    print("✅ API thread started in background")
    
    # Load other configurations
    nas_dir = get_config('nas_directory', NAS_DIR)
    scan_interval = int(get_config('scan_interval', '10'))
    exclude_exts_json = get_config('exclude_extensions', json.dumps(['.tmp', '.bak']))
    exclude_exts = json.loads(exclude_exts_json)
    periodically_scan = get_config('periodically_scan', 'true').lower() == 'true'
    scan_type = get_config('scan_type', 'full')  # 'full' or 'range'
    scan_days_back = int(get_config('scan_days_back', '30'))  # Number of days
    
    print(f"Configurations loaded from SQLite:")
    print(f"  - NAS directory: {nas_dir}")
    print(f"  - Scan interval: {scan_interval} seconds")
    print(f"  - Excluded extensions: {exclude_exts}")
    print(f"  - Periodic scanning: {periodically_scan}")
    print(f"  - Scan type: {scan_type}")
    if scan_type == 'range':
        print(f"  - Time range: last {scan_days_back} days")
    
    # Test comparison between folder in DB and on NAS
    #compare_subfolders_db_vs_nas(nas_dir, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)

    if periodically_scan:
        while True:
            print("\n--- New complete scan ---")
            scan_and_save(nas_dir, exclude_extensions=exclude_exts, scan_type=scan_type, scan_days_back=scan_days_back)
            print(f"Waiting {scan_interval} seconds before next scan...")
            time.sleep(scan_interval)