def update_folders_last_modified(folders, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD):
    """Updates the folders table only for specified folders, using filesystem last_modified date."""
    from datetime import datetime
    import psycopg2
    from psycopg2 import sql
    import os
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS folders (
            id SERIAL PRIMARY KEY,
            path TEXT NOT NULL UNIQUE,
            last_modified TIMESTAMP NOT NULL
        );
    """)
    count = 0
    for folder in folders:
        try:
            dir_mtime = os.path.getmtime(folder)
            dir_mtime_dt = datetime.fromtimestamp(dir_mtime)
            print(f"Updating folder: {folder} (Last Modified: {dir_mtime_dt})")
        except Exception as e:
            print(f"Error reading folder {folder}: {e}")
            continue
        cur.execute(
            sql.SQL("""
                INSERT INTO folders (path, last_modified)
                VALUES (%s, %s)
                ON CONFLICT (path) DO UPDATE SET last_modified = EXCLUDED.last_modified
            """),
            (folder, dir_mtime_dt)
        )
        count += 1
    conn.commit()
    cur.close()
    conn.close()
    print(f"Folders updated: {count}")
def delete_files_in_folder_from_db(folder, files, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD):
    """Deletes specified files (names) from the DB in the indicated folder."""
    import psycopg2
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    for file in files:
        print(f"Deleting from DB: {file} in {folder}")
        cur.execute(
            "DELETE FROM files WHERE filename = %s AND directory = %s",
            (file, folder)
        )
    conn.commit()
    cur.close()
    conn.close()

def save_files_in_folder(folder, files, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD):
    """Saves/updates only specified files (names) in the indicated folder."""
    from datetime import datetime
    import psycopg2
    from psycopg2 import sql
    import os
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            directory TEXT NOT NULL,
            last_modified TIMESTAMP NOT NULL,
            UNIQUE(filename, directory)
        );
    """)
    for file in files:
        file_path = os.path.join(folder, file)
        try:
            last_modified = os.path.getmtime(file_path)
            last_modified_dt = datetime.fromtimestamp(last_modified)
        except Exception:
            print(f"Error reading file {file_path}")
            continue
        print(f"Saving ONLY: {file} in {folder} (Last Modified: {last_modified_dt})")
        cur.execute(
            sql.SQL("""
                INSERT INTO files (filename, directory, last_modified)
                VALUES (%s, %s, %s)
                ON CONFLICT (filename, directory) DO UPDATE SET last_modified = EXCLUDED.last_modified
            """),
            (file, folder, last_modified_dt)
        )
    # Update folder in folders table with current last_modified
    try:
        dir_mtime = os.path.getmtime(folder)
        dir_mtime_dt = datetime.fromtimestamp(dir_mtime)
        cur.execute(
            sql.SQL("""
                INSERT INTO folders (path, last_modified)
                VALUES (%s, %s)
                ON CONFLICT (path) DO UPDATE SET last_modified = EXCLUDED.last_modified
            """),
            (folder, dir_mtime_dt)
        )
    except Exception as e:
        print(f"Error updating folder {folder} in folders table: {e}")
    conn.commit()
    cur.close()
    conn.close()
def compare_files_in_folder_db_vs_nas(folder, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, exclude_extensions=None):
    """Compares DIRECT files of folder between NAS and DB. Returns:
    - 'to_add_or_update': new or modified files (dict: name -> {'nas_mtime': ..., 'db_mtime': ...})
    - 'to_delete': files present in DB but not on NAS anymore (list)
    """
    if exclude_extensions is None:
        exclude_extensions = []
    from datetime import datetime
    import psycopg2
    import os
    # Read files on NAS
    try:
        nas_files = {f: int(os.path.getmtime(os.path.join(folder, f)))
                    for f in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, f)) and not f.lower().endswith(tuple(exclude_extensions))}
    except Exception as e:
        print(f"Error reading files in folder {folder}: {e}")
        return {'to_add_or_update': {}, 'to_delete': []}
    # Read files from DB
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            directory TEXT NOT NULL,
            last_modified TIMESTAMP NOT NULL,
            UNIQUE(filename, directory)
        );
    """)
    cur.execute("SELECT filename, last_modified FROM files WHERE directory = %s", (folder,))
    db_files = {row[0]: int(row[1].timestamp()) for row in cur.fetchall() if row[1] is not None}
    # Comparison
    to_add_or_update = {}
    for f, nas_mtime in nas_files.items():
        db_mtime = db_files.get(f)
        if db_mtime is None or db_mtime != nas_mtime:
            to_add_or_update[f] = {'nas_mtime': nas_mtime, 'db_mtime': db_mtime}
    to_delete = [f for f in db_files if f not in nas_files]
    cur.close()
    conn.close()
    return {'to_add_or_update': to_add_or_update, 'to_delete': to_delete}
def scan_files_in_folder(folder, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, exclude_extensions=None):
    """Scans only DIRECT files in folder (non-recursive) and updates DB."""
    if exclude_extensions is None:
        exclude_extensions = []
    from datetime import datetime
    import psycopg2
    from psycopg2 import sql
    import os
    try:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    except Exception as e:
        print(f"Error reading files in folder {folder}: {e}")
        return
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            directory TEXT NOT NULL,
            last_modified TIMESTAMP NOT NULL,
            UNIQUE(filename, directory)
        );
    """)
    for file in files:
        if file.lower().endswith(tuple(exclude_extensions)):
            continue
        file_path = os.path.join(folder, file)
        try:
            last_modified = os.path.getmtime(file_path)
            last_modified_dt = datetime.fromtimestamp(last_modified)
        except Exception:
            continue
        print(f"Saving: {file} in {folder} (Last Modified: {last_modified_dt})")
        cur.execute(
            sql.SQL("""
                INSERT INTO files (filename, directory, last_modified)
                VALUES (%s, %s, %s)
                ON CONFLICT (filename, directory) DO UPDATE SET last_modified = EXCLUDED.last_modified
            """),
            (file, folder, last_modified_dt)
        )
    conn.commit()
    cur.close()
    conn.close()

def scan_and_save(directory, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, exclude_extensions=None, prev_dir_mtimes=None):
    """Scans files and folders, updates DB, excludes extensions if required."""
    if exclude_extensions is None:
        exclude_extensions = []
    if prev_dir_mtimes is None:
        prev_dir_mtimes = {}
    from datetime import datetime
    import psycopg2
    from psycopg2 import sql
    import os
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    # Create tables if they don't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            filename TEXT NOT NULL,
            directory TEXT NOT NULL,
            last_modified TIMESTAMP NOT NULL,
            UNIQUE(filename, directory)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS folders (
            id SERIAL PRIMARY KEY,
            path TEXT NOT NULL UNIQUE,
            last_modified TIMESTAMP NOT NULL
        );
    """)
    updated_dir_mtimes = prev_dir_mtimes.copy()
    for root, dirs, files in os.walk(directory):
        try:
            dir_mtime = os.path.getmtime(root)
            dir_mtime_dt = datetime.fromtimestamp(dir_mtime)
            dir_mtime_int = int(dir_mtime)
        except Exception:
            continue
        # Update/Insert folder in folders table
        cur.execute(
            sql.SQL("""
                INSERT INTO folders (path, last_modified)
                VALUES (%s, %s)
                ON CONFLICT (path) DO UPDATE SET last_modified = EXCLUDED.last_modified
            """),
            (root, dir_mtime_dt)
        )
        # If directory hasn't changed (integer seconds only), skip
        if root in prev_dir_mtimes and prev_dir_mtimes[root] == dir_mtime_int:
            continue
        # Exclude directory if it contains at least one file with excluded extension
        if any(file.lower().endswith(tuple(exclude_extensions)) for file in files):
            print(f"Excluded directory (contains excluded files): {root}")
            continue
        for file in files:
            file_path = os.path.join(root, file)
            try:
                last_modified = os.path.getmtime(file_path)
                last_modified_dt = datetime.fromtimestamp(last_modified)
            except Exception:
                continue
            print(f"Saving: {file} in {root} (Last Modified: {last_modified_dt})")
            cur.execute(
                sql.SQL("""
                    INSERT INTO files (filename, directory, last_modified)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (filename, directory) DO UPDATE SET last_modified = EXCLUDED.last_modified
                """),
                (file, root, last_modified_dt)
            )
        updated_dir_mtimes[root] = dir_mtime_int
    conn.commit()
    cur.close()
    conn.close()
    return updated_dir_mtimes
import psycopg2
import os
from datetime import datetime


def compare_subfolders_db_vs_nas(parent_folder, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD):
    """Compares all subfolders of parent_folder between DB and NAS."""
    print(f"Comparing subfolders in: {parent_folder}")
    # Get all subfolders from filesystem
    subfolders = [os.path.join(parent_folder, name) for name in os.listdir(parent_folder)
                 if os.path.isdir(os.path.join(parent_folder, name))]
    # Connect to DB
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()

    folders_to_update = {}

    for folder_path in subfolders:
        cur.execute("SELECT last_modified FROM folders WHERE path = %s", (folder_path,))
        row = cur.fetchone()
        if not row:
            print(f"Folder not found in DB: {folder_path}")
            continue
        db_last_modified = row[0]
        if db_last_modified is not None:
            db_last_modified = int(db_last_modified.timestamp())
        else:
            print(f"No date in DB for: {folder_path}")
            continue
        try:
            nas_last_modified = int(os.path.getmtime(folder_path))
        except Exception as e:
            print(f"Error reading folder from NAS: {e}")
            continue
        if db_last_modified != nas_last_modified:
            print(f"\nFolder: {folder_path}")
            print(f"  DB:  {db_last_modified} ({datetime.fromtimestamp(db_last_modified)})")
            print(f"  NAS: {nas_last_modified} ({datetime.fromtimestamp(nas_last_modified)})")
            print("  Dates are different!")
            folders_to_update[folder_path] = {'updated': False}
    cur.close()
    conn.close()
    if not folders_to_update:
        print("All subfolders match between DB and NAS.")
    else:
        print('Folders to update: ')
        for folder in list(folders_to_update.keys()):
            info = folders_to_update[folder]
            print(f" - {folder}, {info}")
            # Recurse on subfolders only if not yet updated
            if not info['updated']:
                sub_updates = compare_subfolders_db_vs_nas(folder, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
                # Merge recursive results into main dictionary
                for subfolder, subinfo in sub_updates.items():
                    folders_to_update[subfolder] = subinfo
    return folders_to_update
