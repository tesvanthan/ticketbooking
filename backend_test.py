import requests
import unittest
import json
from datetime import datetime, timedelta

class BusTicketAPITest(unittest.TestCase):
    """Test suite for BusTicket API endpoints"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.base_url = "https://4e850de7-0fe2-4e5f-bc14-102dd2b91bee.preview.emergentagent.com/api"
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
        
    def test_05_search_routes(self):
        """Test route search functionality"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
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
            print(f"✅ Route search successful: Found {len(data)} routes")
        else:
            print("⚠️ Route search returned no results, but API is working")
            
    def test_06_get_suggestions(self):
        """Test route suggestions for autocomplete"""
        response = requests.get(f"{self.base_url}/suggestions?q=Phnom")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn("Phnom Penh", data)
            print(f"✅ Route suggestions successful: Found {len(data)} suggestions")
        else:
            print("⚠️ Route suggestions returned no results, but API is working")
            
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
        if not self.token:
            self.test_03_login_user()
            
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
                    headers={"Authorization": f"Bearer {self.token}"},
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
                    headers={"Authorization": f"Bearer {self.token}"},
                    json=payment_data
                )
                
                self.assertEqual(payment_response.status_code, 200)
                payment_result = payment_response.json()
                self.assertEqual(payment_result["status"], "success")
                print(f"✅ Payment processing successful: {payment_result['transaction_id']}")
            else:
                print("⚠️ Skipping booking test as no available seats were found")
        else:
            print("⚠️ Skipping booking test as no routes were found")
            
    def test_10_get_user_bookings(self):
        """Test retrieving user bookings"""
        if not self.token:
            self.test_03_login_user()
            
        response = requests.get(
            f"{self.base_url}/bookings",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        print(f"✅ User bookings retrieval successful: Found {len(data)} bookings")

def run_tests():
    """Run all tests in order"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(BusTicketAPITest('test_01_health_check'))
    test_suite.addTest(BusTicketAPITest('test_02_register_user'))
    test_suite.addTest(BusTicketAPITest('test_03_login_user'))
    test_suite.addTest(BusTicketAPITest('test_04_get_user_profile'))
    test_suite.addTest(BusTicketAPITest('test_05_search_routes'))
    test_suite.addTest(BusTicketAPITest('test_06_get_suggestions'))
    test_suite.addTest(BusTicketAPITest('test_07_get_popular_destinations'))
    test_suite.addTest(BusTicketAPITest('test_08_get_seat_layout'))
    test_suite.addTest(BusTicketAPITest('test_09_create_booking'))
    test_suite.addTest(BusTicketAPITest('test_10_get_user_bookings'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

if __name__ == "__main__":
    print("🚀 Starting BusTicket API Tests...")
    run_tests()