"""
Script di test per l'API REST del NAS Scanner
Testa tutti gli endpoint disponibili
"""

import requests
import json
from datetime import datetime

# Configurazione
BASE_URL = "http://localhost:5050/api"

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Test dell'endpoint /api/health"""
    print_header("TEST: Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def test_statistics():
    """Test dell'endpoint /api/statistics"""
    print_header("TEST: Statistics")
    try:
        response = requests.get(f"{BASE_URL}/statistics")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Total Files: {data.get('total_files')}")
        print(f"Total Folders: {data.get('total_folders')}")
        print(f"Files Last 24h: {data.get('files_last_24h')}")
        print(f"Last Scan: {data.get('last_scan')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def test_configurations():
    """Test dell'endpoint /api/configurations"""
    print_header("TEST: Configurations (All)")
    try:
        response = requests.get(f"{BASE_URL}/configurations")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        configs = data.get('configurations', [])
        print(f"Total Configurations: {len(configs)}")
        for config in configs:
            print(f"  - {config['key']}: {config['value']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def test_configuration_single(key='scan_interval'):
    """Test dell'endpoint /api/configurations/{key}"""
    print_header(f"TEST: Configuration ({key})")
    try:
        response = requests.get(f"{BASE_URL}/configurations/{key}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def test_scan_status():
    """Test dell'endpoint /api/scan/status"""
    print_header("TEST: Scan Status")
    try:
        response = requests.get(f"{BASE_URL}/scan/status")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Last Scan: {data.get('last_scan')}")
        print(f"Scan Type: {data.get('scan_type')}")
        print(f"Scan Interval: {data.get('scan_interval')}s")
        print(f"Periodically Scan: {data.get('periodically_scan')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def run_all_tests():
    """Esegue tutti i test"""
    print("\n" + "🚀 "+"="*58)
    print("  INIZIO TEST API - NAS Directory Scanner")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nNOTA: I dati di file e cartelle sono accessibili")
    print("      direttamente dal frontend via PostgreSQL")
    
    results = {
        'Health Check': test_health(),
        'Statistics': test_statistics(),
        'Configurations (All)': test_configurations(),
        'Configuration (Single)': test_configuration_single(),
        'Scan Status': test_scan_status(),
    }
    
    # Riepilogo
    print_header("RIEPILOGO TEST")
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nRisultato: {passed}/{total} test passati")
    print("="*60 + "\n")
    
    return passed == total

if __name__ == '__main__':
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrotto dall'utente")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Errore durante i test: {e}")
        exit(1)
