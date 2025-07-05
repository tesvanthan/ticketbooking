#!/bin/bash

echo "🚀 BusTicket Platform Integration Test"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BACKEND_URL="http://localhost:8001"
FRONTEND_URL="http://localhost:3000"

echo -e "${BLUE}Testing Backend API...${NC}"

# Test 1: Health Check
echo -n "1. Health Check: "
response=$(curl -s "${BACKEND_URL}/api/")
if [[ $response == *"BusTicket API is running"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    exit 1
fi

# Test 2: User Registration
echo -n "2. User Registration: "
email="test_$(date +%s)@example.com"
register_response=$(curl -s -X POST "${BACKEND_URL}/api/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"${email}\",\"password\":\"Test123!\",\"first_name\":\"Test\",\"last_name\":\"User\"}")

if [[ $register_response == *"\"email\":"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $register_response"
    exit 1
fi

# Test 3: User Login
echo -n "3. User Login: "
login_response=$(curl -s -X POST "${BACKEND_URL}/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"${email}\",\"password\":\"Test123!\"}")

if [[ $login_response == *"access_token"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
    # Extract token for subsequent requests
    token=$(echo $login_response | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $login_response"
    exit 1
fi

# Test 4: Route Search
echo -n "4. Route Search: "
tomorrow=$(date -d "tomorrow" +%Y-%m-%d)
search_response=$(curl -s -X POST "${BACKEND_URL}/api/search" \
    -H "Content-Type: application/json" \
    -d "{\"origin\":\"Phnom Penh\",\"destination\":\"Siem Reap\",\"date\":\"${tomorrow}\",\"passengers\":1,\"transport_type\":\"bus\"}")

if [[ $search_response == *"\"id\":"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
    # Extract route ID for seat selection test
    route_id=$(echo $search_response | grep -o '"id":"[^"]*' | head -1 | cut -d'"' -f4)
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $search_response"
    exit 1
fi

# Test 5: Seat Layout
echo -n "5. Seat Layout: "
seat_response=$(curl -s "${BACKEND_URL}/api/seats/${route_id}?date=${tomorrow}")
if [[ $seat_response == *"seat_layout"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $seat_response"
    exit 1
fi

# Test 6: Route Suggestions
echo -n "6. Route Suggestions: "
suggestions_response=$(curl -s "${BACKEND_URL}/api/suggestions?q=Phnom")
if [[ $suggestions_response == *"Phnom Penh"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $suggestions_response"
    exit 1
fi

# Test 7: Frontend Accessibility
echo -n "7. Frontend Accessibility: "
frontend_response=$(curl -s "${FRONTEND_URL}")
if [[ $frontend_response == *"<html"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Frontend not accessible at ${FRONTEND_URL}"
    exit 1
fi

# Test 8: Booking Creation (with auth)
echo -n "8. Booking Creation: "
booking_response=$(curl -s -X POST "${BACKEND_URL}/api/bookings" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${token}" \
    -d "{\"route_id\":\"${route_id}\",\"selected_seats\":[\"1A\"],\"passenger_details\":[{\"firstName\":\"Test\",\"lastName\":\"User\",\"email\":\"${email}\",\"phone\":\"1234567890\"}],\"date\":\"${tomorrow}\"}")

if [[ $booking_response == *"booking_reference"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
    booking_id=$(echo $booking_response | grep -o '"id":"[^"]*' | cut -d'"' -f4)
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $booking_response"
    exit 1
fi

# Test 9: Payment Processing
echo -n "9. Payment Processing: "
payment_response=$(curl -s -X POST "${BACKEND_URL}/api/payments/process" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${token}" \
    -d "{\"booking_id\":\"${booking_id}\",\"payment_method\":\"card\"}")

if [[ $payment_response == *"success"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $payment_response"
    exit 1
fi

# Test 10: View Bookings
echo -n "10. View Bookings: "
bookings_response=$(curl -s -H "Authorization: Bearer ${token}" "${BACKEND_URL}/api/bookings")
if [[ $bookings_response == *"booking_reference"* ]]; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    echo "Response: $bookings_response"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 All Integration Tests Passed!${NC}"
echo ""
echo -e "${BLUE}Configuration Summary:${NC}"
echo "Frontend URL: ${FRONTEND_URL}"
echo "Backend URL: ${BACKEND_URL}"
echo "Test User: ${email}"
echo "Token (first 20 chars): ${token:0:20}..."
echo ""
echo -e "${YELLOW}✅ The BusTicket platform is fully functional!${NC}"
echo -e "${YELLOW}✅ Frontend and Backend are properly integrated!${NC}"
echo -e "${YELLOW}✅ Complete booking flow is working end-to-end!${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Test the complete user journey:"
echo "   - Register/Login"
echo "   - Search for routes"
echo "   - Select seats"
echo "   - Complete booking"
echo "   - View booking history"
echo ""