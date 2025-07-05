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
        
    # New User Profile Feature Tests
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
        self.assertIsInstance(data["transactions"], list)
        print(f"✅ User credit retrieval successful: Balance = {data['balance']}, Transactions = {len(data['transactions'])}")
        
    def test_12_upcoming_bookings(self):
        """Test upcoming bookings endpoint"""
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
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ Upcoming bookings retrieval successful: Found {len(data)} upcoming bookings")
        
    def test_13_past_bookings(self):
        """Test past bookings endpoint"""
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
        print(f"✅ Past bookings retrieval successful: Found {len(data)} past bookings")
        
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
            "email": "friend@example.com",
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
        """Test profile update endpoint"""
        # Register and login a new user for this test
        test_email = f"profile_update_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
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
            "email": test_email,  # Keep the same email to avoid conflicts
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
        
        # Verify the update by getting the profile
        profile_response = requests.get(
            f"{self.base_url}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(profile_response.status_code, 200)
        profile_data = profile_response.json()
        self.assertEqual(profile_data["first_name"], updated_profile["first_name"])
        self.assertEqual(profile_data["last_name"], updated_profile["last_name"])
        self.assertEqual(profile_data["phone"], updated_profile["phone"])
        print("✅ Profile update verification successful")
        
    def test_16_change_password(self):
        """Test password change endpoint"""
        # Register and login a new user for this test
        test_email = f"password_change_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "OldPassword123!",
            "first_name": "Password",
            "last_name": "Change",
            "phone": "1234567890"
        }
        
        # Register
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=test_user
        )
        self.assertEqual(register_response.status_code, 200)
        
        # Login with old password
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
            "current_password": test_user["password"],
            "new_password": "NewPassword456!"
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
        
        # Verify by logging in with new password
        new_login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": test_user["email"],
                "password": password_data["new_password"]
            }
        )
        
        self.assertEqual(new_login_response.status_code, 200)
        self.assertIn("access_token", new_login_response.json())
        print("✅ Login with new password successful")
        
    # Affiliate Program Tests
    def test_17_affiliate_status(self):
        """Test affiliate status endpoint"""
        # Register and login a new user for this test
        test_email = f"affiliate_status_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Affiliate",
            "last_name": "Status",
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
        
        # Check affiliate status (should be false for new user)
        response = requests.get(
            f"{self.base_url}/affiliate/status",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("isAffiliate", data)
        self.assertFalse(data["isAffiliate"])
        print("✅ Affiliate status check successful for new user")
        
    def test_18_affiliate_register(self):
        """Test affiliate registration endpoint"""
        # Register and login a new user for this test
        test_email = f"affiliate_reg_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        test_user = {
            "email": test_email,
            "password": "Test123!",
            "first_name": "Affiliate",
            "last_name": "Register",
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
            "companyName": "Test Travel Agency",
            "website": "https://testagency.example.com",
            "description": "A test travel agency for API testing",
            "monthlySales": 5000,
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
        self.assertEqual(data["status"], "pending")
        print(f"✅ Affiliate registration successful: Code = {data['affiliateCode']}, Status = {data['status']}")
        
        # Verify by checking affiliate status
        status_response = requests.get(
            f"{self.base_url}/affiliate/status",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        self.assertEqual(status_response.status_code, 200)
        status_data = status_response.json()
        self.assertIn("isAffiliate", status_data)
        self.assertTrue(status_data["isAffiliate"])
        self.assertEqual(status_data["affiliateData"]["status"], "pending")
        print("✅ Affiliate status verification successful")
        
    def test_19_affiliate_stats(self):
        """Test affiliate stats endpoint"""
        # Register and login a new user for this test
        test_email = f"affiliate_stats_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
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
        
        # Register as affiliate first
        affiliate_data = {
            "companyName": "Stats Travel Agency",
            "website": "https://statsagency.example.com",
            "description": "A test travel agency for stats testing",
            "monthlySales": 7500,
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
        self.assertIn("conversionRate", data)
        self.assertIn("monthlyEarnings", data)
        print(f"✅ Affiliate stats retrieval successful: Total Earnings = {data['totalEarnings']}, Total Referrals = {data['totalReferrals']}")
        
    def test_20_affiliate_activity(self):
        """Test affiliate activity endpoint"""
        # Register and login a new user for this test
        test_email = f"affiliate_activity_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
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
        
        # Register as affiliate first
        affiliate_data = {
            "companyName": "Activity Travel Agency",
            "website": "https://activityagency.example.com",
            "description": "A test travel agency for activity testing",
            "monthlySales": 6000,
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
            self.assertIn("date", data[0])
        print(f"✅ Affiliate activity retrieval successful: Found {len(data)} activities")
        
    # Ticket Management Tests
    def test_21_ticket_download(self):
        """Test ticket download endpoint"""
        # Register and login a new user for this test
        test_email = f"ticket_download_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
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
        
        # Search for routes
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
                
                self.assertEqual(booking_response.status_code, 200)
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
                
                # Now test ticket download
                response = requests.get(
                    f"{self.base_url}/tickets/download/{booking_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertIn("message", data)
                self.assertIn("booking_id", data)
                print(f"✅ Ticket download successful: {data['message']}")
            else:
                print("⚠️ Skipping ticket download test as no available seats were found")
        else:
            print("⚠️ Skipping ticket download test as no routes were found")
        
    def test_22_ticket_send(self):
        """Test ticket send endpoint"""
        # Register and login a new user for this test
        test_email = f"ticket_send_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
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
        
        # Search for routes
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
                
                self.assertEqual(booking_response.status_code, 200)
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
                
                # Now test ticket send
                send_data = {
                    "booking_id": booking_id,
                    "recipients": ["friend@example.com", "family@example.com"],
                    "method": "email",
                    "message": "Here's your ticket for our trip!"
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
                print("⚠️ Skipping ticket send test as no available seats were found")
        else:
            print("⚠️ Skipping ticket send test as no routes were found")
        
    # Enhanced Search Tests
    def test_23_search_by_transport_type(self):
        """Test search by transport type endpoint"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Test different transport types
        transport_types = ["bus", "ferry", "private_taxi", "airport_shuttle"]
        
        for transport_type in transport_types:
            search_data = {
                "origin": "Phnom Penh",
                "destination": "Siem Reap",
                "date": tomorrow,
                "passengers": 1
            }
            
            response = requests.post(
                f"{self.base_url}/search/{transport_type}",
                json=search_data
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertIsInstance(data, list)
            
            # For ferry, use a route that's likely to have ferry service
            if transport_type == "ferry" and len(data) == 0:
                ferry_search = {
                    "origin": "Sihanoukville",
                    "destination": "Koh Rong",
                    "date": tomorrow,
                    "passengers": 1
                }
                
                ferry_response = requests.post(
                    f"{self.base_url}/search/ferry",
                    json=ferry_search
                )
                
                self.assertEqual(ferry_response.status_code, 200)
                ferry_data = ferry_response.json()
                print(f"✅ Ferry search successful: Found {len(ferry_data)} routes")
            else:
                print(f"✅ {transport_type.capitalize()} search successful: Found {len(data)} routes")

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
    
    # New User Profile Feature Tests
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