#!/usr/bin/env python
import requests
import json
import time

URL_BASE = "http://127.0.0.1:8001"

print("=" * 60)
print("PRUEBA DE CARGA DE ARCHIVO - SERVIDOR FASTAPI")
print("=" * 60)

# Esperar a que el servidor esté listo
time.sleep(2)

# 1. Test health check
print("\n[1] Probando health endpoint...")
try:
    r = requests.get(f"{URL_BASE}/health", timeout=5)
    print(f"✓ Status: {r.status_code}")
    print(f"  Response: {json.dumps(r.json(), indent=2)}")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# 2. Create a test user
print("\n[2] Creando usuario de prueba...")
try:
    import time as time_module
    timestamp = int(time_module.time())
    payload = {
        "name": "TestUser",
        "last_name": "ForUpload",
        "email": f"testupload{timestamp}@example.com",
        "password": "testpass123",
        "role_id": 1,
        "profile_image": None
    }
    r = requests.post(f"{URL_BASE}/api/auth/register", json=payload, timeout=10)
    print(f"✓ Status: {r.status_code}")
    user_data = r.json()
    print(f"  Response: {json.dumps(user_data, indent=2)}")
    
    # Extract user_id
    if r.status_code in [200, 201] and 'user_id' in user_data:
        user_id = user_data['user_id']
    else:
        print("  Usando user_id: 1 (predeterminado)")
        user_id = 1
        
except Exception as e:
    print(f"! Error creating user (no es crítico): {e}")
    user_id = 1
    print(f"  Usando user_id: {user_id}")

# 3. Upload a test file
print("\n[3] Cargando archivo de prueba...")
try:
    # Create a simple test file in memory
    test_content = b"Este es un archivo de prueba para verificar que la carga funciona correctamente con MySQL y LAST_INSERT_ID()."
    
    files = {
        'file': ('test_document_' + str(int(time.time())) + '.txt', test_content, 'text/plain')
    }
    
    data = {
        'uploadedBy': user_id
    }
    
    r = requests.post(f"{URL_BASE}/api/files", files=files, data=data, timeout=15)
    
    print(f"✓ Status: {r.status_code}")
    
    if r.status_code == 200:
        response = r.json()
        print(f"  ✓ Respuesta exitosa:")
        print(json.dumps(response, indent=2))
        print("\n" + "=" * 60)
        print("✓✓✓ PRUEBA EXITOSA - NO HAY ERROR DE RETURNING")
        print("=" * 60)
    else:
        print(f"  ✗ Error: {r.text}")
        print("\n" + "=" * 60)
        print("✗ PRUEBA FALLÓ")
        print("=" * 60)
        
except Exception as e:
    print(f"✗ Error al cargar archivo: {e}")
    import traceback
    traceback.print_exc()
