"""
Quick test to verify admin login and role
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

print("Testing Admin Login...")
print("=" * 60)

# Login as admin
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "username": "admin",
    "password": "admin123"
})

print(f"\nStatus Code: {response.status_code}")
data = response.json()
print(f"\nResponse:")
print(json.dumps(data, indent=2))

if response.ok:
    print("\n" + "=" * 60)
    print(f"✅ Login successful!")
    print(f"Username: {data['user']['username']}")
    print(f"Role: {data['user']['role']}")
    print(f"Name: {data['user']['name']}")
    print(f"\nToken: {data['access'][:50]}...")
    
    # Test creating a locker
    print("\n" + "=" * 60)
    print("Testing Locker Creation (Admin Only)...")
    
    headers = {"Authorization": f"Bearer {data['access']}"}
    locker_response = requests.post(f"{BASE_URL}/lockers/", json={
        "locker_number": "A101",
        "location": "Building A - Floor 1",
        "size": "medium",
        "status": "available"
    }, headers=headers)
    
    print(f"\nStatus Code: {locker_response.status_code}")
    if locker_response.ok:
        print("✅ Locker created successfully!")
        print(json.dumps(locker_response.json(), indent=2))
    else:
        print("❌ Failed to create locker")
        print(json.dumps(locker_response.json(), indent=2))
else:
    print("❌ Login failed!")
