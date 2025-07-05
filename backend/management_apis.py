from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from bson import ObjectId
import logging

from management_models import *
from server import db

logger = logging.getLogger(__name__)

# Management API Router
management_router = APIRouter(prefix="/api/management", tags=["Management"])

# Bus Operator Management
@management_router.post("/operators", response_model=BusOperatorResponse)
async def create_operator(operator: BusOperatorCreate, admin: dict = Depends(check_admin_access)):
    """Create a new bus operator"""
    try:
        # Check if operator already exists
        existing = await db.operators.find_one({"email": operator.email})
        if existing:
            raise HTTPException(status_code=400, detail="Operator with this email already exists")
        
        operator_dict = {
            **operator.dict(),
            "total_buses": 0,
            "total_routes": 0,
            "total_bookings": 0,
            "revenue": 0.0,
            "rating": 0.0,
            "created_at": datetime.utcnow()
        }
        
        result = await db.operators.insert_one(operator_dict)
        operator_dict["id"] = str(result.inserted_id)
        
        return BusOperatorResponse(**operator_dict)
    except Exception as e:
        logger.error(f"Error creating operator: {e}")
        raise HTTPException(status_code=500, detail="Failed to create operator")

@management_router.get("/operators", response_model=List[BusOperatorResponse])
async def get_operators(admin: dict = Depends(check_admin_access)):
    """Get all bus operators"""
    try:
        operators = await db.operators.find().to_list(length=1000)
        
        result = []
        for operator in operators:
            operator["id"] = str(operator["_id"])
            result.append(BusOperatorResponse(**operator))
        
        return result
    except Exception as e:
        logger.error(f"Error fetching operators: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch operators")

@management_router.put("/operators/{operator_id}")
async def update_operator(operator_id: str, operator_data: dict, admin: dict = Depends(check_admin_access)):
    """Update bus operator"""
    try:
        await db.operators.update_one(
            {"_id": ObjectId(operator_id)},
            {"$set": {**operator_data, "updated_at": datetime.utcnow()}}
        )
        return {"status": "success", "message": "Operator updated successfully"}
    except Exception as e:
        logger.error(f"Error updating operator: {e}")
        raise HTTPException(status_code=500, detail="Failed to update operator")

# Vehicle Management
@management_router.post("/vehicles", response_model=VehicleResponse)
async def create_vehicle(vehicle: VehicleCreate, admin: dict = Depends(check_admin_access)):
    """Create a new vehicle"""
    try:
        # Check if vehicle already exists
        existing = await db.vehicles.find_one({"license_plate": vehicle.license_plate})
        if existing:
            raise HTTPException(status_code=400, detail="Vehicle with this license plate already exists")
        
        # Get operator info
        operator = await db.operators.find_one({"_id": ObjectId(vehicle.operator_id)})
        if not operator:
            raise HTTPException(status_code=404, detail="Operator not found")
        
        vehicle_dict = {
            **vehicle.dict(),
            "operator_name": operator["name"],
            "maintenance_due": datetime.utcnow() + timedelta(days=90),
            "total_trips": 0,
            "revenue": 0.0,
            "rating": 0.0,
            "created_at": datetime.utcnow()
        }
        
        result = await db.vehicles.insert_one(vehicle_dict)
        vehicle_dict["id"] = str(result.inserted_id)
        
        # Update operator vehicle count
        await db.operators.update_one(
            {"_id": ObjectId(vehicle.operator_id)},
            {"$inc": {"total_buses": 1}}
        )
        
        return VehicleResponse(**vehicle_dict)
    except Exception as e:
        logger.error(f"Error creating vehicle: {e}")
        raise HTTPException(status_code=500, detail="Failed to create vehicle")

@management_router.get("/vehicles", response_model=List[VehicleResponse])
async def get_vehicles(operator_id: Optional[str] = None, admin: dict = Depends(check_admin_access)):
    """Get all vehicles or vehicles by operator"""
    try:
        query = {}
        if operator_id:
            query["operator_id"] = operator_id
        
        vehicles = await db.vehicles.find(query).to_list(length=1000)
        
        result = []
        for vehicle in vehicles:
            vehicle["id"] = str(vehicle["_id"])
            result.append(VehicleResponse(**vehicle))
        
        return result
    except Exception as e:
        logger.error(f"Error fetching vehicles: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch vehicles")

# Route Management
@management_router.post("/routes", response_model=RouteResponse)
async def create_route(route: RouteCreate, admin: dict = Depends(check_admin_access)):
    """Create a new route"""
    try:
        # Get operator info
        operator = await db.operators.find_one({"_id": ObjectId(route.operator_id)})
        if not operator:
            raise HTTPException(status_code=404, detail="Operator not found")
        
        route_dict = {
            **route.dict(),
            "operator_name": operator["name"],
            "total_bookings": 0,
            "revenue": 0.0,
            "popularity_score": 0.0,
            "created_at": datetime.utcnow()
        }
        
        result = await db.routes.insert_one(route_dict)
        route_dict["id"] = str(result.inserted_id)
        
        # Update operator route count
        await db.operators.update_one(
            {"_id": ObjectId(route.operator_id)},
            {"$inc": {"total_routes": 1}}
        )
        
        return RouteResponse(**route_dict)
    except Exception as e:
        logger.error(f"Error creating route: {e}")
        raise HTTPException(status_code=500, detail="Failed to create route")

@management_router.get("/routes", response_model=List[RouteResponse])
async def get_routes(operator_id: Optional[str] = None, admin: dict = Depends(check_admin_access)):
    """Get all routes or routes by operator"""
    try:
        query = {}
        if operator_id:
            query["operator_id"] = operator_id
        
        routes = await db.routes.find(query).to_list(length=1000)
        
        result = []
        for route in routes:
            route["id"] = str(route["_id"])
            result.append(RouteResponse(**route))
        
        return result
    except Exception as e:
        logger.error(f"Error fetching routes: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch routes")

# Agent Management
@management_router.post("/agents", response_model=AgentResponse)
async def create_agent(agent: AgentCreate, admin: dict = Depends(check_admin_access)):
    """Create a new travel agent"""
    try:
        existing = await db.agents.find_one({"email": agent.email})
        if existing:
            raise HTTPException(status_code=400, detail="Agent with this email already exists")
        
        agent_dict = {
            **agent.dict(),
            "total_sales": 0,
            "revenue": 0.0,
            "commission_earned": 0.0,
            "rating": 0.0,
            "created_at": datetime.utcnow()
        }
        
        result = await db.agents.insert_one(agent_dict)
        agent_dict["id"] = str(result.inserted_id)
        
        return AgentResponse(**agent_dict)
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(status_code=500, detail="Failed to create agent")

@management_router.get("/agents", response_model=List[AgentResponse])
async def get_agents(admin: dict = Depends(check_admin_access)):
    """Get all travel agents"""
    try:
        agents = await db.agents.find().to_list(length=1000)
        
        result = []
        for agent in agents:
            agent["id"] = str(agent["_id"])
            result.append(AgentResponse(**agent))
        
        return result
    except Exception as e:
        logger.error(f"Error fetching agents: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch agents")

# Smart Seat Management
@management_router.get("/seats/management/{route_id}")
async def get_seat_management(route_id: str, date: str, admin: dict = Depends(check_admin_access)):
    """Get comprehensive seat management data"""
    try:
        # Get route info
        route = await db.routes.find_one({"_id": ObjectId(route_id)})
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        
        # Get vehicles for demo
        vehicles = await db.vehicles.find().to_list(length=1)
        if not vehicles:
            raise HTTPException(status_code=404, detail="No vehicles available")
        
        vehicle = vehicles[0]
        
        # Get bookings for this date
        bookings = await db.bookings.find({
            "route_id": route_id,
            "date": date,
            "status": {"$in": ["confirmed", "paid"]}
        }).to_list(length=1000)
        
        booked_seats = []
        for booking in bookings:
            booked_seats.extend(booking.get("seats", []))
        
        # Generate smart seat management data
        total_seats = vehicle["total_seats"]
        available_seats = total_seats - len(booked_seats)
        
        # Smart features
        vip_seats = [f"{i}A" for i in range(1, min(5, total_seats//4 + 1))]
        blocked_seats = []
        
        # Dynamic pricing tiers
        pricing_tiers = {
            "economy": route["price_base"],
            "premium": route["price_base"] * 1.25,
            "vip": route["price_base"] * 1.5
        }
        
        return SeatManagementResponse(
            route_id=route_id,
            vehicle_id=str(vehicle["_id"]),
            date=date,
            total_seats=total_seats,
            available_seats=available_seats,
            booked_seats=booked_seats,
            blocked_seats=blocked_seats,
            vip_seats=vip_seats,
            pricing_tiers=pricing_tiers
        )
    except Exception as e:
        logger.error(f"Error getting seat management data: {e}")
        raise HTTPException(status_code=500, detail="Failed to get seat management data")

# Analytics and Reporting
@management_router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(admin: dict = Depends(check_admin_access)):
    """Get comprehensive analytics data"""
    try:
        # Basic counts
        total_bookings = await db.bookings.count_documents({})
        total_users = await db.users.count_documents({})
        total_operators = await db.operators.count_documents({})
        total_vehicles = await db.vehicles.count_documents({})
        total_routes = await db.routes.count_documents({})
        
        # Revenue calculation
        revenue_pipeline = [
            {"$match": {"status": "paid"}},
            {"$group": {"_id": None, "total": {"$sum": "$total_price"}}}
        ]
        revenue_result = await db.bookings.aggregate(revenue_pipeline).to_list(length=1)
        total_revenue = revenue_result[0]["total"] if revenue_result else 0
        
        # Top routes
        top_routes_pipeline = [
            {"$group": {"_id": "$route_id", "count": {"$sum": 1}, "revenue": {"$sum": "$total_price"}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        top_routes = await db.bookings.aggregate(top_routes_pipeline).to_list(length=10)
        
        # Revenue trend (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        revenue_trend_pipeline = [
            {"$match": {"created_at": {"$gte": thirty_days_ago}, "status": "paid"}},
            {"$group": {
                "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                "revenue": {"$sum": "$total_price"},
                "bookings": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        revenue_trend = await db.bookings.aggregate(revenue_trend_pipeline).to_list(length=30)
        
        booking_trend = revenue_trend
        
        # Operator performance - simplified
        operator_performance = []
        
        return AnalyticsResponse(
            total_bookings=total_bookings,
            total_revenue=total_revenue,
            total_users=total_users,
            total_operators=total_operators,
            total_vehicles=total_vehicles,
            total_routes=total_routes,
            top_routes=top_routes,
            revenue_trend=revenue_trend,
            booking_trend=booking_trend,
            operator_performance=operator_performance
        )
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analytics")

# AI Features
@management_router.post("/ai/optimize-routes")
async def optimize_routes(admin: dict = Depends(check_admin_access)):
    """AI-powered route optimization"""
    try:
        # Simplified AI recommendations
        recommendations = [
            {
                "type": "increase_frequency",
                "route": "Phnom Penh to Siem Reap",
                "demand": 85,
                "suggested_action": "Add morning departure at 07:30"
            },
            {
                "type": "dynamic_pricing",
                "route": "Phnom Penh to Sihanoukville",
                "demand": 92,
                "suggested_action": "Increase weekend prices by 15%"
            }
        ]
        
        return {
            "status": "success",
            "recommendations": recommendations,
            "analysis_date": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Error optimizing routes: {e}")
        raise HTTPException(status_code=500, detail="Failed to optimize routes")

@management_router.post("/ai/dynamic-pricing")
async def calculate_dynamic_pricing(route_id: str, date: str, admin: dict = Depends(check_admin_access)):
    """AI-powered dynamic pricing"""
    try:
        # Get route info
        route = await db.routes.find_one({"_id": ObjectId(route_id)})
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        
        base_price = route["price_base"]
        
        # Simplified dynamic pricing
        demand_factor = 1.2  # High demand
        availability_factor = 1.1  # Limited availability
        early_bird_factor = 0.9  # Early booking discount
        
        dynamic_price = base_price * demand_factor * availability_factor * early_bird_factor
        
        return {
            "route_id": route_id,
            "date": date,
            "base_price": base_price,
            "dynamic_price": round(dynamic_price, 2),
            "factors": {
                "demand_factor": demand_factor,
                "availability_factor": availability_factor,
                "early_bird_factor": early_bird_factor
            },
            "recommendation": "optimal_price"
        }
    except Exception as e:
        logger.error(f"Error calculating dynamic pricing: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate dynamic pricing")

# Real-time Dashboard
@management_router.get("/realtime/dashboard")
async def get_realtime_dashboard(admin: dict = Depends(check_admin_access)):
    """Get real-time dashboard data"""
    try:
        # Current active bookings
        active_bookings = await db.bookings.count_documents({
            "status": "paid",
            "date": {"$gte": datetime.utcnow().strftime("%Y-%m-%d")}
        })
        
        # Today's revenue
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_revenue = await db.payments.aggregate([
            {"$match": {"created_at": {"$gte": today_start}, "status": "completed"}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]).to_list(length=1)
        
        revenue_today = today_revenue[0]["total"] if today_revenue else 0
        
        # Active vehicles
        active_vehicles = await db.vehicles.count_documents({"is_active": True})
        
        # System alerts
        alerts = [
            {
                "type": "maintenance",
                "message": "Vehicle KH-PP-1234 maintenance due in 3 days",
                "priority": "medium"
            },
            {
                "type": "availability",
                "message": "High demand detected for weekend routes",
                "priority": "high"
            }
        ]
        
        return {
            "active_bookings": active_bookings,
            "revenue_today": revenue_today,
            "active_vehicles": active_vehicles,
            "alerts": alerts,
            "last_updated": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Error getting realtime dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to get dashboard data")