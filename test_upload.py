#!/usr/bin/env python
import requests
import time

# Wait for server to start
time.sleep(2)

# Test health check
try:
    print("Testing health endpoint...")
    response = requests.get('http://localhost:8001/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Test file upload
try:
    print("\nTesting file upload...")
    
    # Create a test file
    with open('test_file.txt', 'w') as f:
        f.write('Test content for file upload')
    
    # Upload file
    with open('test_file.txt', 'rb') as f:
        files = {'file': f}
        data = {'uploadedBy': 1}  # user_id = 1
        response = requests.post('http://localhost:8001/api/files', files=files, data=data)
        
    print(f"Upload Status: {response.status_code}")
    print(f"Upload Response: {response.json()}")
    
except Exception as e:
    print(f"Error: {e}")
