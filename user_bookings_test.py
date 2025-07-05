import requests
import unittest
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from frontend/.env
load_dotenv('/app/frontend/.env')

class UserBookingsTest(unittest.TestCase):
    """Test suite for user bookings endpoints with ObjectId serialization fix"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Get the backend URL from environment variables
        backend_url = os.getenv('REACT_APP_BACKEND_URL', 'https://4eb98124-cdcf-45e0-bb77-b91b8274688c.preview.emergentagent.com')
        self.base_url = f"{backend_url}/api"
        print(f"Using API base URL: {self.base_url}")
        
        self.test_user = {
            "email": f"test_user_{datetime.now().strftime('%Y%m%d%H%M%S%f')}@example.com",
            "password": "Test123!",
            "first_name": "Test",
            "last_name": "User",
            "phone": "1234567890"
        }
        
        self.token = None
        
    def test_01_register_and_login(self):
        """Register and login test user"""
        # Generate a unique email for this test
        self.test_user["email"] = f"test_user_{datetime.now().strftime('%Y%m%d%H%M%S%f')}@example.com"
        
        # Register user
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=self.test_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login user
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        self.token = login_response.json()["access_token"]
        print(f"✅ User registration and login successful: {self.test_user['email']}")
        
    def test_02_upcoming_bookings(self):
        """Test upcoming bookings endpoint with ObjectId serialization fix"""
        if not self.token:
            self.test_01_register_and_login()
            
        response = requests.get(
            f"{self.base_url}/bookings/upcoming",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            self.assertIsInstance(data, list)
            print(f"✅ Upcoming bookings retrieval successful: Found {len(data)} bookings")
            if len(data) > 0:
                print(f"Sample data: {json.dumps(data[0], indent=2)}")
                # Verify ObjectId fields are properly serialized
                booking = data[0]
                self.assertIn("id", booking)
                self.assertIsInstance(booking["id"], str)
                print("✅ ObjectId serialization working correctly in upcoming bookings")
        else:
            print(f"❌ Upcoming bookings retrieval failed with status code: {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            self.fail(f"Upcoming bookings endpoint failed with status code {response.status_code}")
        
    def test_03_past_bookings(self):
        """Test past bookings endpoint with ObjectId serialization fix"""
        if not self.token:
            self.test_01_register_and_login()
            
        response = requests.get(
            f"{self.base_url}/bookings/past",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            self.assertIsInstance(data, list)
            print(f"✅ Past bookings retrieval successful: Found {len(data)} bookings")
            if len(data) > 0:
                print(f"Sample data: {json.dumps(data[0], indent=2)}")
                # Verify ObjectId fields are properly serialized
                booking = data[0]
                self.assertIn("id", booking)
                self.assertIsInstance(booking["id"], str)
                print("✅ ObjectId serialization working correctly in past bookings")
        else:
            print(f"❌ Past bookings retrieval failed with status code: {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            self.fail(f"Past bookings endpoint failed with status code {response.status_code}")
        
    def test_04_create_booking(self):
        """Test booking creation and seat selection"""
        if not self.token:
            self.test_01_register_and_login()
            
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
        
        if len(routes) == 0:
            print("⚠️ No routes found for testing booking flow")
            return
            
        route_id = routes[0]["id"]
        print(f"Found route: {route_id}")
        
        # Step 2: Get seat layout
        seats_response = requests.get(
            f"{self.base_url}/seats/{route_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        self.assertEqual(seats_response.status_code, 200)
        seats_data = seats_response.json()
        
        # Find available seats
        available_seats = []
        for seat in seats_data["seats"]:
            if seat["status"] == "available":
                available_seats.append(seat["id"])
                
        if len(available_seats) == 0:
            print("⚠️ No available seats found for testing booking flow")
            return
            
        print(f"Found available seats: {available_seats[:3]}")
        
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
        
        print(f"Booking response status code: {booking_response.status_code}")
        
        if booking_response.status_code == 200:
            booking_result = booking_response.json()
            booking_id = booking_result["id"]
            print(f"✅ Booking creation successful: {booking_id}")
            
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
            
            print(f"Payment response status code: {payment_response.status_code}")
            
            if payment_response.status_code == 200:
                payment_result = payment_response.json()
                print(f"✅ Payment processing successful: {payment_result.get('transaction_id', '')}")
                
                # Step 5: Check upcoming bookings again
                upcoming_response = requests.get(
                    f"{self.base_url}/bookings/upcoming",
                    headers={"Authorization": f"Bearer {self.token}"}
                )
                
                if upcoming_response.status_code == 200:
                    upcoming_data = upcoming_response.json()
                    print(f"✅ Upcoming bookings after booking: Found {len(upcoming_data)} bookings")
                    if len(upcoming_data) > 0:
                        # Verify ObjectId fields are properly serialized
                        booking = upcoming_data[0]
                        self.assertIn("id", booking)
                        self.assertIsInstance(booking["id"], str)
                        print("✅ ObjectId serialization working correctly in upcoming bookings after booking")
                else:
                    print(f"❌ Upcoming bookings retrieval failed after booking: {upcoming_response.status_code}")
                
                print(f"Complete booking flow test passed successfully")
            else:
                print(f"❌ Payment processing failed with status code: {payment_response.status_code}")
                print(f"Response text: {payment_response.text[:500]}")
        else:
            print(f"❌ Booking creation failed with status code: {booking_response.status_code}")
            print(f"Response text: {booking_response.text[:500]}")
            if "Some seats are already booked" in booking_response.text:
                print("❌ Seat selection issue detected: 'Some seats are already booked' error")
            self.fail(f"Booking creation failed with status code {booking_response.status_code}")

if __name__ == "__main__":
    print("🚀 Starting User Bookings Tests...")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    test_suite.addTest(UserBookingsTest('test_01_register_and_login'))
    test_suite.addTest(UserBookingsTest('test_02_upcoming_bookings'))
    test_suite.addTest(UserBookingsTest('test_03_past_bookings'))
    test_suite.addTest(UserBookingsTest('test_04_create_booking'))
    
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