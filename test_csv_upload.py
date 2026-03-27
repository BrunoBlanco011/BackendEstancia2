#!/usr/bin/env python
import requests
import json
import time

URL_BASE = "http://127.0.0.1:8001"

print("=" * 60)
print("PRUEBA DE CARGA DE ARCHIVO CSV")
print("=" * 60)

# Esperar a que el servidor esté listo
time.sleep(1)

# Test health check
print("\n[1] Probando health endpoint...")
try:
    r = requests.get(f"{URL_BASE}/health", timeout=5)
    print(f"✓ Status: {r.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Upload a test CSV file
print("\n[2] Cargando archivo CSV de prueba...")
try:
    # Create a simple CSV file content
    csv_content = b"""id,nombre,email,edad
1,Juan,juan@example.com,25
2,Maria,maria@example.com,30
3,Pedro,pedro@example.com,35
"""
    
    files = {
        'file': ('test_data_' + str(int(time.time())) + '.csv', csv_content, 'text/csv')
    }
    
    data = {
        'uploadedBy': 1
    }
    
    r = requests.post(f"{URL_BASE}/api/files", files=files, data=data, timeout=15)
    
    print(f"✓ Status: {r.status_code}")
    
    if r.status_code == 200:
        response = r.json()
        print(f"  ✓ Archivo cargado exitosamente!")
        print(f"  File ID: {response.get('file_id')}")
        print(f"  File Name: {response.get('file_name')}")
        print(f"  Upload Date: {response.get('upload_date')}")
        print("\n" + "=" * 60)
        print("✓✓✓ PRUEBA EXITOSA!")
        print("✓ No hay erro de RETURNING syntax")
        print("✓ Archivo guardado en base de datos MySQL")
        print("=" * 60)
    elif r.status_code == 400:
        error = r.json()
        print(f"  Error de validación: {error.get('error')}")
    else:
        print(f"  Status: {r.status_code}")
        print(f"  Response: {r.text}")
        
except Exception as e:
    print(f"✗ Error al cargar archivo: {e}")
    import traceback
    traceback.print_exc()
