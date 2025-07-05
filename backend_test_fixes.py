import requests
import unittest
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import re

# Load environment variables from frontend/.env
load_dotenv('/app/frontend/.env')

class BusTicketAPIFixesTest(unittest.TestCase):
    """Test suite for fixed BusTicket API endpoints"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Get the backend URL from environment variables
        backend_url = os.getenv('REACT_APP_BACKEND_URL', 'https://4eb98124-cdcf-45e0-bb77-b91b8274688c.preview.emergentagent.com')
        self.base_url = f"{backend_url}/api"
        print(f"Using API base URL: {self.base_url}")
        
        # Create a test user for authentication
        self.test_user = {
            "email": f"test_user_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "Test123!",
            "first_name": "Test",
            "last_name": "User",
            "phone": "1234567890"
        }
        
        # Register the test user
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=self.test_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login to get token
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        self.token = login_response.json()["access_token"]
        
    def test_01_upcoming_bookings(self):
        """Test the fixed upcoming bookings endpoint"""
        print("\n🔍 Testing User Profile Upcoming Bookings API...")
        
        # Create a booking first to ensure we have data
        booking_id = self.create_test_booking()
        if not booking_id:
            self.skipTest("Skipping test as booking creation failed")
        
        # Test the upcoming bookings endpoint
        response = requests.get(
            f"{self.base_url}/bookings/upcoming",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        # Check response status
        self.assertEqual(response.status_code, 200, 
                         f"Expected status code 200, got {response.status_code}. Response: {response.text}")
        
        # Validate response data
        data = response.json()
        self.assertIsInstance(data, list, "Response should be a list")
        
        print(f"✅ Upcoming bookings API working correctly. Found {len(data)} bookings.")
        
    def test_02_past_bookings(self):
        """Test the fixed past bookings endpoint"""
        print("\n🔍 Testing User Profile Past Bookings API...")
        
        # Test the past bookings endpoint
        response = requests.get(
            f"{self.base_url}/bookings/past",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        # Check response status
        self.assertEqual(response.status_code, 200, 
                         f"Expected status code 200, got {response.status_code}. Response: {response.text}")
        
        # Validate response data
        data = response.json()
        self.assertIsInstance(data, list, "Response should be a list")
        
        print(f"✅ Past bookings API working correctly. Found {len(data)} bookings.")
        
    def test_03_admin_users(self):
        """Test the fixed admin users endpoint"""
        print("\n🔍 Testing Admin Users API...")
        
        # Test the admin users endpoint
        response = requests.get(
            f"{self.base_url}/admin/users",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        # Check response status
        self.assertEqual(response.status_code, 200, 
                         f"Expected status code 200, got {response.status_code}. Response: {response.text}")
        
        # Validate response data
        data = response.json()
        self.assertIsInstance(data, list, "Response should be a list")
        
        print(f"✅ Admin users API working correctly. Found {len(data)} users.")
        
    def test_04_admin_routes(self):
        """Test the fixed admin routes endpoint"""
        print("\n🔍 Testing Admin Routes API...")
        
        # Test the admin routes endpoint
        response = requests.get(
            f"{self.base_url}/admin/routes",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        # Check response status
        self.assertEqual(response.status_code, 200, 
                         f"Expected status code 200, got {response.status_code}. Response: {response.text}")
        
        # Validate response data
        data = response.json()
        self.assertIsInstance(data, list, "Response should be a list")
        
        print(f"✅ Admin routes API working correctly. Found {len(data)} routes.")
        
    def test_05_admin_buses(self):
        """Test the fixed admin buses endpoint"""
        print("\n🔍 Testing Admin Buses API...")
        
        # Test the admin buses endpoint
        response = requests.get(
            f"{self.base_url}/admin/buses",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        # Check response status
        self.assertEqual(response.status_code, 200, 
                         f"Expected status code 200, got {response.status_code}. Response: {response.text}")
        
        # Validate response data
        data = response.json()
        self.assertIsInstance(data, list, "Response should be a list")
        
        print(f"✅ Admin buses API working correctly. Found {len(data)} buses.")
        
    def test_06_booking_flow(self):
        """Test the complete booking flow with seat selection"""
        print("\n🔍 Testing Complete Booking Flow with Seat Selection...")
        
        # Step 1: Search for routes
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        search_data = {
            "origin": "Phnom Penh",
            "destination": "Siem Reap",
            "date": tomorrow,
            "passengers": 1,
            "transport_type": "bus"
        }
        
        search_response = requests.post(
            f"{self.base_url}/search",
            json=search_data
        )
        self.assertEqual(search_response.status_code, 200)
        routes = search_response.json()
        
        if not routes:
            self.skipTest("No routes found for testing")
        
        route_id = routes[0]["id"]
        
        # Step 2: Get seat layout
        seats_response = requests.get(
            f"{self.base_url}/seats/{route_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(seats_response.status_code, 200)
        seats_data = seats_response.json()
        
        # Check if we have seat layout data
        self.assertIn("seats", seats_data, "Seat layout response should contain 'seats' field")
        
        # Find available seats
        available_seats = [seat["id"] for seat in seats_data["seats"] if seat["status"] == "available"]
        
        if not available_seats:
            self.skipTest("No available seats found for testing")
        
        # Step 3: Create booking
        booking_data = {
            "route_id": route_id,
            "selected_seats": [available_seats[0]],
            "passenger_details": [
                {
                    "firstName": "Test",
                    "lastName": "Passenger",
                    "email": "test@example.com",
                    "phone": "1234567890"
                }
            ],
            "date": tomorrow
        }
        
        booking_response = requests.post(
            f"{self.base_url}/bookings",
            headers={"Authorization": f"Bearer {self.token}"},
            json=booking_data
        )
        
        # Check if booking was successful
        self.assertEqual(booking_response.status_code, 200, 
                         f"Expected status code 200, got {booking_response.status_code}. Response: {booking_response.text}")
        
        booking_result = booking_response.json()
        self.assertIn("id", booking_result, "Booking response should contain 'id' field")
        booking_id = booking_result["id"]
        
        # Step 4: Process payment
        payment_data = {
            "booking_id": booking_id,
            "payment_method": "card",
            "card_details": {
                "cardNumber": "4111111111111111",
                "expiryDate": "12/25",
                "cvv": "123",
                "cardHolderName": "Test User"
            }
        }
        
        payment_response = requests.post(
            f"{self.base_url}/payments/process",
            headers={"Authorization": f"Bearer {self.token}"},
            json=payment_data
        )
        
        # Check if payment was successful
        self.assertEqual(payment_response.status_code, 200, 
                         f"Expected status code 200, got {payment_response.status_code}. Response: {payment_response.text}")
        
        payment_result = payment_response.json()
        self.assertEqual(payment_result["status"], "success", "Payment should be successful")
        
        print("✅ Complete booking flow with seat selection working correctly.")
        
    def create_test_booking(self):
        """Helper method to create a test booking"""
        # Search for routes
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        search_data = {
            "origin": "Phnom Penh",
            "destination": "Siem Reap",
            "date": tomorrow,
            "passengers": 1,
            "transport_type": "bus"
        }
        
        search_response = requests.post(
            f"{self.base_url}/search",
            json=search_data
        )
        
        if search_response.status_code != 200:
            print(f"⚠️ Route search failed: {search_response.status_code}")
            return None
            
        routes = search_response.json()
        
        if not routes:
            print("⚠️ No routes found")
            return None
            
        route_id = routes[0]["id"]
        
        # Get seat layout
        seats_response = requests.get(
            f"{self.base_url}/seats/{route_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        if seats_response.status_code != 200:
            print(f"⚠️ Seat layout retrieval failed: {seats_response.status_code}")
            return None
            
        seats_data = seats_response.json()
        
        # Find available seats
        available_seats = [seat["id"] for seat in seats_data["seats"] if seat["status"] == "available"]
        
        if not available_seats:
            print("⚠️ No available seats found")
            return None
            
        # Create booking
        booking_data = {
            "route_id": route_id,
            "selected_seats": [available_seats[0]],
            "passenger_details": [
                {
                    "firstName": "Test",
                    "lastName": "Passenger",
                    "email": "test@example.com",
                    "phone": "1234567890"
                }
            ],
            "date": tomorrow
        }
        
        booking_response = requests.post(
            f"{self.base_url}/bookings",
            headers={"Authorization": f"Bearer {self.token}"},
            json=booking_data
        )
        
        if booking_response.status_code != 200:
            print(f"⚠️ Booking creation failed: {booking_response.status_code}")
            return None
            
        booking_result = booking_response.json()
        
        # Process payment
        payment_data = {
            "booking_id": booking_result["id"],
            "payment_method": "card",
            "card_details": {
                "cardNumber": "4111111111111111",
                "expiryDate": "12/25",
                "cvv": "123",
                "cardHolderName": "Test User"
            }
        }
        
        payment_response = requests.post(
            f"{self.base_url}/payments/process",
            headers={"Authorization": f"Bearer {self.token}"},
            json=payment_data
        )
        
        if payment_response.status_code != 200:
            print(f"⚠️ Payment processing failed: {payment_response.status_code}")
            
        return booking_result["id"]

if __name__ == "__main__":
    # Create a test suite with specific tests
    test_suite = unittest.TestSuite()
    
    # Add tests for fixed endpoints
    test_suite.addTest(BusTicketAPIFixesTest('test_01_upcoming_bookings'))
    test_suite.addTest(BusTicketAPIFixesTest('test_02_past_bookings'))
    test_suite.addTest(BusTicketAPIFixesTest('test_03_admin_users'))
    test_suite.addTest(BusTicketAPIFixesTest('test_04_admin_routes'))
    test_suite.addTest(BusTicketAPIFixesTest('test_05_admin_buses'))
    test_suite.addTest(BusTicketAPIFixesTest('test_06_booking_flow'))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)