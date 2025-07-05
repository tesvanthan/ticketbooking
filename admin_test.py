import requests
import unittest
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from frontend/.env
load_dotenv('/app/frontend/.env')

class AdminEndpointsTest(unittest.TestCase):
    """Test suite for admin endpoints with ObjectId serialization fix"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Get the backend URL from environment variables
        backend_url = os.getenv('REACT_APP_BACKEND_URL', 'https://4eb98124-cdcf-45e0-bb77-b91b8274688c.preview.emergentagent.com')
        self.base_url = f"{backend_url}/api"
        print(f"Using API base URL: {self.base_url}")
        
        # Admin user for testing admin endpoints
        self.admin_user = {
            "email": f"admin_user_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "9876543210"
        }
        
        self.admin_token = None
        
    def test_01_register_and_login(self):
        """Register and login admin user"""
        # Register admin user
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=self.admin_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login admin user
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": self.admin_user["email"],
                "password": self.admin_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        self.admin_token = login_response.json()["access_token"]
        print(f"✅ Admin registration and login successful: {self.admin_user['email']}")
        
    def test_02_admin_users(self):
        """Test admin users endpoint with ObjectId serialization fix"""
        if not self.admin_token:
            self.test_01_register_and_login()
            
        response = requests.get(
            f"{self.base_url}/admin/users",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            self.assertIsInstance(data, list)
            print(f"✅ Admin users retrieval successful: Found {len(data)} users")
            if len(data) > 0:
                print(f"Sample data: {json.dumps(data[0], indent=2)}")
                # Verify ObjectId fields are properly serialized
                user = data[0]
                self.assertIn("id", user)
                self.assertIsInstance(user["id"], str)
                print("✅ ObjectId serialization working correctly in admin users")
        else:
            print(f"❌ Admin users retrieval failed with status code: {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            self.fail(f"Admin users endpoint failed with status code {response.status_code}")
        
    def test_03_admin_routes(self):
        """Test admin routes endpoint with ObjectId serialization fix"""
        if not self.admin_token:
            self.test_01_register_and_login()
            
        response = requests.get(
            f"{self.base_url}/admin/routes",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            self.assertIsInstance(data, list)
            print(f"✅ Admin routes retrieval successful: Found {len(data)} routes")
            if len(data) > 0:
                print(f"Sample data: {json.dumps(data[0], indent=2)}")
                # Verify ObjectId fields are properly serialized
                route = data[0]
                self.assertIn("id", route)
                self.assertIsInstance(route["id"], str)
                print("✅ ObjectId serialization working correctly in admin routes")
        else:
            print(f"❌ Admin routes retrieval failed with status code: {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            self.fail(f"Admin routes endpoint failed with status code {response.status_code}")
        
    def test_04_admin_buses(self):
        """Test admin buses endpoint with ObjectId serialization fix"""
        if not self.admin_token:
            self.test_01_register_and_login()
            
        response = requests.get(
            f"{self.base_url}/admin/buses",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            self.assertIsInstance(data, list)
            print(f"✅ Admin buses retrieval successful: Found {len(data)} buses")
            if len(data) > 0:
                print(f"Sample data: {json.dumps(data[0], indent=2)}")
                # Verify ObjectId fields are properly serialized
                bus = data[0]
                self.assertIn("id", bus)
                self.assertIsInstance(bus["id"], str)
                print("✅ ObjectId serialization working correctly in admin buses")
        else:
            print(f"❌ Admin buses retrieval failed with status code: {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            self.fail(f"Admin buses endpoint failed with status code {response.status_code}")

if __name__ == "__main__":
    print("🚀 Starting Admin Endpoints Tests...")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    test_suite.addTest(AdminEndpointsTest('test_01_register_and_login'))
    test_suite.addTest(AdminEndpointsTest('test_02_admin_users'))
    test_suite.addTest(AdminEndpointsTest('test_03_admin_routes'))
    test_suite.addTest(AdminEndpointsTest('test_04_admin_buses'))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    
    # Exit with appropriate status code
    if result.wasSuccessful():
        print("✅ All tests passed!")
        exit(0)
    else:
        print("❌ Some tests failed!")
        exit(1)