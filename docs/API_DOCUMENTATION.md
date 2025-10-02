# API Documentation - NAS Directory Scanner

API REST integrata nel backend per monitorare lo stato e le statistiche del NAS scanner.

## Configurazione

**Server**: `http://localhost:5000`

**Database**: PostgreSQL su `<YOUR_SERVER>:5432`

**Integrazione**: L'API è integrata in `main.py` e viene eseguita in un thread separato, permettendo di avere sia la scansione NAS che l'API REST in un unico processo.

## Avvio del Sistema

L'API si avvia automaticamente insieme al sistema di scansione:

### Windows
```bash
start.bat
```

### Linux/Mac
```bash
./start.sh
```

Oppure direttamente:
```bash
python main.py
```

Il sistema avvierà:
- ✅ Thread API REST su `http://localhost:5000`
- ✅ Scansione NAS periodica in background

## Endpoints Disponibili

### 1. Health Check
Verifica lo stato di salute del backend e della connessione al database.

```http
GET /api/health
```

**Risposta di successo (200)**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-10-02T10:30:00.123456"
}
```

**Risposta di errore (503)**:
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "error": "connection refused",
  "timestamp": "2025-10-02T10:30:00.123456"
}
```

---

### 2. Statistiche Generali
Restituisce statistiche complete del sistema.

```http
GET /api/statistics
```

**Risposta (200)**:
```json
{
  "total_files": 15420,
  "total_folders": 3210,
  "files_last_24h": 45,
  "folders_last_24h": 12,
  "last_scan": "2025-10-02T09:15:30.000000",
  "recent_files": [
    {
      "filename": "document.pdf",
      "directory": "\\\\<NAS_IP>\\<SHARE>\\<FOLDER>",
      "last_modified": "2025-10-02T09:15:30.000000"
    }
  ],
  "timestamp": "2025-10-02T10:30:00.123456"
}
```

---

### 3. Configurazioni

#### Ottieni tutte le configurazioni
```http
GET /api/configurations
```

**Risposta (200)**:
```json
{
  "configurations": [
    {
      "key": "nas_directory",
      "value": "\\\\<NAS_IP>\\<SHARE>\\<FOLDER>",
      "description": "Directory del NAS da scansionare",
      "updated_at": "2025-10-01T12:00:00.000000"
    },
    {
      "key": "scan_interval",
      "value": "10",
      "description": "Intervallo in secondi tra le scansioni",
      "updated_at": "2025-10-01T12:00:00.000000"
    }
  ],
  "timestamp": "2025-10-02T10:30:00.123456"
}
```

#### Ottieni una configurazione specifica
```http
GET /api/configurations/{key}
```

**Esempio**:
```http
GET /api/configurations/scan_interval
```

**Risposta (200)**:
```json
{
  "key": "scan_interval",
  "value": "10",
  "description": "Intervallo in secondi tra le scansioni",
  "updated_at": "2025-10-01T12:00:00.000000",
  "timestamp": "2025-10-02T10:30:00.123456"
}
```

#### Aggiorna una configurazione
```http
PUT /api/configurations/{key}
Content-Type: application/json

{
  "value": "20"
}
```

**Risposta (200)**:
```json
{
  "message": "Configuration 'scan_interval' updated successfully",
  "key": "scan_interval",
  "value": "20",
  "timestamp": "2025-10-02T10:30:00.123456"
}
```

---

### 4. Stato Scansione

#### Ottieni lo stato della scansione corrente
```http
GET /api/scan/status
```

**Risposta (200)**:
```json
{
  "last_scan": "2025-10-02T09:15:30.000000",
  "scan_type": "full",
  "scan_interval": "10",
  "periodically_scan": "true",
  "scan_days_back": "30",
  "timestamp": "2025-10-02T10:30:00.123456"
}
```

---

## Accesso Diretto ai Dati

Per l'accesso ai dati di file e cartelle, il frontend si connette **direttamente al database PostgreSQL**:

- **Database**: `nas_scanner` su `<YOUR_SERVER>:5432`
- **Tabelle**:
  - `files` (filename, directory, last_modified)
  - `folders` (path, last_modified)

Questo approccio permette:
- ✅ Query più efficienti e flessibili dal frontend
- ✅ Paginazione e filtri personalizzati
- ✅ Riduzione del carico sull'API REST
- ✅ Accesso real-time ai dati senza intermediari

---

## Architettura

L'API è completamente integrata in `main.py`:
- **Thread Principale**: Gestisce la scansione NAS periodica
- **Thread API**: Esegue il server Flask in background (daemon thread)
- **Condivisione Database**: Entrambi i thread accedono allo stesso database PostgreSQL

Questo design permette di:
- ✅ Avere un unico processo da gestire
- ✅ Monitorare lo stato della scansione in tempo reale via API
- ✅ Aggiornare le configurazioni dinamicamente
- ✅ Non interferire con la scansione in corso

---

## Note

- **CORS**: Abilitato per tutte le origini (configurare in produzione)
- **Autenticazione**: Non implementata (da aggiungere in produzione)
- **Rate Limiting**: Non implementato (da aggiungere in produzione)
- **Logging**: Usa il logging standard di Flask (configurare in produzione)

---

## Codici di Stato HTTP

- `200 OK`: Richiesta completata con successo
- `400 Bad Request`: Parametri mancanti o non validi
- `404 Not Found`: Risorsa non trovata
- `500 Internal Server Error`: Errore del server
- `503 Service Unavailable`: Servizio non disponibile (database disconnesso)
