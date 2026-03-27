#!/usr/bin/env python
import requests
import json

# Test health endpoint
print("Testing health endpoint at http://localhost:8001/health...")
try:
    r = requests.get('http://localhost:8001/health', timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")
    print("✓ Server is running\n")
except Exception as e:
    print(f"✗ Error connecting to server: {e}\n")

# Try to create a test file and upload
print("Attempting file upload...")
try:
    # Create test file
    test_content = b"This is a test file for uploading"
    
    files = {'file': ('test_document.txt', test_content, 'text/plain')}
    data = {'uploadedBy': 1}
    
    r = requests.post('http://localhost:8001/api/files', files=files, data=data, timeout=10)
    print(f"Upload Status: {r.status_code}")
    print(f"Response: {json.dumps(r.json(), indent=2)}")
    
    if r.status_code == 200:
        print("✓ File upload successful!")
    else:
        print(f"✗ Upload failed with status {r.status_code}")
except Exception as e:
    print(f"✗ Error uploading file: {e}")
