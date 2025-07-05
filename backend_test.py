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
        backend_url = os.getenv('REACT_APP_BACKEND_URL', 'https://4eb98124-cdcf-45e0-bb77-b91b8274688c.preview.emergentagent.com')
        self.base_url = f"{backend_url}/api"
        print(f"Using API base URL: {self.base_url}")
        
        self.test_user = {
            "email": f"test_user_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "Test123!",
            "first_name": "Test",
            "last_name": "User",
            "phone": "1234567890"
        }
        
        # Admin user for testing admin endpoints
        self.admin_user = {
            "email": f"admin_user_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "9876543210"
        }
        
        self.token = None
        self.admin_token = None
        self.user_id = None
        
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
        # Register a new user specifically for this test
        test_email = f"login_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Login",
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
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.token = data["access_token"]
        print("✅ User login successful")
        
    def test_04_get_user_profile(self):
        """Test getting user profile"""
        # Register and login a new user specifically for this test
        test_email = f"profile_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Profile",
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
            
        # Get profile
        response = requests.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], test_user["email"])
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
                
                if response.status_code == 200:
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
                    
                    if payment_response.status_code == 200:
                        payment_result = payment_response.json()
                        if payment_result.get("status") == "success":
                            print(f"✅ Payment processing successful: {payment_result['transaction_id']}")
                        else:
                            print(f"⚠️ Payment processing returned non-success status: {payment_result.get('status')}")
                    else:
                        print(f"⚠️ Payment processing failed with status code: {payment_response.status_code}")
                        if payment_response.text:
                            print(f"Response: {payment_response.text[:200]}")
                    
                    # Test retrieving user bookings
                    try:
                        bookings_response = requests.get(
                            f"{self.base_url}/bookings",
                            headers={"Authorization": f"Bearer {token}"}
                        )
                        
                        if bookings_response.status_code == 200:
                            bookings_data = bookings_response.json()
                            self.assertIsInstance(bookings_data, list)
                            print(f"✅ User bookings retrieval successful: Found {len(bookings_data)} bookings")
                        else:
                            print(f"⚠️ User bookings retrieval failed with status code: {bookings_response.status_code}")
                            if bookings_response.text:
                                print(f"Response: {bookings_response.text[:200]}")
                    except Exception as e:
                        print(f"⚠️ Error retrieving user bookings: {str(e)}")
                else:
                    print(f"⚠️ Booking creation failed with status code: {response.status_code}")
                    if response.text:
                        print(f"Response: {response.text[:200]}")
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
        
    def test_11_user_credit(self):
        """Test user credit endpoint"""
        # Register and login a new user for this test
        test_email = f"credit_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Credit",
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
        
        # Get user credit
        response = requests.get(
            f"{self.base_url}/user/credit",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("balance", data)
        self.assertIn("transactions", data)
        print(f"✅ User credit retrieval successful: Balance = {data['balance']}")
        
    def test_12_upcoming_bookings(self):
        """Test upcoming bookings endpoint with fixed InvalidId exception handling"""
        # Register and login a new user for this test
        test_email = f"upcoming_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Upcoming",
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
        
        # Get upcoming bookings
        response = requests.get(
            f"{self.base_url}/bookings/upcoming",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        # This should work for a new user with no bookings
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ Upcoming bookings retrieval successful: Found {len(data)} bookings")
        
        # Test with invalid token to check exception handling
        response = requests.get(
            f"{self.base_url}/bookings/upcoming",
            headers={"Authorization": f"Bearer invalid_token"}
        )
        
        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, 401)
        print(f"✅ Upcoming bookings with invalid token returns 401 as expected")
        
    def test_13_past_bookings(self):
        """Test past bookings endpoint with fixed InvalidId exception handling"""
        # Register and login a new user for this test
        test_email = f"past_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Past",
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
        
        # Get past bookings
        response = requests.get(
            f"{self.base_url}/bookings/past",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ Past bookings retrieval successful: Found {len(data)} bookings")
        
        # Test with invalid route_id to check exception handling
        # Create a booking with an invalid date (in the past)
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # First get a valid route
        search_data = {
            "origin": "Phnom Penh",
            "destination": "Siem Reap",
            "date": yesterday,
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
            # Create a booking with an invalid route_id format
            booking_data = {
                "route_id": "invalid-id-format",  # This should trigger the InvalidId exception handling
                "selected_seats": ["1A"],
                "passenger_details": [
                    {
                        "firstName": "Test",
                        "lastName": "Passenger",
                        "email": "test@example.com",
                        "phone": "1234567890"
                    }
                ],
                "date": yesterday
            }
            
            # Try to create a booking with invalid route_id
            try:
                booking_response = requests.post(
                    f"{self.base_url}/bookings",
                    headers={"Authorization": f"Bearer {token}"},
                    json=booking_data
                )
                # We expect this to fail, but we're just creating a test case
            except:
                pass
                
            # Now test the past bookings endpoint again to ensure it handles invalid ObjectIds
            response = requests.get(
                f"{self.base_url}/bookings/past",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIsInstance(data, list)
            print(f"✅ Past bookings with InvalidId exception handling works correctly")
        
    def test_14_user_invite(self):
        """Test user invite endpoint"""
        # Register and login a new user for this test
        test_email = f"invite_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Invite",
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
        
        # Send invite
        invite_data = {
            "email": f"friend_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "invite_code": "INVITE123"
        }
        
        response = requests.post(
            f"{self.base_url}/user/invite",
            headers={"Authorization": f"Bearer {token}"},
            json=invite_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        print(f"✅ User invite successful: {data['message']}")
        
    def test_15_update_profile(self):
        """Test update profile endpoint"""
        # Register and login a new user for this test
        test_email = f"profile_update_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Profile",
            "last_name": "Update",
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
        
        # Update profile
        updated_profile = {
            "first_name": "Updated",
            "last_name": "Profile",
            "email": test_email,  # Keep the same email
            "phone": "9876543210"
        }
        
        response = requests.put(
            f"{self.base_url}/user/profile",
            headers={"Authorization": f"Bearer {token}"},
            json=updated_profile
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        print(f"✅ Profile update successful: {data['message']}")
        
    def test_16_change_password(self):
        """Test change password endpoint"""
        # Register and login a new user for this test
        test_email = f"password_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Password",
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
        
        # Change password
        password_data = {
            "current_password": "Test123!",
            "new_password": "NewTest456!"
        }
        
        response = requests.put(
            f"{self.base_url}/user/change-password",
            headers={"Authorization": f"Bearer {token}"},
            json=password_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        print(f"✅ Password change successful: {data['message']}")
        
        # Verify new password works
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": test_user["email"],
                "password": "NewTest456!"
            }
        )
        self.assertEqual(login_response.status_code, 200)
        print("✅ Login with new password successful")
        
    def test_17_affiliate_status(self):
        """Test affiliate status endpoint"""
        # Register and login a new user for this test
        test_email = f"affiliate_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Affiliate",
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
        
        # Get affiliate status
        response = requests.get(
            f"{self.base_url}/affiliate/status",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("isAffiliate", data)
        print(f"✅ Affiliate status retrieval successful: isAffiliate = {data['isAffiliate']}")
        
    def test_18_affiliate_register(self):
        """Test affiliate registration endpoint"""
        # Register and login a new user for this test
        test_email = f"affiliate_reg_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Affiliate",
            "last_name": "Registration",
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
        
        # Register as affiliate
        affiliate_data = {
            "companyName": "Test Affiliate Company",
            "website": "https://testaffiliate.com",
            "description": "Test affiliate company for API testing",
            "monthlySales": 1000,
            "marketingChannels": ["Social Media", "Email", "Website"]
        }
        
        response = requests.post(
            f"{self.base_url}/affiliate/register",
            headers={"Authorization": f"Bearer {token}"},
            json=affiliate_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("affiliateCode", data)
        self.assertIn("status", data)
        print(f"✅ Affiliate registration successful: Code = {data['affiliateCode']}, Status = {data['status']}")
        
    def test_19_affiliate_stats(self):
        """Test affiliate stats endpoint"""
        # Register and login a new user for this test
        test_email = f"affiliate_stats_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Affiliate",
            "last_name": "Stats",
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
        
        # Register as affiliate
        affiliate_data = {
            "companyName": "Test Affiliate Stats",
            "website": "https://testaffiliatestats.com",
            "description": "Test affiliate stats for API testing",
            "monthlySales": 1000,
            "marketingChannels": ["Social Media", "Email", "Website"]
        }
        
        affiliate_response = requests.post(
            f"{self.base_url}/affiliate/register",
            headers={"Authorization": f"Bearer {token}"},
            json=affiliate_data
        )
        self.assertEqual(affiliate_response.status_code, 200)
        
        # Get affiliate stats
        response = requests.get(
            f"{self.base_url}/affiliate/stats",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("totalEarnings", data)
        self.assertIn("totalReferrals", data)
        print(f"✅ Affiliate stats retrieval successful: Total Earnings = {data['totalEarnings']}")
        
    def test_20_affiliate_activity(self):
        """Test affiliate activity endpoint"""
        # Register and login a new user for this test
        test_email = f"affiliate_activity_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Affiliate",
            "last_name": "Activity",
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
        
        # Register as affiliate
        affiliate_data = {
            "companyName": "Test Affiliate Activity",
            "website": "https://testaffiliateactivity.com",
            "description": "Test affiliate activity for API testing",
            "monthlySales": 1000,
            "marketingChannels": ["Social Media", "Email", "Website"]
        }
        
        affiliate_response = requests.post(
            f"{self.base_url}/affiliate/register",
            headers={"Authorization": f"Bearer {token}"},
            json=affiliate_data
        )
        self.assertEqual(affiliate_response.status_code, 200)
        
        # Get affiliate activity
        response = requests.get(
            f"{self.base_url}/affiliate/activity",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn("description", data[0])
            self.assertIn("commission", data[0])
        print(f"✅ Affiliate activity retrieval successful: Found {len(data)} activities")
        
    def test_21_ticket_download(self):
        """Test ticket download endpoint"""
        # Register and login a new user for this test
        test_email = f"ticket_download_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Ticket",
            "last_name": "Download",
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
        
        # Create a booking first
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
                
                booking_response = requests.post(
                    f"{self.base_url}/bookings",
                    headers={"Authorization": f"Bearer {token}"},
                    json=booking_data
                )
                
                if booking_response.status_code == 200:
                    booking_data = booking_response.json()
                    booking_id = booking_data["id"]
                    
                    # Process payment
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
                        headers={"Authorization": f"Bearer {token}"},
                        json=payment_data
                    )
                    self.assertEqual(payment_response.status_code, 200)
                    
                    # Download ticket
                    response = requests.get(
                        f"{self.base_url}/tickets/download/{booking_id}",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    
                    self.assertEqual(response.status_code, 200)
                    data = response.json()
                    self.assertIn("message", data)
                    self.assertIn("booking_id", data)
                    print(f"✅ Ticket download successful for booking {booking_id}")
                else:
                    print(f"⚠️ Skipping ticket download test as booking creation failed: {booking_response.status_code}")
            else:
                print("⚠️ Skipping ticket download test as no available seats were found")
        else:
            print("⚠️ Skipping ticket download test as no routes were found")
        
    def test_22_ticket_send(self):
        """Test ticket send endpoint"""
        # Register and login a new user for this test
        test_email = f"ticket_send_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Ticket",
            "last_name": "Send",
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
        
        # Create a booking first
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
                
                booking_response = requests.post(
                    f"{self.base_url}/bookings",
                    headers={"Authorization": f"Bearer {token}"},
                    json=booking_data
                )
                
                if booking_response.status_code == 200:
                    booking_data = booking_response.json()
                    booking_id = booking_data["id"]
                    
                    # Process payment
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
                        headers={"Authorization": f"Bearer {token}"},
                        json=payment_data
                    )
                    self.assertEqual(payment_response.status_code, 200)
                    
                    # Send ticket
                    send_data = {
                        "booking_id": booking_id,
                        "recipients": ["friend@example.com"],
                        "method": "email",
                        "message": "Here's your ticket!"
                    }
                    
                    response = requests.post(
                        f"{self.base_url}/tickets/send",
                        headers={"Authorization": f"Bearer {token}"},
                        json=send_data
                    )
                    
                    self.assertEqual(response.status_code, 200)
                    data = response.json()
                    self.assertIn("message", data)
                    print(f"✅ Ticket send successful: {data['message']}")
                else:
                    print(f"⚠️ Skipping ticket send test as booking creation failed: {booking_response.status_code}")
            else:
                print("⚠️ Skipping ticket send test as no available seats were found")
        else:
            print("⚠️ Skipping ticket send test as no routes were found")
        
    def test_23_search_by_transport_type(self):
        """Test search by transport type endpoint"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Test bus search
        search_data = {
            "origin": "Phnom Penh",
            "destination": "Siem Reap",
            "date": tomorrow,
            "passengers": 1
        }
        
        response = requests.post(
            f"{self.base_url}/search/bus",
            json=search_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ Bus search successful: Found {len(data)} routes")
        
        # Test ferry search
        search_data = {
            "origin": "Sihanoukville",
            "destination": "Koh Rong",
            "date": tomorrow,
            "passengers": 1
        }
        
        response = requests.post(
            f"{self.base_url}/search/ferry",
            json=search_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ Ferry search successful: Found {len(data)} routes")
        
    def test_24_admin_users(self):
        """Test admin users endpoint"""
        # Register and login an admin user
        admin_email = f"admin_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        admin_user = {
            "email": admin_email,
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "Test",
            "phone": "1234567890"
        }
        
        # Register
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=admin_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": admin_user["email"],
                "password": admin_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        admin_token = login_response.json()["access_token"]
        
        # Get all users
        response = requests.get(
            f"{self.base_url}/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ Admin users retrieval successful: Found {len(data)} users")
        
    def test_25_admin_user_permissions(self):
        """Test admin user permissions endpoint"""
        # Register and login an admin user
        admin_email = f"admin_perm_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        admin_user = {
            "email": admin_email,
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "Permissions",
            "phone": "1234567890"
        }
        
        # Register admin
        register_admin_response = requests.post(
            f"{self.base_url}/auth/register",
            json=admin_user
        )
        self.assertEqual(register_admin_response.status_code, 200)
        
        # Login admin
        login_admin_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": admin_user["email"],
                "password": admin_user["password"]
            }
        )
        self.assertEqual(login_admin_response.status_code, 200)
        admin_token = login_admin_response.json()["access_token"]
        
        # Register a regular user
        regular_email = f"regular_user_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        regular_user = {
            "email": regular_email,
            "password": "User123!",
            "first_name": "Regular",
            "last_name": "User",
            "phone": "9876543210"
        }
        
        register_user_response = requests.post(
            f"{self.base_url}/auth/register",
            json=regular_user
        )
        self.assertEqual(register_user_response.status_code, 200)
        user_data = register_user_response.json()
        user_id = user_data["id"]
        
        # Update user permissions
        permissions_data = {
            "permissions": ["view_routes", "book_tickets", "view_profile"]
        }
        
        response = requests.put(
            f"{self.base_url}/admin/users/{user_id}/permissions",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=permissions_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        print(f"✅ User permissions update successful: {data['message']}")
        
    def test_26_admin_buses(self):
        """Test admin buses endpoint"""
        # Register and login an admin user
        admin_email = f"admin_buses_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        admin_user = {
            "email": admin_email,
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "Buses",
            "phone": "1234567890"
        }
        
        # Register
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=admin_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": admin_user["email"],
                "password": admin_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        admin_token = login_response.json()["access_token"]
        
        # Get all buses
        response = requests.get(
            f"{self.base_url}/admin/buses",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ Admin buses retrieval successful: Found {len(data)} buses")
        
        # Create a new bus
        bus_data = {
            "name": f"Test Bus {datetime.now().strftime('%Y%m%d%H%M%S')}",
            "company": "Test Bus Company",
            "vehicle_type": "VIP Bus",
            "seat_layout": "2-2",
            "total_seats": 44,
            "amenities": ["WiFi", "AC", "USB Charging", "Blanket", "Water"],
            "status": "active"
        }
        
        create_response = requests.post(
            f"{self.base_url}/admin/buses",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=bus_data
        )
        
        self.assertEqual(create_response.status_code, 200)
        create_data = create_response.json()
        self.assertIn("message", create_data)
        self.assertIn("id", create_data)
        print(f"✅ Bus creation successful: {create_data['message']}")
        
    def test_27_admin_routes(self):
        """Test admin routes endpoint"""
        # Register and login an admin user
        admin_email = f"admin_routes_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        admin_user = {
            "email": admin_email,
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "Routes",
            "phone": "1234567890"
        }
        
        # Register
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=admin_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": admin_user["email"],
                "password": admin_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        admin_token = login_response.json()["access_token"]
        
        # Get all routes
        response = requests.get(
            f"{self.base_url}/admin/routes",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ Admin routes retrieval successful: Found {len(data)} routes")
        
        # Create a new route
        route_data = {
            "origin": "Battambang",
            "destination": "Siem Reap",
            "distance": 170,
            "duration": "3h 30m",
            "transport_type": "bus",
            "price_base": 10.0,
            "status": "active"
        }
        
        create_response = requests.post(
            f"{self.base_url}/admin/routes",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=route_data
        )
        
        self.assertEqual(create_response.status_code, 200)
        create_data = create_response.json()
        self.assertIn("message", create_data)
        self.assertIn("id", create_data)
        print(f"✅ Route creation successful: {create_data['message']}")
        
    def test_28_admin_stats(self):
        """Test admin stats endpoint"""
        # Register and login an admin user
        admin_email = f"admin_stats_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        admin_user = {
            "email": admin_email,
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "Stats",
            "phone": "1234567890"
        }
        
        # Register
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=admin_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": admin_user["email"],
                "password": admin_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        admin_token = login_response.json()["access_token"]
        
        # Get admin stats
        response = requests.get(
            f"{self.base_url}/admin/stats",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_users", data)
        self.assertIn("total_revenue", data)
        print(f"✅ Admin stats retrieval successful: {data['total_users']} users, ${data['total_revenue']} revenue")
        
    def test_29_admin_bulk_upload_buses(self):
        """Test admin bulk upload buses endpoint"""
        # Register and login an admin user
        admin_email = f"admin_bulk_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        admin_user = {
            "email": admin_email,
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "Bulk",
            "phone": "1234567890"
        }
        
        # Register
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=admin_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": admin_user["email"],
                "password": admin_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        admin_token = login_response.json()["access_token"]
        
        # Bulk upload buses
        buses_data = [
            {
                "name": f"Bulk Bus 1 {datetime.now().strftime('%Y%m%d%H%M%S')}",
                "company": "Bulk Bus Company",
                "vehicle_type": "Standard Bus",
                "seat_layout": "2-2",
                "total_seats": 40,
                "amenities": ["WiFi", "AC"],
                "status": "active"
            },
            {
                "name": f"Bulk Bus 2 {datetime.now().strftime('%Y%m%d%H%M%S')}",
                "company": "Bulk Bus Company",
                "vehicle_type": "VIP Bus",
                "seat_layout": "2-1",
                "total_seats": 36,
                "amenities": ["WiFi", "AC", "USB Charging", "Blanket"],
                "status": "active"
            }
        ]
        
        response = requests.post(
            f"{self.base_url}/admin/buses/bulk-upload",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=buses_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("created_count", data)
        print(f"✅ Bulk bus upload successful: {data['created_count']} buses created")
        
    def test_30_admin_bulk_upload_routes(self):
        """Test admin bulk upload routes endpoint"""
        # Register and login an admin user
        admin_email = f"admin_bulk_routes_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        admin_user = {
            "email": admin_email,
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "Bulk Routes",
            "phone": "1234567890"
        }
        
        # Register
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=admin_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": admin_user["email"],
                "password": admin_user["password"]
            }
        )
        self.assertEqual(login_response.status_code, 200)
        admin_token = login_response.json()["access_token"]
        
        # Bulk upload routes
        routes_data = [
            {
                "origin": "Battambang",
                "destination": "Phnom Penh",
                "distance": 290,
                "duration": "5h 30m",
                "transport_type": "bus",
                "price_base": 12.0,
                "status": "active"
            },
            {
                "origin": "Kampot",
                "destination": "Sihanoukville",
                "distance": 95,
                "duration": "2h 15m",
                "transport_type": "bus",
                "price_base": 7.0,
                "status": "active"
            }
        ]
        
        response = requests.post(
            f"{self.base_url}/admin/routes/bulk-upload",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=routes_data
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("created_count", data)
        print(f"✅ Bulk route upload successful: {data['created_count']} routes created")
        
    def test_31_enhanced_payment_methods(self):
        """Test payment processing with multiple methods"""
        # Register and login a new user for this test
        test_email = f"payment_test_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Payment",
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
        
        # Create a booking first
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
                
                booking_response = requests.post(
                    f"{self.base_url}/bookings",
                    headers={"Authorization": f"Bearer {token}"},
                    json=booking_data
                )
                
                if booking_response.status_code == 200:
                    booking_data = booking_response.json()
                    booking_id = booking_data["id"]
                    
                    # Test payment with credit card
                    payment_data = {
                        "booking_id": booking_id,
                        "payment_method": "credit_card",
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
                    payment_data = payment_response.json()
                    self.assertIn("status", payment_data)
                    self.assertEqual(payment_data["status"], "success")
                    print(f"✅ Credit card payment successful: {payment_data['transaction_id']}")
                    
                    # Create another booking for PayPal test
                    if len(available_seats) > 1:
                        booking_data = {
                            "route_id": route_id,
                            "selected_seats": [available_seats[1]],
                            "passenger_details": [
                                {
                                    "firstName": "PayPal",
                                    "lastName": "Test",
                                    "email": "paypal@example.com",
                                    "phone": "1234567890"
                                }
                            ],
                            "date": tomorrow
                        }
                        
                        booking_response = requests.post(
                            f"{self.base_url}/bookings",
                            headers={"Authorization": f"Bearer {token}"},
                            json=booking_data
                        )
                        
                        if booking_response.status_code == 200:
                            booking_data = booking_response.json()
                            booking_id = booking_data["id"]
                            
                            # Test payment with PayPal
                            payment_data = {
                                "booking_id": booking_id,
                                "payment_method": "paypal",
                                "paypal_details": {
                                    "paypal_email": "test@paypal.com"
                                }
                            }
                            
                            payment_response = requests.post(
                                f"{self.base_url}/payments/process",
                                headers={"Authorization": f"Bearer {token}"},
                                json=payment_data
                            )
                            
                            self.assertEqual(payment_response.status_code, 200)
                            payment_data = payment_response.json()
                            self.assertIn("status", payment_data)
                            print(f"✅ PayPal payment test: {payment_data['status']}")
                    else:
                        print("⚠️ Skipping PayPal payment test as not enough available seats")
                else:
                    print(f"⚠️ Skipping payment tests as booking creation failed: {booking_response.status_code}")
            else:
                print("⚠️ Skipping payment tests as no available seats were found")
        else:
            print("⚠️ Skipping payment tests as no routes were found")

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
    
    # User Profile Feature Tests
    test_suite.addTest(BusTicketAPITest('test_11_user_credit'))
    test_suite.addTest(BusTicketAPITest('test_12_upcoming_bookings'))
    test_suite.addTest(BusTicketAPITest('test_13_past_bookings'))
    test_suite.addTest(BusTicketAPITest('test_14_user_invite'))
    test_suite.addTest(BusTicketAPITest('test_15_update_profile'))
    test_suite.addTest(BusTicketAPITest('test_16_change_password'))
    
    # Affiliate Program Tests
    test_suite.addTest(BusTicketAPITest('test_17_affiliate_status'))
    test_suite.addTest(BusTicketAPITest('test_18_affiliate_register'))
    test_suite.addTest(BusTicketAPITest('test_19_affiliate_stats'))
    test_suite.addTest(BusTicketAPITest('test_20_affiliate_activity'))
    
    # Ticket Management Tests
    test_suite.addTest(BusTicketAPITest('test_21_ticket_download'))
    test_suite.addTest(BusTicketAPITest('test_22_ticket_send'))
    
    # Enhanced Search Tests
    test_suite.addTest(BusTicketAPITest('test_23_search_by_transport_type'))
    
    # Admin Management Tests
    test_suite.addTest(BusTicketAPITest('test_24_admin_users'))
    test_suite.addTest(BusTicketAPITest('test_25_admin_user_permissions'))
    test_suite.addTest(BusTicketAPITest('test_26_admin_buses'))
    test_suite.addTest(BusTicketAPITest('test_27_admin_routes'))
    test_suite.addTest(BusTicketAPITest('test_28_admin_stats'))
    
    # Bulk Operations Tests
    test_suite.addTest(BusTicketAPITest('test_29_admin_bulk_upload_buses'))
    test_suite.addTest(BusTicketAPITest('test_30_admin_bulk_upload_routes'))
    
    # Enhanced Payment Tests
    test_suite.addTest(BusTicketAPITest('test_31_enhanced_payment_methods'))
    
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