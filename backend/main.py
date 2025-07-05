from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from datetime import datetime, timedelta
from typing import Optional, List
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from bson import ObjectId
from pymongo import MongoClient
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(MONGO_URL)
db = client.busticket_db

# Security
security = HTTPBearer()

# Pydantic Models
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_active: bool = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SearchRequest(BaseModel):
    origin: str
    destination: str
    date: str
    passengers: int = 1
    transport_type: str = "bus"

class RouteResponse(BaseModel):
    id: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
    vehicle_type: str
    company: str
    amenities: List[str]
    available_seats: int
    total_seats: int

class SeatSelection(BaseModel):
    seat_number: str
    seat_type: str
    price: float
    is_available: bool

class BookingRequest(BaseModel):
    route_id: str
    selected_seats: List[str]
    passenger_details: List[dict]
    date: str

class BookingResponse(BaseModel):
    id: str
    booking_reference: str
    route_id: str
    seats: List[str]
    total_price: float
    status: str
    created_at: datetime

class PaymentRequest(BaseModel):
    booking_id: str
    payment_method: str
    card_details: Optional[dict] = None

# Helper Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"email": username})
    if user is None:
        raise credentials_exception
    return user

# Startup event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database collections and indexes
    await init_database()
    yield
    # Cleanup
    pass

async def init_database():
    """Initialize database with sample data"""
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.bookings.create_index("booking_reference", unique=True)
    await db.routes.create_index([("origin", 1), ("destination", 1)])
    
    # Insert sample data if collections are empty
    if await db.routes.count_documents({}) == 0:
        await insert_sample_routes()
    if await db.vehicles.count_documents({}) == 0:
        await insert_sample_vehicles()

async def insert_sample_routes():
    """Insert sample routes and schedules"""
    sample_routes = [
        {
            "origin": "Phnom Penh",
            "destination": "Siem Reap",
            "distance": 314,
            "duration": "5h 45m",
            "transport_type": "bus",
            "price_base": 15.0,
            "created_at": datetime.utcnow()
        },
        {
            "origin": "Phnom Penh",
            "destination": "Sihanoukville",
            "distance": 230,
            "duration": "4h 30m",
            "transport_type": "bus",
            "price_base": 12.0,
            "created_at": datetime.utcnow()
        },
        {
            "origin": "Phnom Penh",
            "destination": "Kampot",
            "distance": 148,
            "duration": "3h 15m",
            "transport_type": "bus",
            "price_base": 8.0,
            "created_at": datetime.utcnow()
        },
        {
            "origin": "Siem Reap",
            "destination": "Phnom Penh",
            "distance": 314,
            "duration": "5h 45m",
            "transport_type": "bus",
            "price_base": 15.0,
            "created_at": datetime.utcnow()
        },
        {
            "origin": "Sihanoukville",
            "destination": "Koh Rong",
            "distance": 25,
            "duration": "45m",
            "transport_type": "ferry",
            "price_base": 25.0,
            "created_at": datetime.utcnow()
        }
    ]
    
    await db.routes.insert_many(sample_routes)
    logger.info("Sample routes inserted")

async def insert_sample_vehicles():
    """Insert sample vehicles"""
    sample_vehicles = [
        {
            "company": "Mekong Express",
            "vehicle_type": "VIP Bus",
            "seat_layout": "2-2",
            "total_seats": 44,
            "amenities": ["WiFi", "AC", "USB Charging", "Blanket", "Water"],
            "rating": 4.8,
            "created_at": datetime.utcnow()
        },
        {
            "company": "Giant Ibis",
            "vehicle_type": "Sleeper Bus",
            "seat_layout": "2-1",
            "total_seats": 36,
            "amenities": ["WiFi", "AC", "Reclining Seats", "Meals", "Entertainment"],
            "rating": 4.6,
            "created_at": datetime.utcnow()
        },
        {
            "company": "Virak Buntham",
            "vehicle_type": "Standard Bus",
            "seat_layout": "2-2",
            "total_seats": 45,
            "amenities": ["AC", "Water"],
            "rating": 4.2,
            "created_at": datetime.utcnow()
        }
    ]
    
    await db.vehicles.insert_many(sample_vehicles)
    logger.info("Sample vehicles inserted")

# Initialize FastAPI app
app = FastAPI(
    title="BusTicket API",
    description="Enhanced Bus Booking Platform API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/")
async def health_check():
    return {"message": "BusTicket API is running!", "timestamp": datetime.utcnow()}

# Authentication endpoints
@app.post("/api/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    user_dict = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    
    return UserResponse(**user_dict)

@app.post("/api/auth/login", response_model=Token)
async def login(user: UserLogin):
    # Find user
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["email"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user["_id"]),
        email=current_user["email"],
        first_name=current_user["first_name"],
        last_name=current_user["last_name"],
        phone=current_user.get("phone"),
        created_at=current_user["created_at"],
        is_active=current_user["is_active"]
    )

# Search endpoints
@app.post("/api/search", response_model=List[RouteResponse])
async def search_routes(search: SearchRequest):
    """Search for available routes"""
    # Find matching routes
    routes = await db.routes.find({
        "origin": {"$regex": search.origin, "$options": "i"},
        "destination": {"$regex": search.destination, "$options": "i"},
        "transport_type": search.transport_type
    }).to_list(length=100)
    
    results = []
    for route in routes:
        # Get available schedules for the date
        schedules = await generate_schedules_for_route(route, search.date)
        
        for schedule in schedules:
            vehicle = await db.vehicles.find_one({"_id": schedule["vehicle_id"]})
            if vehicle:
                # Calculate available seats
                bookings = await db.bookings.find({
                    "route_id": str(route["_id"]),
                    "date": search.date,
                    "status": {"$in": ["confirmed", "paid"]}
                }).to_list(length=1000)
                
                booked_seats = []
                for booking in bookings:
                    booked_seats.extend(booking.get("seats", []))
                
                available_seats = vehicle["total_seats"] - len(booked_seats)
                
                results.append(RouteResponse(
                    id=str(route["_id"]) + "-" + str(schedule["schedule_id"]),
                    origin=route["origin"],
                    destination=route["destination"],
                    departure_time=schedule["departure_time"],
                    arrival_time=schedule["arrival_time"],
                    duration=route["duration"],
                    price=route["price_base"],
                    vehicle_type=vehicle["vehicle_type"],
                    company=vehicle["company"],
                    amenities=vehicle["amenities"],
                    available_seats=available_seats,
                    total_seats=vehicle["total_seats"]
                ))
    
    return results

async def generate_schedules_for_route(route, date):
    """Generate schedules for a route on a given date"""
    # Sample schedule generation
    base_times = [
        {"departure": "06:00", "arrival": "11:45"},
        {"departure": "08:30", "arrival": "14:15"},
        {"departure": "13:00", "arrival": "18:45"},
        {"departure": "15:30", "arrival": "21:15"},
        {"departure": "20:00", "arrival": "01:45+1"}
    ]
    
    vehicles = await db.vehicles.find().to_list(length=10)
    schedules = []
    
    for i, time_slot in enumerate(base_times[:3]):  # Limit to 3 schedules per route
        if i < len(vehicles):
            schedules.append({
                "schedule_id": i + 1,
                "vehicle_id": vehicles[i]["_id"],
                "departure_time": time_slot["departure"],
                "arrival_time": time_slot["arrival"],
                "date": date
            })
    
    return schedules

# Seat selection endpoints
@app.get("/api/seats/{route_schedule_id}")
async def get_seat_layout(route_schedule_id: str, date: str):
    """Get seat layout and availability"""
    # Parse route_schedule_id
    parts = route_schedule_id.split("-")
    if len(parts) < 2:
        raise HTTPException(status_code=400, detail="Invalid route schedule ID")
    
    route_id = parts[0]
    schedule_id = parts[1]
    
    # Get route and vehicle info
    route = await db.routes.find_one({"_id": ObjectId(route_id)})
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Get vehicle for this schedule (simplified)
    vehicles = await db.vehicles.find().to_list(length=10)
    if not vehicles:
        raise HTTPException(status_code=404, detail="No vehicles available")
    
    vehicle = vehicles[0]  # Simplified selection
    
    # Get booked seats
    bookings = await db.bookings.find({
        "route_schedule_id": route_schedule_id,
        "date": date,
        "status": {"$in": ["confirmed", "paid"]}
    }).to_list(length=1000)
    
    booked_seats = []
    for booking in bookings:
        booked_seats.extend(booking.get("seats", []))
    
    # Generate seat layout
    seat_layout = generate_seat_layout(vehicle, booked_seats)
    
    return {
        "route_id": route_id,
        "schedule_id": schedule_id,
        "vehicle_info": {
            "company": vehicle["company"],
            "vehicle_type": vehicle["vehicle_type"],
            "total_seats": vehicle["total_seats"],
            "amenities": vehicle["amenities"]
        },
        "seat_layout": seat_layout,
        "booked_seats": booked_seats
    }

def generate_seat_layout(vehicle, booked_seats):
    """Generate seat layout based on vehicle configuration"""
    total_seats = vehicle["total_seats"]
    seat_layout = vehicle["seat_layout"]  # e.g., "2-2"
    
    seats = []
    seat_number = 1
    
    # Simple 2-2 layout generation
    for row in range(1, (total_seats // 4) + 2):
        for position in ["A", "B", "C", "D"]:
            if seat_number <= total_seats:
                seat_id = f"{row}{position}"
                seat_type = "window" if position in ["A", "D"] else "aisle"
                price_modifier = 1.0 if seat_type == "window" else 0.95
                
                seats.append({
                    "seat_id": seat_id,
                    "seat_number": seat_number,
                    "seat_type": seat_type,
                    "is_available": seat_id not in booked_seats,
                    "price_modifier": price_modifier,
                    "row": row,
                    "position": position
                })
                seat_number += 1
    
    return seats

# Booking endpoints
@app.post("/api/bookings", response_model=BookingResponse)
async def create_booking(booking: BookingRequest, current_user: dict = Depends(get_current_user)):
    """Create a new booking"""
    # Generate booking reference
    booking_ref = f"BT{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    # Check seat availability
    existing_bookings = await db.bookings.find({
        "route_id": booking.route_id,
        "date": booking.date,
        "status": {"$in": ["confirmed", "paid"]},
        "seats": {"$in": booking.selected_seats}
    }).to_list(length=1000)
    
    if existing_bookings:
        raise HTTPException(status_code=400, detail="Some seats are already booked")
    
    # Get route price
    route_parts = booking.route_id.split("-")
    route = await db.routes.find_one({"_id": ObjectId(route_parts[0])})
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    total_price = route["price_base"] * len(booking.selected_seats)
    
    # Create booking
    booking_dict = {
        "booking_reference": booking_ref,
        "user_id": str(current_user["_id"]),
        "route_id": booking.route_id,
        "route_schedule_id": booking.route_id,
        "seats": booking.selected_seats,
        "passenger_details": booking.passenger_details,
        "date": booking.date,
        "total_price": total_price,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    result = await db.bookings.insert_one(booking_dict)
    booking_dict["id"] = str(result.inserted_id)
    
    return BookingResponse(**booking_dict)

@app.get("/api/bookings")
async def get_user_bookings(current_user: dict = Depends(get_current_user)):
    """Get user's bookings"""
    bookings = await db.bookings.find({
        "user_id": str(current_user["_id"])
    }).sort("created_at", -1).to_list(length=100)
    
    for booking in bookings:
        booking["id"] = str(booking["_id"])
        # Get route details
        route_parts = booking["route_id"].split("-")
        route = await db.routes.find_one({"_id": ObjectId(route_parts[0])})
        if route:
            booking["route_details"] = {
                "origin": route["origin"],
                "destination": route["destination"],
                "duration": route["duration"]
            }
    
    return bookings

@app.get("/api/bookings/{booking_id}")
async def get_booking_details(booking_id: str, current_user: dict = Depends(get_current_user)):
    """Get booking details"""
    booking = await db.bookings.find_one({
        "_id": ObjectId(booking_id),
        "user_id": str(current_user["_id"])
    })
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking["id"] = str(booking["_id"])
    
    # Get route details
    route_parts = booking["route_id"].split("-")
    route = await db.routes.find_one({"_id": ObjectId(route_parts[0])})
    if route:
        booking["route_details"] = {
            "origin": route["origin"],
            "destination": route["destination"],
            "duration": route["duration"]
        }
    
    return booking

# Payment endpoints
@app.post("/api/payments/process")
async def process_payment(payment: PaymentRequest, current_user: dict = Depends(get_current_user)):
    """Process payment for booking"""
    # Get booking
    booking = await db.bookings.find_one({
        "_id": ObjectId(payment.booking_id),
        "user_id": str(current_user["_id"])
    })
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking["status"] != "pending":
        raise HTTPException(status_code=400, detail="Booking is not pending payment")
    
    # Simulate payment processing
    payment_successful = True  # In real implementation, integrate with payment gateway
    
    if payment_successful:
        # Update booking status
        await db.bookings.update_one(
            {"_id": ObjectId(payment.booking_id)},
            {
                "$set": {
                    "status": "paid",
                    "payment_method": payment.payment_method,
                    "paid_at": datetime.utcnow()
                }
            }
        )
        
        # Create payment record
        payment_record = {
            "booking_id": payment.booking_id,
            "user_id": str(current_user["_id"]),
            "amount": booking["total_price"],
            "payment_method": payment.payment_method,
            "status": "completed",
            "transaction_id": f"TXN{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "created_at": datetime.utcnow()
        }
        
        await db.payments.insert_one(payment_record)
        
        return {
            "status": "success",
            "message": "Payment processed successfully",
            "booking_id": payment.booking_id,
            "transaction_id": payment_record["transaction_id"]
        }
    else:
        return {
            "status": "failed",
            "message": "Payment processing failed"
        }

# Admin endpoints
@app.get("/api/admin/stats")
async def get_admin_stats(current_user: dict = Depends(get_current_user)):
    """Get admin statistics"""
    total_bookings = await db.bookings.count_documents({})
    total_users = await db.users.count_documents({})
    total_revenue = await db.payments.aggregate([
        {"$match": {"status": "completed"}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]).to_list(length=1)
    
    revenue = total_revenue[0]["total"] if total_revenue else 0
    
    return {
        "total_bookings": total_bookings,
        "total_users": total_users,
        "total_revenue": revenue,
        "generated_at": datetime.utcnow()
    }

# Popular destinations endpoint
@app.get("/api/destinations/popular")
async def get_popular_destinations():
    """Get popular destinations"""
    destinations = await db.routes.aggregate([
        {"$group": {
            "_id": "$destination", 
            "count": {"$sum": 1},
            "avg_price": {"$avg": "$price_base"}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]).to_list(length=10)
    
    return destinations

# Route suggestions endpoint
@app.get("/api/suggestions")
async def get_route_suggestions(q: str = ""):
    """Get route suggestions for autocomplete"""
    if not q:
        return []
    
    # Get origins and destinations matching query
    origins = await db.routes.find({
        "origin": {"$regex": q, "$options": "i"}
    }).distinct("origin")
    
    destinations = await db.routes.find({
        "destination": {"$regex": q, "$options": "i"}
    }).distinct("destination")
    
    # Combine and deduplicate
    suggestions = list(set(origins + destinations))
    return suggestions[:10]

# User Profile endpoints
@app.get("/api/user/credit")
async def get_user_credit(current_user: dict = Depends(get_current_user)):
    """Get user credit balance and transactions"""
    # Sample credit data - in real app, this would come from database
    credit_data = {
        "balance": 25.50,
        "transactions": [
            {"description": "Booking Credit Refund", "amount": 15.00, "date": "2025-07-03"},
            {"description": "Referral Bonus", "amount": 10.00, "date": "2025-07-01"},
            {"description": "Welcome Bonus", "amount": 5.00, "date": "2025-06-25"},
            {"description": "Booking Payment", "amount": -4.50, "date": "2025-06-20"}
        ]
    }
    return credit_data

@app.get("/api/bookings/upcoming")
async def get_upcoming_bookings(current_user: dict = Depends(get_current_user)):
    """Get user's upcoming bookings"""
    from datetime import datetime
    today = datetime.utcnow()
    
    bookings = await db.bookings.find({
        "user_id": str(current_user["_id"]),
        "date": {"$gte": today.strftime("%Y-%m-%d")},
        "status": {"$in": ["confirmed", "paid"]}
    }).sort("date", 1).to_list(length=50)
    
    for booking in bookings:
        booking["id"] = str(booking["_id"])
        # Get route details
        route_parts = booking["route_id"].split("-")
        route = await db.routes.find_one({"_id": ObjectId(route_parts[0])})
        if route:
            booking["route_details"] = {
                "origin": route["origin"],
                "destination": route["destination"],
                "duration": route["duration"]
            }
    
    return bookings

@app.get("/api/bookings/past")
async def get_past_bookings(current_user: dict = Depends(get_current_user)):
    """Get user's past bookings"""
    from datetime import datetime
    today = datetime.utcnow()
    
    bookings = await db.bookings.find({
        "user_id": str(current_user["_id"]),
        "date": {"$lt": today.strftime("%Y-%m-%d")}
    }).sort("date", -1).to_list(length=50)
    
    for booking in bookings:
        booking["id"] = str(booking["_id"])
        # Get route details
        route_parts = booking["route_id"].split("-")
        route = await db.routes.find_one({"_id": ObjectId(route_parts[0])})
        if route:
            booking["route_details"] = {
                "origin": route["origin"],
                "destination": route["destination"],
                "duration": route["duration"]
            }
    
    return bookings

@app.post("/api/user/invite")
async def send_invite(invite_data: dict, current_user: dict = Depends(get_current_user)):
    """Send invitation to friends"""
    # In real implementation, this would send actual emails
    invite_record = {
        "inviter_id": str(current_user["_id"]),
        "email": invite_data["email"],
        "invite_code": invite_data["invite_code"],
        "status": "sent",
        "created_at": datetime.utcnow()
    }
    
    await db.invites.insert_one(invite_record)
    return {"message": "Invite sent successfully"}

@app.put("/api/user/profile")
async def update_user_profile(profile_data: dict, current_user: dict = Depends(get_current_user)):
    """Update user profile"""
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {
            "first_name": profile_data["first_name"],
            "last_name": profile_data["last_name"],
            "email": profile_data["email"],
            "phone": profile_data["phone"],
            "updated_at": datetime.utcnow()
        }}
    )
    return {"message": "Profile updated successfully"}

@app.put("/api/user/change-password")
async def change_password(password_data: dict, current_user: dict = Depends(get_current_user)):
    """Change user password"""
    if not verify_password(password_data["current_password"], current_user["password"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    new_password_hash = get_password_hash(password_data["new_password"])
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$set": {
            "password": new_password_hash,
            "updated_at": datetime.utcnow()
        }}
    )
    return {"message": "Password changed successfully"}

# Affiliate Program endpoints
@app.get("/api/affiliate/status")
async def get_affiliate_status(current_user: dict = Depends(get_current_user)):
    """Check if user is an affiliate"""
    affiliate = await db.affiliates.find_one({"user_id": str(current_user["_id"])})
    
    if affiliate:
        return {
            "isAffiliate": True,
            "affiliateData": {
                "affiliateCode": affiliate["affiliate_code"],
                "status": affiliate["status"],
                "createdAt": affiliate["created_at"]
            }
        }
    else:
        return {"isAffiliate": False, "affiliateData": None}

@app.post("/api/affiliate/register")
async def register_affiliate(affiliate_data: dict, current_user: dict = Depends(get_current_user)):
    """Register as affiliate"""
    # Generate unique affiliate code
    affiliate_code = f"BMB{str(current_user['_id'])[-6:].upper()}"
    
    affiliate_record = {
        "user_id": str(current_user["_id"]),
        "affiliate_code": affiliate_code,
        "company_name": affiliate_data["companyName"],
        "website": affiliate_data["website"],
        "description": affiliate_data["description"],
        "monthly_sales": affiliate_data["monthlySales"],
        "marketing_channels": affiliate_data["marketingChannels"],
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    await db.affiliates.insert_one(affiliate_record)
    
    return {
        "affiliateCode": affiliate_code,
        "status": "pending",
        "message": "Affiliate application submitted successfully"
    }

@app.get("/api/affiliate/stats")
async def get_affiliate_stats(current_user: dict = Depends(get_current_user)):
    """Get affiliate statistics"""
    # Sample stats - in real app, this would be calculated from actual data
    stats = {
        "totalEarnings": 1250.75,
        "totalReferrals": 42,
        "conversionRate": 3.2,
        "monthlyEarnings": 285.50
    }
    return stats

@app.get("/api/affiliate/activity")
async def get_affiliate_activity(current_user: dict = Depends(get_current_user)):
    """Get recent affiliate activity"""
    # Sample activity data
    activity = [
        {"description": "New booking commission", "commission": 15.50, "date": "2025-07-04"},
        {"description": "Referral signup bonus", "commission": 10.00, "date": "2025-07-03"},
        {"description": "Booking commission", "commission": 8.25, "date": "2025-07-02"}
    ]
    return activity

# Ticket Management endpoints
@app.get("/api/tickets/download/{booking_id}")
async def download_ticket(booking_id: str, current_user: dict = Depends(get_current_user)):
    """Download ticket as PDF"""
    booking = await db.bookings.find_one({
        "_id": ObjectId(booking_id),
        "user_id": str(current_user["_id"])
    })
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # In real implementation, this would generate a PDF
    # For now, return a placeholder response
    return {"message": "PDF download would be generated here", "booking_id": booking_id}

@app.post("/api/tickets/send")
async def send_ticket(send_data: dict, current_user: dict = Depends(get_current_user)):
    """Send ticket via email or SMS"""
    booking = await db.bookings.find_one({
        "_id": ObjectId(send_data["booking_id"]),
        "user_id": str(current_user["_id"])
    })
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # In real implementation, this would send actual emails/SMS
    send_record = {
        "booking_id": send_data["booking_id"],
        "recipients": send_data["recipients"],
        "method": send_data["method"],
        "message": send_data.get("message", ""),
        "sent_at": datetime.utcnow(),
        "sent_by": str(current_user["_id"])
    }
    
    await db.ticket_sends.insert_one(send_record)
    return {"message": "Ticket sent successfully"}

# Enhanced search for different transport types
@app.post("/api/search/{transport_type}")
async def search_by_transport_type(transport_type: str, search: SearchRequest):
    """Search for specific transport type"""
    search.transport_type = transport_type
    return await search_routes(search)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)