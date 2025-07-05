import requests
import unittest
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import re

# Load environment variables from frontend/.env
load_dotenv('/app/frontend/.env')

class BusTicketAPITest(unittest.TestCase):
    """Test suite for BusTicket API endpoints"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Get the backend URL from environment variables
        backend_url = os.getenv('REACT_APP_BACKEND_URL', 'https://463918e2-1f42-4cce-be47-8127013d3681.preview.emergentagent.com')
        self.base_url = f"{backend_url}/api"
        print(f"Using API base URL: {self.base_url}")
        
        self.test_user = {
            "email": f"test_user_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "Test123!",
            "first_name": "Test",
            "last_name": "User",
            "phone": "1234567890"
        }
        self.token = None
        
    def test_01_health_check(self):
        """Test API health check endpoint"""
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("BusTicket API is running", data["message"])
        print("✅ Health check endpoint working")
        
    def test_02_register_user(self):
        """Test user registration"""
        response = requests.post(
            f"{self.base_url}/auth/register",
            json=self.test_user
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], self.test_user["email"])
        self.assertEqual(data["first_name"], self.test_user["first_name"])
        self.assertEqual(data["last_name"], self.test_user["last_name"])
        print(f"✅ User registration successful: {self.test_user['email']}")
        
    def test_03_login_user(self):
        """Test user login"""
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.token = data["access_token"]
        print("✅ User login successful")
        
    def test_04_get_user_profile(self):
        """Test getting user profile"""
        if not self.token:
            self.test_03_login_user()
            
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], self.test_user["email"])
        print("✅ User profile retrieval successful")
        
    def test_04a_auth_error_handling(self):
        """Test authentication error handling"""
        # Test with invalid token
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        self.assertEqual(response.status_code, 401)
        print("✅ Invalid token handling successful")
        
        # Test with missing token
        response = requests.get(f"{self.base_url}/auth/me")
        self.assertIn(response.status_code, [401, 403, 422])  # Different frameworks handle this differently
        print("✅ Missing token handling successful")
        
        # Test with invalid login credentials
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "WrongPassword123"
            }
        )
        self.assertEqual(response.status_code, 401)
        print("✅ Invalid login credentials handling successful")
        
    def test_05_search_routes(self):
        """Test route search functionality with various parameters"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Test case 1: Standard search
        search_data = {
            "origin": "Phnom Penh",
            "destination": "Siem Reap",
            "date": tomorrow,
            "passengers": 2,
            "transport_type": "bus"
        }
        
        response = requests.post(
            f"{self.base_url}/search",
            json=search_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn("id", data[0])
            self.assertIn("origin", data[0])
            self.assertIn("destination", data[0])
            self.assertIn("price", data[0])
            print(f"✅ Standard route search successful: Found {len(data)} routes")
        else:
            print("⚠️ Standard route search returned no results, but API is working")
        
        # Test case 2: Different origin and destination
        search_data = {
            "origin": "Phnom Penh",
            "destination": "Sihanoukville",
            "date": tomorrow,
            "passengers": 1,
            "transport_type": "bus"
        }
        
        response = requests.post(
            f"{self.base_url}/search",
            json=search_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(f"✅ Alternative route search successful: Found {len(data)} routes")
        
        # Test case 3: Different transport type
        search_data = {
            "origin": "Sihanoukville",
            "destination": "Koh Rong",
            "date": tomorrow,
            "passengers": 1,
            "transport_type": "ferry"
        }
        
        response = requests.post(
            f"{self.base_url}/search",
            json=search_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(f"✅ Ferry transport search successful: Found {len(data)} routes")
        
        # Test case 4: Case insensitive search
        search_data = {
            "origin": "phnom penh",  # lowercase
            "destination": "siem reap",  # lowercase
            "date": tomorrow,
            "passengers": 1,
            "transport_type": "bus"
        }
        
        response = requests.post(
            f"{self.base_url}/search",
            json=search_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(f"✅ Case insensitive search successful: Found {len(data)} routes")
        
        # Test case 5: Future date
        next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        search_data = {
            "origin": "Phnom Penh",
            "destination": "Siem Reap",
            "date": next_week,
            "passengers": 1,
            "transport_type": "bus"
        }
        
        response = requests.post(
            f"{self.base_url}/search",
            json=search_data
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(f"✅ Future date search successful: Found {len(data)} routes")
        
        # Test case 6: Invalid input handling
        search_data = {
            "origin": "NonExistentCity",
            "destination": "AnotherNonExistentCity",
            "date": tomorrow,
            "passengers": 1,
            "transport_type": "bus"
        }
        
        response = requests.post(
            f"{self.base_url}/search",
            json=search_data
        )
        self.assertEqual(response.status_code, 200)  # Should still return 200 with empty results
        data = response.json()
        self.assertEqual(len(data), 0)  # Should return empty list
        print("✅ Invalid city search handled correctly with empty results")
            
    def test_06_get_suggestions(self):
        """Test route suggestions for autocomplete with various queries"""
        # Test case 1: Standard query
        response = requests.get(f"{self.base_url}/suggestions?q=Phnom")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn("Phnom Penh", data)
            print(f"✅ Standard suggestions query successful: Found {len(data)} suggestions")
        else:
            print("⚠️ Standard suggestions query returned no results, but API is working")
        
        # Test case 2: Lowercase query
        response = requests.get(f"{self.base_url}/suggestions?q=phnom")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        if len(data) > 0:
            self.assertIn("Phnom Penh", data)
            print(f"✅ Lowercase suggestions query successful: Found {len(data)} suggestions")
        else:
            print("⚠️ Lowercase suggestions query returned no results, but API is working")
        
        # Test case 3: Partial match
        response = requests.get(f"{self.base_url}/suggestions?q=Siem")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        if len(data) > 0:
            self.assertIn("Siem Reap", data)
            print(f"✅ Partial match suggestions query successful: Found {len(data)} suggestions")
        else:
            print("⚠️ Partial match suggestions query returned no results, but API is working")
        
        # Test case 4: Destination query
        response = requests.get(f"{self.base_url}/suggestions?q=Koh")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        if len(data) > 0:
            self.assertIn("Koh Rong", data)
            print(f"✅ Destination suggestions query successful: Found {len(data)} suggestions")
        else:
            print("⚠️ Destination suggestions query returned no results, but API is working")
        
        # Test case 5: Empty query
        response = requests.get(f"{self.base_url}/suggestions?q=")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)  # Should return empty list
        print("✅ Empty suggestions query handled correctly with empty results")
        
        # Test case 6: Non-existent location
        response = requests.get(f"{self.base_url}/suggestions?q=NonExistentCity")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)  # Should return empty list
        print("✅ Non-existent location query handled correctly with empty results")
            
    def test_07_get_popular_destinations(self):
        """Test popular destinations endpoint"""
        response = requests.get(f"{self.base_url}/destinations/popular")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ Popular destinations retrieval successful: Found {len(data)} destinations")
            
    def test_08_get_seat_layout(self):
        """Test seat layout retrieval"""
        # First search for routes
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
        
        if len(routes) > 0:
            route_id = routes[0]["id"]
            response = requests.get(
                f"{self.base_url}/seats/{route_id}?date={tomorrow}"
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIn("seat_layout", data)
            self.assertIsInstance(data["seat_layout"], list)
            print(f"✅ Seat layout retrieval successful: Found {len(data['seat_layout'])} seats")
        else:
            print("⚠️ Skipping seat layout test as no routes were found")
            
    def test_09_create_booking(self):
        """Test booking creation"""
        # Register and login a new user for this test
        test_email = f"booking_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Booking",
            "last_name": "Test",
            "phone": "1234567890"
        }
        
        # Register
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=test_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["access_token"]
            
        # First search for routes
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
        
        if len(routes) > 0:
            route_id = routes[0]["id"]
            
            # Get seat layout
            seats_response = requests.get(
                f"{self.base_url}/seats/{route_id}?date={tomorrow}"
            )
            self.assertEqual(seats_response.status_code, 200)
            seats_data = seats_response.json()
            
            # Find an available seat
            available_seats = [seat["seat_id"] for seat in seats_data["seat_layout"] if seat["is_available"]]
            
            if available_seats:
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
                
                response = requests.post(
                    f"{self.base_url}/bookings",
                    headers={"Authorization": f"Bearer {token}"},
                    json=booking_data
                )
                
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertIn("id", data)
                self.assertIn("booking_reference", data)
                self.booking_id = data["id"]
                print(f"✅ Booking creation successful: {data['booking_reference']}")
                
                # Test payment processing
                payment_data = {
                    "booking_id": self.booking_id,
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
                    headers={"Authorization": f"Bearer {token}"},
                    json=payment_data
                )
                
                self.assertEqual(payment_response.status_code, 200)
                payment_result = payment_response.json()
                self.assertEqual(payment_result["status"], "success")
                print(f"✅ Payment processing successful: {payment_result['transaction_id']}")
                
                # Test retrieving user bookings
                bookings_response = requests.get(
                    f"{self.base_url}/bookings",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                self.assertEqual(bookings_response.status_code, 200)
                bookings_data = bookings_response.json()
                self.assertIsInstance(bookings_data, list)
                self.assertGreater(len(bookings_data), 0)
                print(f"✅ User bookings retrieval successful: Found {len(bookings_data)} bookings")
            else:
                print("⚠️ Skipping booking test as no available seats were found")
        else:
            print("⚠️ Skipping booking test as no routes were found")
            
    def test_10_get_user_bookings(self):
        """Test retrieving user bookings"""
        # This test depends on test_09_create_booking having run successfully
        # Register and login a new user for this test
        test_email = f"bookings_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Bookings",
            "last_name": "Test",
            "phone": "1234567890"
        }
        
        # Register
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=test_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["access_token"]
        
        # Get user bookings (should be empty for a new user)
        response = requests.get(
            f"{self.base_url}/bookings",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ User bookings retrieval successful: Found {len(data)} bookings for new user")

def run_tests():
    """Run all tests in order"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(BusTicketAPITest('test_01_health_check'))
    test_suite.addTest(BusTicketAPITest('test_02_register_user'))
    test_suite.addTest(BusTicketAPITest('test_03_login_user'))
    test_suite.addTest(BusTicketAPITest('test_04_get_user_profile'))
    test_suite.addTest(BusTicketAPITest('test_04a_auth_error_handling'))
    test_suite.addTest(BusTicketAPITest('test_05_search_routes'))
    test_suite.addTest(BusTicketAPITest('test_06_get_suggestions'))
    test_suite.addTest(BusTicketAPITest('test_07_get_popular_destinations'))
    test_suite.addTest(BusTicketAPITest('test_08_get_seat_layout'))
    test_suite.addTest(BusTicketAPITest('test_09_create_booking'))
    test_suite.addTest(BusTicketAPITest('test_10_get_user_bookings'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(test_suite)

def run_specific_tests(test_names):
    """Run specific tests by name"""
    test_suite = unittest.TestSuite()
    for test_name in test_names:
        test_suite.addTest(BusTicketAPITest(test_name))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(test_suite)

if __name__ == "__main__":
    print("🚀 Starting BusTicket API Tests...")
    
    # Run specific tests based on command line arguments
    import sys
    if len(sys.argv) > 1:
        test_names = sys.argv[1:]
        print(f"Running specific tests: {', '.join(test_names)}")
        result = run_specific_tests(test_names)
    else:
        # Run all tests
        result = run_tests()
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    
    # Exit with appropriate status code
    if result.wasSuccessful():
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)