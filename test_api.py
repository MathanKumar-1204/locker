"""
Test script for Smart Locker System API
Run this after starting the server to verify all endpoints work correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_separator():
    print("\n" + "="*80 + "\n")

def print_response(title, response):
    print(f"{title}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print_separator()

def test_api():
    print("🧪 Testing Smart Locker System API\n")
    
    # Test 1: Register Admin
    print("1️⃣ Register Admin User")
    response = requests.post(f"{BASE_URL}/auth/register/", json={
        "username": "testadmin",
        "email": "admin@test.com",
        "name": "Test Admin",
        "password": "adminpass123"
    })
    print_response("Register Admin:", response)
    
    # Test 2: Register Regular User
    print("2️⃣ Register Regular User")
    response = requests.post(f"{BASE_URL}/auth/register/", json={
        "username": "testuser",
        "email": "user@test.com",
        "name": "Test User",
        "password": "userpass123"
    })
    print_response("Register User:", response)
    
    # Test 3: Login Admin
    print("3️⃣ Login Admin")
    login_response = requests.post(f"{BASE_URL}/auth/login/", json={
        "username": "testadmin",
        "password": "adminpass123"
    })
    print_response("Login Admin:", login_response)
    admin_token = login_response.json().get('access')
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Test 4: Login User
    print("4️⃣ Login Regular User")
    login_response = requests.post(f"{BASE_URL}/auth/login/", json={
        "username": "testuser",
        "password": "userpass123"
    })
    print_response("Login User:", login_response)
    user_token = login_response.json().get('access')
    user_headers = {"Authorization": f"Bearer {user_token}"}
    
    # Test 5: Create Locker (Admin)
    print("5️⃣ Create Locker (Admin Only)")
    response = requests.post(f"{BASE_URL}/lockers/", json={
        "locker_number": "A101",
        "location": "Building A - Floor 1",
        "size": "medium",
        "status": "available"
    }, headers=admin_headers)
    print_response("Create Locker 1:", response)
    
    # Test 6: Create Another Locker
    print("6️⃣ Create Second Locker")
    response = requests.post(f"{BASE_URL}/lockers/", json={
        "locker_number": "B202",
        "location": "Building B - Floor 2",
        "size": "large",
        "status": "available"
    }, headers=admin_headers)
    print_response("Create Locker 2:", response)
    
    # Test 7: List All Lockers
    print("7️⃣ List All Lockers")
    response = requests.get(f"{BASE_URL}/lockers/", headers=admin_headers)
    print_response("All Lockers:", response)
    
    # Test 8: Get Available Lockers (Cached)
    print("8️⃣ Get Available Lockers (Redis Cached)")
    response = requests.get(f"{BASE_URL}/lockers/available/", headers=user_headers)
    print_response("Available Lockers:", response)
    
    # Test 9: Reserve Locker (User)
    print("9️⃣ Reserve Locker (User)")
    response = requests.post(f"{BASE_URL}/reservations/", json={
        "locker_id": 1
    }, headers=user_headers)
    print_response("Reserve Locker:", response)
    
    # Test 10: List User Reservations
    print("🔟 List User Reservations")
    response = requests.get(f"{BASE_URL}/reservations/", headers=user_headers)
    print_response("User Reservations:", response)
    
    # Test 11: Try to Reserve Another Locker (Should Fail)
    print("1️⃣1️⃣ Try to Reserve Another Locker (Should Fail - Already Have Active)")
    response = requests.post(f"{BASE_URL}/reservations/", json={
        "locker_id": 2
    }, headers=user_headers)
    print_response("Reserve Second Locker (Should Fail):", response)
    
    # Test 12: Get Locker Details
    print("1️⃣2️⃣ Get Locker Details")
    response = requests.get(f"{BASE_URL}/lockers/1/", headers=user_headers)
    print_response("Locker Details:", response)
    
    # Test 13: Release Locker
    print("1️⃣3️⃣ Release Locker")
    response = requests.put(f"{BASE_URL}/reservations/1/release/", headers=user_headers)
    print_response("Release Locker:", response)
    
    # Test 14: Check Available Lockers After Release
    print("1️⃣4️⃣ Check Available Lockers After Release")
    response = requests.get(f"{BASE_URL}/lockers/available/", headers=user_headers)
    print_response("Available Lockers After Release:", response)
    
    # Test 15: Admin View All Reservations
    print("1️⃣5️⃣ Admin View All Reservations")
    response = requests.get(f"{BASE_URL}/reservations/", headers=admin_headers)
    print_response("All Reservations (Admin):", response)
    
    # Test 16: Update Locker (Admin)
    print("1️⃣6️⃣ Update Locker (Admin)")
    response = requests.put(f"{BASE_URL}/lockers/1/", json={
        "location": "Building A - Floor 1 (Updated)"
    }, headers=admin_headers)
    print_response("Update Locker:", response)
    
    # Test 17: User Profile
    print("1️⃣7️⃣ Get User Profile")
    response = requests.get(f"{BASE_URL}/auth/profile/", headers=user_headers)
    print_response("User Profile:", response)
    
    print("✅ All tests completed!\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server!")
        print("Make sure the Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
