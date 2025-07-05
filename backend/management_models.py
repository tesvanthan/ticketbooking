from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId
import logging

# Import from main.py
from server import db, get_current_user

logger = logging.getLogger(__name__)

# Management API Router
management_router = APIRouter(prefix="/api/management", tags=["Management"])

# Pydantic Models for Management

class BusOperatorCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str
    license_number: str
    commission_rate: float = 0.10
    is_active: bool = True

class BusOperatorResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    address: str
    license_number: str
    commission_rate: float
    is_active: bool
    total_buses: int
    total_routes: int
    total_bookings: int
    revenue: float
    rating: float
    created_at: datetime

class VehicleCreate(BaseModel):
    operator_id: str
    license_plate: str
    vehicle_type: str
    brand: str
    model: str
    year: int
    total_seats: int
    seat_layout: str
    amenities: List[str]
    fuel_type: str
    max_speed: int
    is_active: bool = True

class VehicleResponse(BaseModel):
    id: str
    operator_id: str
    operator_name: str
    license_plate: str
    vehicle_type: str
    brand: str
    model: str
    year: int
    total_seats: int
    seat_layout: str
    amenities: List[str]
    fuel_type: str
    max_speed: int
    is_active: bool
    maintenance_due: Optional[datetime]
    total_trips: int
    revenue: float
    rating: float
    created_at: datetime

class RouteCreate(BaseModel):
    origin: str
    destination: str
    distance: float
    duration: str
    transport_type: str
    price_base: float
    operator_id: str
    stops: List[Dict[str, Any]] = []
    is_active: bool = True

class RouteResponse(BaseModel):
    id: str
    origin: str
    destination: str
    distance: float
    duration: str
    transport_type: str
    price_base: float
    operator_id: str
    operator_name: str
    stops: List[Dict[str, Any]]
    is_active: bool
    total_bookings: int
    revenue: float
    popularity_score: float
    created_at: datetime

class AgentCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    location: str
    commission_rate: float = 0.05
    is_active: bool = True

class AgentResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    location: str
    commission_rate: float
    is_active: bool
    total_sales: int
    revenue: float
    commission_earned: float
    rating: float
    created_at: datetime

class ScheduleCreate(BaseModel):
    route_id: str
    vehicle_id: str
    departure_time: str
    arrival_time: str
    days_of_week: List[int]  # 0=Monday, 6=Sunday
    price_multiplier: float = 1.0
    is_active: bool = True

class SeatManagementResponse(BaseModel):
    route_id: str
    vehicle_id: str
    date: str
    total_seats: int
    available_seats: int
    booked_seats: List[str]
    blocked_seats: List[str]
    vip_seats: List[str]
    pricing_tiers: Dict[str, float]

class AnalyticsResponse(BaseModel):
    total_bookings: int
    total_revenue: float
    total_users: int
    total_operators: int
    total_vehicles: int
    total_routes: int
    top_routes: List[Dict[str, Any]]
    revenue_trend: List[Dict[str, Any]]
    booking_trend: List[Dict[str, Any]]
    operator_performance: List[Dict[str, Any]]

# Helper function to check admin access
async def check_admin_access(current_user: dict = Depends(get_current_user)):
    """Check if user has admin access"""
    # For now, we'll assume all logged-in users are admins
    # In production, you'd check user roles
    if not current_user:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user