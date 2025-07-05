import requests
import unittest
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sys

# Load environment variables from frontend/.env
load_dotenv('/app/frontend/.env')

class CriticalIssuesTest(unittest.TestCase):
    """Test suite for critical issues in BusTicket API"""
    
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
        
        if register_response.status_code != 200:
            print(f"Failed to register test user: {register_response.text}")
            self.token = None
            return
            
        # Login the test user
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }
        )
        
        if login_response.status_code != 200:
            print(f"Failed to login test user: {login_response.text}")
            self.token = None
            return
            
        self.token = login_response.json()["access_token"]
        print(f"Successfully authenticated test user: {self.test_user['email']}")
        
    def test_01_seat_layout_api(self):
        """Test the seat layout API that's causing 'Failed to fetch seat layout' error"""
        print("\n=== Testing Seat Layout API ===")
        
        # First search for routes to get a valid route_id
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
        
        self.assertEqual(search_response.status_code, 200, "Search API failed")
        routes = search_response.json()
        
        if not routes:
            self.fail("No routes found for testing seat layout")
        
        route_id = routes[0]["id"]
        print(f"Found route ID for testing: {route_id}")
        
        # Test seat layout endpoint with authentication
        seats_response = requests.get(
            f"{self.base_url}/seats/{route_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Seat layout API response status: {seats_response.status_code}")
        
        if seats_response.status_code != 200:
            print(f"Error response: {seats_response.text[:200]}")
            self.fail(f"Seat layout API failed with status code: {seats_response.status_code}")
        
        seats_data = seats_response.json()
        
        # Check if the response contains the expected data
        self.assertIn("seats", seats_data, "Seats data missing from response")
        self.assertIn("layout", seats_data, "Layout data missing from response")
        
        print(f"✅ Seat layout API working correctly. Found {len(seats_data['seats'])} seats.")
        
    def test_02_payment_method_selection(self):
        """Test the payment processing endpoints that are causing 'Select payment method' error"""
        print("\n=== Testing Payment Method Selection ===")
        
        # Create a booking first
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # 1. Search for routes
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
        
        self.assertEqual(search_response.status_code, 200, "Search API failed")
        routes = search_response.json()
        
        if not routes:
            self.fail("No routes found for testing payment")
        
        route_id = routes[0]["id"]
        print(f"Found route ID for testing: {route_id}")
        
        # 2. Get seat layout
        seats_response = requests.get(
            f"{self.base_url}/seats/{route_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        self.assertEqual(seats_response.status_code, 200, "Seat layout API failed")
        seats_data = seats_response.json()
        
        # Find available seats
        available_seats = []
        for seat in seats_data.get("seats", []):
            if seat.get("status") == "available":
                available_seats.append(seat.get("id"))
                break
        
        if not available_seats:
            self.fail("No available seats found for testing payment")
        
        print(f"Found available seat for testing: {available_seats[0]}")
        
        # 3. Create booking
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
        
        print(f"Booking API response status: {booking_response.status_code}")
        
        if booking_response.status_code != 200:
            print(f"Error response: {booking_response.text[:200]}")
            self.fail(f"Booking API failed with status code: {booking_response.status_code}")
        
        booking_data = booking_response.json()
        booking_id = booking_data.get("id") or booking_data.get("booking_id")
        
        if not booking_id:
            self.fail("No booking ID returned from booking API")
        
        print(f"Created booking with ID: {booking_id}")
        
        # 4. Test payment with credit card
        payment_data_card = {
            "booking_id": booking_id,
            "payment_method": "card",
            "card_details": {
                "cardNumber": "4111111111111111",
                "expiryDate": "12/25",
                "cvv": "123",
                "cardHolderName": "Test User"
            }
        }
        
        card_payment_response = requests.post(
            f"{self.base_url}/payments/process",
            headers={"Authorization": f"Bearer {self.token}"},
            json=payment_data_card
        )
        
        print(f"Card payment API response status: {card_payment_response.status_code}")
        
        if card_payment_response.status_code != 200:
            print(f"Error response: {card_payment_response.text[:200]}")
            self.fail(f"Card payment API failed with status code: {card_payment_response.status_code}")
        
        card_payment_result = card_payment_response.json()
        self.assertIn("status", card_payment_result, "Status missing from payment response")
        
        # 5. Create another booking for PayPal test
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
            print(f"Error response: {booking_response.text[:200]}")
            self.fail(f"Booking API failed with status code: {booking_response.status_code}")
        
        booking_data = booking_response.json()
        booking_id = booking_data.get("id") or booking_data.get("booking_id")
        
        # 6. Test payment with PayPal
        payment_data_paypal = {
            "booking_id": booking_id,
            "payment_method": "paypal",
            "payment_data": {
                "paypal_email": "test@example.com",
                "paypal_transaction_id": "PAYPAL123456789"
            }
        }
        
        paypal_payment_response = requests.post(
            f"{self.base_url}/payments/process",
            headers={"Authorization": f"Bearer {self.token}"},
            json=payment_data_paypal
        )
        
        print(f"PayPal payment API response status: {paypal_payment_response.status_code}")
        
        if paypal_payment_response.status_code != 200:
            print(f"Error response: {paypal_payment_response.text[:200]}")
            self.fail(f"PayPal payment API failed with status code: {paypal_payment_response.status_code}")
        
        paypal_payment_result = paypal_payment_response.json()
        self.assertIn("status", paypal_payment_result, "Status missing from payment response")
        
        print("✅ Payment method selection working correctly for both card and PayPal")
        
    def test_03_affiliate_management_apis(self):
        """Test the affiliate management dashboard APIs"""
        print("\n=== Testing Affiliate Management APIs ===")
        
        # 1. Check affiliate status
        status_response = requests.get(
            f"{self.base_url}/affiliate/status",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Affiliate status API response status: {status_response.status_code}")
        
        if status_response.status_code != 200:
            print(f"Error response: {status_response.text[:200]}")
            self.fail(f"Affiliate status API failed with status code: {status_response.status_code}")
        
        status_data = status_response.json()
        self.assertIn("isAffiliate", status_data, "isAffiliate missing from status response")
        
        # 2. Register as affiliate
        affiliate_data = {
            "companyName": "Test Affiliate Company",
            "website": "https://testaffiliate.com",
            "description": "Test affiliate company for API testing",
            "monthlySales": 1000,
            "marketingChannels": ["Social Media", "Email", "Website"]
        }
        
        register_response = requests.post(
            f"{self.base_url}/affiliate/register",
            headers={"Authorization": f"Bearer {self.token}"},
            json=affiliate_data
        )
        
        print(f"Affiliate registration API response status: {register_response.status_code}")
        
        if register_response.status_code != 200:
            print(f"Error response: {register_response.text[:200]}")
            self.fail(f"Affiliate registration API failed with status code: {register_response.status_code}")
        
        register_data = register_response.json()
        self.assertIn("affiliateCode", register_data, "affiliateCode missing from registration response")
        
        # 3. Get affiliate stats
        stats_response = requests.get(
            f"{self.base_url}/affiliate/stats",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Affiliate stats API response status: {stats_response.status_code}")
        
        if stats_response.status_code != 200:
            print(f"Error response: {stats_response.text[:200]}")
            self.fail(f"Affiliate stats API failed with status code: {stats_response.status_code}")
        
        stats_data = stats_response.json()
        self.assertIn("totalEarnings", stats_data, "totalEarnings missing from stats response")
        
        # 4. Get affiliate activity
        activity_response = requests.get(
            f"{self.base_url}/affiliate/activity",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Affiliate activity API response status: {activity_response.status_code}")
        
        if activity_response.status_code != 200:
            print(f"Error response: {activity_response.text[:200]}")
            self.fail(f"Affiliate activity API failed with status code: {activity_response.status_code}")
        
        activity_data = activity_response.json()
        self.assertIsInstance(activity_data, list, "Activity data should be a list")
        
        print("✅ Affiliate management APIs working correctly")
        
    def test_04_user_profile_features(self):
        """Test the user profile endpoints that were previously showing 500 errors"""
        print("\n=== Testing User Profile Features ===")
        
        # 1. Test user credit endpoint
        credit_response = requests.get(
            f"{self.base_url}/user/credit",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"User credit API response status: {credit_response.status_code}")
        
        if credit_response.status_code != 200:
            print(f"Error response: {credit_response.text[:200]}")
            self.fail(f"User credit API failed with status code: {credit_response.status_code}")
        
        credit_data = credit_response.json()
        self.assertIn("balance", credit_data, "Balance missing from credit response")
        self.assertIn("transactions", credit_data, "Transactions missing from credit response")
        
        # 2. Test upcoming bookings endpoint
        upcoming_response = requests.get(
            f"{self.base_url}/bookings/upcoming",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Upcoming bookings API response status: {upcoming_response.status_code}")
        
        if upcoming_response.status_code != 200:
            print(f"Error response: {upcoming_response.text[:200]}")
            self.fail(f"Upcoming bookings API failed with status code: {upcoming_response.status_code}")
        
        upcoming_data = upcoming_response.json()
        self.assertIsInstance(upcoming_data, list, "Upcoming bookings data should be a list")
        
        # 3. Test past bookings endpoint
        past_response = requests.get(
            f"{self.base_url}/bookings/past",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Past bookings API response status: {past_response.status_code}")
        
        if past_response.status_code != 200:
            print(f"Error response: {past_response.text[:200]}")
            self.fail(f"Past bookings API failed with status code: {past_response.status_code}")
        
        past_data = past_response.json()
        self.assertIsInstance(past_data, list, "Past bookings data should be a list")
        
        # 4. Test user invite endpoint
        invite_data = {
            "email": f"friend_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "invite_code": "INVITE123"
        }
        
        invite_response = requests.post(
            f"{self.base_url}/user/invite",
            headers={"Authorization": f"Bearer {self.token}"},
            json=invite_data
        )
        
        print(f"User invite API response status: {invite_response.status_code}")
        
        if invite_response.status_code != 200:
            print(f"Error response: {invite_response.text[:200]}")
            self.fail(f"User invite API failed with status code: {invite_response.status_code}")
        
        invite_result = invite_response.json()
        self.assertIn("message", invite_result, "Message missing from invite response")
        
        # 5. Test profile update endpoint
        profile_data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": self.test_user["email"],
            "phone": "9876543210"
        }
        
        profile_response = requests.put(
            f"{self.base_url}/user/profile",
            headers={"Authorization": f"Bearer {self.token}"},
            json=profile_data
        )
        
        print(f"Profile update API response status: {profile_response.status_code}")
        
        if profile_response.status_code != 200:
            print(f"Error response: {profile_response.text[:200]}")
            self.fail(f"Profile update API failed with status code: {profile_response.status_code}")
        
        profile_result = profile_response.json()
        self.assertIn("message", profile_result, "Message missing from profile update response")
        
        print("✅ User profile features working correctly")
        
    def test_05_admin_management_apis(self):
        """Test the admin endpoints that were previously returning 500 errors"""
        print("\n=== Testing Admin Management APIs ===")
        
        # Create an admin user for testing
        admin_user = {
            "email": f"admin_user_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
            "password": "Admin123!",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "9876543210"
        }
        
        # Register admin user
        register_response = requests.post(
            f"{self.base_url}/auth/register",
            json=admin_user
        )
        
        self.assertEqual(register_response.status_code, 200, "Failed to register admin user")
        
        # Login admin user
        login_response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": admin_user["email"],
                "password": admin_user["password"]
            }
        )
        
        self.assertEqual(login_response.status_code, 200, "Failed to login admin user")
        admin_token = login_response.json()["access_token"]
        
        # 1. Test admin users endpoint
        users_response = requests.get(
            f"{self.base_url}/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        print(f"Admin users API response status: {users_response.status_code}")
        
        if users_response.status_code != 200:
            print(f"Error response: {users_response.text[:200]}")
            self.fail(f"Admin users API failed with status code: {users_response.status_code}")
        
        users_data = users_response.json()
        self.assertIsInstance(users_data, list, "Users data should be a list")
        
        # 2. Test admin routes endpoint
        routes_response = requests.get(
            f"{self.base_url}/admin/routes",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        print(f"Admin routes API response status: {routes_response.status_code}")
        
        if routes_response.status_code != 200:
            print(f"Error response: {routes_response.text[:200]}")
            self.fail(f"Admin routes API failed with status code: {routes_response.status_code}")
        
        routes_data = routes_response.json()
        self.assertIsInstance(routes_data, list, "Routes data should be a list")
        
        # 3. Test admin buses endpoint
        buses_response = requests.get(
            f"{self.base_url}/admin/buses",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        print(f"Admin buses API response status: {buses_response.status_code}")
        
        if buses_response.status_code != 200:
            print(f"Error response: {buses_response.text[:200]}")
            self.fail(f"Admin buses API failed with status code: {buses_response.status_code}")
        
        buses_data = buses_response.json()
        self.assertIsInstance(buses_data, list, "Buses data should be a list")
        
        # 4. Test admin stats endpoint
        stats_response = requests.get(
            f"{self.base_url}/admin/stats",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        print(f"Admin stats API response status: {stats_response.status_code}")
        
        if stats_response.status_code != 200:
            print(f"Error response: {stats_response.text[:200]}")
            self.fail(f"Admin stats API failed with status code: {stats_response.status_code}")
        
        stats_data = stats_response.json()
        self.assertIn("total_users", stats_data, "Total users missing from stats response")
        
        # 5. Test admin user permissions endpoint
        # First get a user ID to update
        if len(users_data) > 0:
            user_id = users_data[0]["id"]
            
            permissions_data = {
                "permissions": ["view_routes", "book_tickets", "view_profile"]
            }
            
            permissions_response = requests.put(
                f"{self.base_url}/admin/users/{user_id}/permissions",
                headers={"Authorization": f"Bearer {admin_token}"},
                json=permissions_data
            )
            
            print(f"Admin user permissions API response status: {permissions_response.status_code}")
            
            if permissions_response.status_code != 200:
                print(f"Error response: {permissions_response.text[:200]}")
                self.fail(f"Admin user permissions API failed with status code: {permissions_response.status_code}")
            
            permissions_result = permissions_response.json()
            self.assertIn("message", permissions_result, "Message missing from permissions response")
        
        print("✅ Admin management APIs working correctly")
        
    def test_06_booking_flow(self):
        """Test the complete booking flow from search to payment"""
        print("\n=== Testing Complete Booking Flow ===")
        
        # 1. Search for routes
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
        
        print(f"Search API response status: {search_response.status_code}")
        
        if search_response.status_code != 200:
            print(f"Error response: {search_response.text[:200]}")
            self.fail(f"Search API failed with status code: {search_response.status_code}")
        
        routes = search_response.json()
        
        if not routes:
            self.fail("No routes found for testing booking flow")
        
        route_id = routes[0]["id"]
        print(f"Found route ID for testing: {route_id}")
        
        # 2. Get seat layout
        seats_response = requests.get(
            f"{self.base_url}/seats/{route_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Seat layout API response status: {seats_response.status_code}")
        
        if seats_response.status_code != 200:
            print(f"Error response: {seats_response.text[:200]}")
            self.fail(f"Seat layout API failed with status code: {seats_response.status_code}")
        
        seats_data = seats_response.json()
        
        # Find available seats
        available_seats = []
        for seat in seats_data.get("seats", []):
            if seat.get("status") == "available":
                available_seats.append(seat.get("id"))
                if len(available_seats) >= 2:  # Get at least 2 seats to avoid conflicts
                    break
        
        if not available_seats:
            self.fail("No available seats found for testing booking flow")
            
        # Use a different seat for each test to avoid conflicts
        import random
        if len(available_seats) > 1:
            selected_seat = random.choice(available_seats)
        else:
            selected_seat = available_seats[0]
            
        print(f"Found available seat for testing: {selected_seat}")
        
        print(f"Found available seat for testing: {available_seats[0]}")
        
        # 3. Create booking
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
        
        print(f"Booking API response status: {booking_response.status_code}")
        
        if booking_response.status_code != 200:
            print(f"Error response: {booking_response.text[:200]}")
            self.fail(f"Booking API failed with status code: {booking_response.status_code}")
        
        booking_data = booking_response.json()
        booking_id = booking_data.get("id") or booking_data.get("booking_id")
        
        if not booking_id:
            self.fail("No booking ID returned from booking API")
        
        print(f"Created booking with ID: {booking_id}")
        
        # 4. Process payment
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
        
        print(f"Payment API response status: {payment_response.status_code}")
        
        if payment_response.status_code != 200:
            print(f"Error response: {payment_response.text[:200]}")
            self.fail(f"Payment API failed with status code: {payment_response.status_code}")
        
        payment_result = payment_response.json()
        self.assertIn("status", payment_result, "Status missing from payment response")
        
        # 5. Get booking details
        booking_details_response = requests.get(
            f"{self.base_url}/bookings/{booking_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        print(f"Booking details API response status: {booking_details_response.status_code}")
        
        if booking_details_response.status_code != 200:
            print(f"Error response: {booking_details_response.text[:200]}")
            self.fail(f"Booking details API failed with status code: {booking_details_response.status_code}")
        
        booking_details = booking_details_response.json()
        self.assertEqual(booking_details.get("status"), "paid", "Booking status should be 'paid' after payment")
        
        print("✅ Complete booking flow working correctly")

if __name__ == "__main__":
    # Create a test suite with the critical issue tests
    test_suite = unittest.TestSuite()
    test_suite.addTest(CriticalIssuesTest('test_01_seat_layout_api'))
    test_suite.addTest(CriticalIssuesTest('test_02_payment_method_selection'))
    test_suite.addTest(CriticalIssuesTest('test_03_affiliate_management_apis'))
    test_suite.addTest(CriticalIssuesTest('test_04_user_profile_features'))
    test_suite.addTest(CriticalIssuesTest('test_05_admin_management_apis'))
    test_suite.addTest(CriticalIssuesTest('test_06_booking_flow'))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)