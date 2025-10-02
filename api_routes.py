"""
API Routes for NAS Scanner Backend
Contains all REST endpoints for system monitoring and configuration.
"""

from datetime import datetime, timedelta
from flask import jsonify, request
from psycopg2.extras import RealDictCursor


def register_routes(app, get_db_connection, get_sqlite_connection):
    """
    Registers all API routes in the Flask application.
    
    Args:
        app: Flask instance
        get_db_connection: Function to get PostgreSQL connection
        get_sqlite_connection: Function to get SQLite connection
    """
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Checks backend and database health status."""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            conn.close()
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': datetime.now().isoformat()
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 503


    @app.route('/api/statistics', methods=['GET'])
    def get_statistics():
        """Returns general system statistics."""
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # File statistics
            cur.execute("SELECT COUNT(*) as total_files FROM files")
            total_files = cur.fetchone()['total_files']
            
            # Folder statistics
            cur.execute("SELECT COUNT(*) as total_folders FROM folders")
            total_folders = cur.fetchone()['total_folders']
            
            # Most recent files (last 10)
            cur.execute("""
                SELECT filename, directory, last_modified 
                FROM files 
                ORDER BY last_modified DESC 
                LIMIT 10
            """)
            recent_files = cur.fetchall()
            
            # Files modified in last 24 hours
            yesterday = datetime.now() - timedelta(days=1)
            cur.execute("""
                SELECT COUNT(*) as files_last_24h 
                FROM files 
                WHERE last_modified >= %s
            """, (yesterday,))
            files_last_24h = cur.fetchone()['files_last_24h']
            
            # Folders modified in last 24 hours
            cur.execute("""
                SELECT COUNT(*) as folders_last_24h 
                FROM folders 
                WHERE last_modified >= %s
            """, (yesterday,))
            folders_last_24h = cur.fetchone()['folders_last_24h']
            
            # Last overall modification date
            cur.execute("""
                SELECT MAX(last_modified) as last_scan 
                FROM files
            """)
            last_scan_result = cur.fetchone()
            last_scan = last_scan_result['last_scan'].isoformat() if last_scan_result['last_scan'] else None
            
            cur.close()
            conn.close()
            
            return jsonify({
                'total_files': total_files,
                'total_folders': total_folders,
                'files_last_24h': files_last_24h,
                'folders_last_24h': folders_last_24h,
                'last_scan': last_scan,
                'recent_files': [
                    {
                        'filename': f['filename'],
                        'directory': f['directory'],
                        'last_modified': f['last_modified'].isoformat()
                    } for f in recent_files
                ],
                'timestamp': datetime.now().isoformat()
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500


    @app.route('/api/configurations', methods=['GET'])
    def get_configurations_api():
        """Returns all system configurations from SQLite."""
        try:
            conn = get_sqlite_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT key, value, description, updated_at 
                FROM configurations 
                ORDER BY key
            """)
            configs = cur.fetchall()
            
            cur.close()
            conn.close()
            
            return jsonify({
                'configurations': [
                    {
                        'key': c['key'],
                        'value': c['value'],
                        'description': c['description'],
                        'updated_at': c['updated_at'] if c['updated_at'] else None
                    } for c in configs
                ],
                'timestamp': datetime.now().isoformat()
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500


    @app.route('/api/configurations/<key>', methods=['GET'])
    def get_configuration_api(key):
        """Returns a specific configuration from SQLite."""
        try:
            conn = get_sqlite_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT key, value, description, updated_at 
                FROM configurations 
                WHERE key = ?
            """, (key,))
            config = cur.fetchone()
            
            cur.close()
            conn.close()
            
            if config:
                return jsonify({
                    'key': config['key'],
                    'value': config['value'],
                    'description': config['description'],
                    'updated_at': config['updated_at'] if config['updated_at'] else None,
                    'timestamp': datetime.now().isoformat()
                }), 200
            else:
                return jsonify({
                    'error': f"Configuration '{key}' not found",
                    'timestamp': datetime.now().isoformat()
                }), 404
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500


    @app.route('/api/configurations/<key>', methods=['PUT'])
    def update_configuration_api(key):
        """Updates a specific configuration in SQLite."""
        try:
            data = request.get_json()
            if not data or 'value' not in data:
                return jsonify({
                    'error': 'Missing "value" in request body',
                    'timestamp': datetime.now().isoformat()
                }), 400
            
            conn = get_sqlite_connection()
            cur = conn.cursor()
            
            cur.execute("""
                UPDATE configurations 
                SET value = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE key = ?
            """, (data['value'], key))
            
            rows_affected = cur.rowcount
            conn.commit()
            cur.close()
            conn.close()
            
            if rows_affected > 0:
                return jsonify({
                    'message': f"Configuration '{key}' updated successfully",
                    'key': key,
                    'value': data['value'],
                    'timestamp': datetime.now().isoformat()
                }), 200
            else:
                return jsonify({
                    'error': f"Configuration '{key}' not found",
                    'timestamp': datetime.now().isoformat()
                }), 404
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500


    @app.route('/api/scan/status', methods=['GET'])
    def get_scan_status_api():
        """Returns current scan status."""
        try:
            # Last modification in PostgreSQL database
            conn_pg = get_db_connection()
            cur_pg = conn_pg.cursor(cursor_factory=RealDictCursor)
            
            cur_pg.execute("""
                SELECT MAX(last_modified) as last_scan 
                FROM files
            """)
            last_scan_result = cur_pg.fetchone()
            cur_pg.close()
            conn_pg.close()
            
            # Relevant configurations from SQLite
            conn_sqlite = get_sqlite_connection()
            cur_sqlite = conn_sqlite.cursor()
            
            cur_sqlite.execute("""
                SELECT key, value 
                FROM configurations 
                WHERE key IN ('scan_type', 'scan_interval', 'periodically_scan', 'scan_days_back')
            """)
            configs = {row['key']: row['value'] for row in cur_sqlite.fetchall()}
            cur_sqlite.close()
            conn_sqlite.close()
            
            return jsonify({
                'last_scan': last_scan_result['last_scan'].isoformat() if last_scan_result['last_scan'] else None,
                'scan_type': configs.get('scan_type', 'full'),
                'scan_interval': configs.get('scan_interval', '10'),
                'periodically_scan': configs.get('periodically_scan', 'true'),
                'scan_days_back': configs.get('scan_days_back', '30'),
                'timestamp': datetime.now().isoformat()
            }), 200
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500

    print("✅ API routes registered successfully")
