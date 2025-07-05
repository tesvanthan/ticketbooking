import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Plane, 
  Car, 
  Ship, 
  Bus, 
  Plus, 
  Edit2, 
  Trash2, 
  Eye, 
  Settings, 
  Users, 
  MapPin, 
  Clock, 
  DollarSign, 
  Calendar, 
  Star, 
  AlertCircle, 
  CheckCircle, 
  Search, 
  Filter, 
  Download, 
  Upload, 
  BarChart3,
  Navigation,
  Route,
  Square,
  Shield,
  Bell,
  Smartphone,
  Mail,
  Globe,
  RefreshCw,
  Save,
  X,
  ArrowRight,
  Target,
  TrendingUp,
  Activity,
  Zap
} from 'lucide-react';
import { useAuth } from './components';

// Route Management Component
export const RouteManagement = () => {
  const [routes, setRoutes] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingRoute, setEditingRoute] = useState(null);
  const [routeForm, setRouteForm] = useState({
    origin: '',
    destination: '',
    distance: '',
    duration: '',
    price: '',
    transport_type: 'bus',
    schedule: [],
    status: 'active'
  });
  const [scheduleForm, setScheduleForm] = useState({
    departure_time: '',
    arrival_time: '',
    days: []
  });
  const { token } = useAuth();

  useEffect(() => {
    fetchRoutes();
  }, []);

  const fetchRoutes = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/routes`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setRoutes(data);
      }
    } catch (error) {
      console.error('Error fetching routes:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const method = editingRoute ? 'PUT' : 'POST';
      const url = editingRoute 
        ? `${process.env.REACT_APP_BACKEND_URL}/api/admin/routes/${editingRoute.id}`
        : `${process.env.REACT_APP_BACKEND_URL}/api/admin/routes`;

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(routeForm)
      });

      if (response.ok) {
        alert(`Route ${editingRoute ? 'updated' : 'created'} successfully!`);
        setShowForm(false);
        setEditingRoute(null);
        fetchRoutes();
      }
    } catch (error) {
      alert('Failed to save route');
    }
  };

  const addSchedule = () => {
    if (scheduleForm.departure_time && scheduleForm.arrival_time) {
      setRouteForm(prev => ({
        ...prev,
        schedule: [...prev.schedule, scheduleForm]
      }));
      setScheduleForm({ departure_time: '', arrival_time: '', days: [] });
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Route Management</h2>
        <div className="flex space-x-2">
          <button 
            onClick={() => setShowForm(true)}
            className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 flex items-center"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Route
          </button>
          <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 flex items-center">
            <Upload className="w-4 h-4 mr-2" />
            Bulk Import
          </button>
        </div>
      </div>

      {/* Routes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {routes.map((route) => (
          <motion.div
            key={route.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold">{route.origin} → {route.destination}</h3>
                <p className="text-gray-600">{route.transport_type.toUpperCase()}</p>
              </div>
              <div className="flex space-x-1">
                <button className="text-blue-600 hover:text-blue-800">
                  <Edit2 className="w-4 h-4" />
                </button>
                <button className="text-red-600 hover:text-red-800">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Distance:</span>
                <span className="font-medium">{route.distance}</span>
              </div>
              <div className="flex justify-between">
                <span>Duration:</span>
                <span className="font-medium">{route.duration}</span>
              </div>
              <div className="flex justify-between">
                <span>Price:</span>
                <span className="font-medium text-green-600">${route.price}</span>
              </div>
              <div className="flex justify-between">
                <span>Status:</span>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  route.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {route.status}
                </span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Add/Edit Route Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-xl font-bold mb-4">
              {editingRoute ? 'Edit Route' : 'Add New Route'}
            </h3>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Origin</label>
                  <input
                    type="text"
                    value={routeForm.origin}
                    onChange={(e) => setRouteForm({...routeForm, origin: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Destination</label>
                  <input
                    type="text"
                    value={routeForm.destination}
                    onChange={(e) => setRouteForm({...routeForm, destination: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Distance</label>
                  <input
                    type="text"
                    value={routeForm.distance}
                    onChange={(e) => setRouteForm({...routeForm, distance: e.target.value})}
                    placeholder="e.g., 315 km"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Duration</label>
                  <input
                    type="text"
                    value={routeForm.duration}
                    onChange={(e) => setRouteForm({...routeForm, duration: e.target.value})}
                    placeholder="e.g., 5h 45m"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Price (USD)</label>
                  <input
                    type="number"
                    value={routeForm.price}
                    onChange={(e) => setRouteForm({...routeForm, price: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Transport Type</label>
                  <select
                    value={routeForm.transport_type}
                    onChange={(e) => setRouteForm({...routeForm, transport_type: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="bus">Bus</option>
                    <option value="ferry">Ferry</option>
                    <option value="flight">Flight</option>
                    <option value="taxi">Taxi</option>
                  </select>
                </div>
              </div>

              {/* Schedule Section */}
              <div className="border-t pt-4">
                <h4 className="font-semibold mb-3">Schedule</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Departure Time</label>
                    <input
                      type="time"
                      value={scheduleForm.departure_time}
                      onChange={(e) => setScheduleForm({...scheduleForm, departure_time: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Arrival Time</label>
                    <input
                      type="time"
                      value={scheduleForm.arrival_time}
                      onChange={(e) => setScheduleForm({...scheduleForm, arrival_time: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div className="flex items-end">
                    <button
                      type="button"
                      onClick={addSchedule}
                      className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600"
                    >
                      Add Schedule
                    </button>
                  </div>
                </div>

                {/* Schedule List */}
                {routeForm.schedule.length > 0 && (
                  <div className="space-y-2">
                    {routeForm.schedule.map((schedule, index) => (
                      <div key={index} className="flex justify-between items-center bg-gray-50 p-3 rounded">
                        <span>{schedule.departure_time} - {schedule.arrival_time}</span>
                        <button
                          type="button"
                          onClick={() => setRouteForm(prev => ({
                            ...prev,
                            schedule: prev.schedule.filter((_, i) => i !== index)
                          }))}
                          className="text-red-600 hover:text-red-800"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex justify-end space-x-2 pt-4">
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                >
                  {editingRoute ? 'Update' : 'Create'} Route
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// Agent Management Component
export const AgentManagement = () => {
  const [agents, setAgents] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingAgent, setEditingAgent] = useState(null);
  const [agentForm, setAgentForm] = useState({
    name: '',
    email: '',
    phone: '',
    location: '',
    commission_rate: '',
    territories: [],
    status: 'active',
    documents: []
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Agent Management</h2>
        <button 
          onClick={() => setShowForm(true)}
          className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 flex items-center"
        >
          <Plus className="w-4 h-4 mr-2" />
          Add Agent
        </button>
      </div>

      {/* Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <motion.div
            key={agent.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <Users className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold">{agent.name}</h3>
                  <p className="text-gray-600">{agent.location}</p>
                </div>
              </div>
              <div className="flex space-x-1">
                <button className="text-blue-600 hover:text-blue-800">
                  <Edit2 className="w-4 h-4" />
                </button>
                <button className="text-red-600 hover:text-red-800">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <div className="space-y-2 text-sm">
              <div><strong>Email:</strong> {agent.email}</div>
              <div><strong>Phone:</strong> {agent.phone}</div>
              <div><strong>Commission:</strong> {agent.commission_rate}%</div>
              <div>
                <strong>Status:</strong>
                <span className={`ml-2 px-2 py-1 rounded-full text-xs ${
                  agent.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {agent.status}
                </span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

// Smart Seat Management Component
export const SmartSeatManagement = () => {
  const [seatLayouts, setSeatLayouts] = useState([]);
  const [showDesigner, setShowDesigner] = useState(false);
  const [currentLayout, setCurrentLayout] = useState({
    name: '',
    vehicle_type: '',
    rows: 12,
    cols: 4,
    seats: []
  });

  const SeatDesigner = () => {
    const [selectedSeat, setSelectedSeat] = useState(null);

    const generateSeatLayout = () => {
      const seats = [];
      for (let row = 1; row <= currentLayout.rows; row++) {
        for (let col = 1; col <= currentLayout.cols; col++) {
          if (col === 2) continue; // Aisle
          seats.push({
            id: `${row}${String.fromCharCode(64 + col)}`,
            row,
            col,
            type: 'standard',
            status: 'available',
            price_modifier: 0
          });
        }
      }
      setCurrentLayout(prev => ({ ...prev, seats }));
    };

    return (
      <div className="bg-white rounded-lg p-6">
        <h3 className="text-xl font-bold mb-4">Smart Seat Designer</h3>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Controls */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Layout Name</label>
              <input
                type="text"
                value={currentLayout.name}
                onChange={(e) => setCurrentLayout({...currentLayout, name: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Vehicle Type</label>
              <select
                value={currentLayout.vehicle_type}
                onChange={(e) => setCurrentLayout({...currentLayout, vehicle_type: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select Type</option>
                <option value="standard_bus">Standard Bus</option>
                <option value="vip_bus">VIP Bus</option>
                <option value="sleeper_bus">Sleeper Bus</option>
                <option value="mini_van">Mini Van</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Rows</label>
                <input
                  type="number"
                  value={currentLayout.rows}
                  onChange={(e) => setCurrentLayout({...currentLayout, rows: parseInt(e.target.value)})}
                  min="5"
                  max="20"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Columns</label>
                <input
                  type="number"
                  value={currentLayout.cols}
                  onChange={(e) => setCurrentLayout({...currentLayout, cols: parseInt(e.target.value)})}
                  min="3"
                  max="6"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            <button
              onClick={generateSeatLayout}
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600"
            >
              Generate Layout
            </button>
          </div>

          {/* Seat Layout Preview */}
          <div className="lg:col-span-2">
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-center mb-4">
                <div className="inline-flex items-center bg-gray-800 text-white px-4 py-2 rounded">
                  <Users className="w-4 h-4 mr-2" />
                  Driver
                </div>
              </div>
              
              <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${currentLayout.cols}, 1fr)` }}>
                {currentLayout.seats.map((seat) => (
                  <button
                    key={seat.id}
                    onClick={() => setSelectedSeat(seat)}
                    className={`w-12 h-12 rounded border-2 text-xs font-bold transition-colors ${
                      seat.col === 2 ? 'invisible' : // Aisle space
                      selectedSeat?.id === seat.id ? 'border-blue-500 bg-blue-100' :
                      seat.type === 'vip' ? 'border-purple-300 bg-purple-100' :
                      seat.type === 'premium' ? 'border-orange-300 bg-orange-100' :
                      seat.status === 'occupied' ? 'border-red-300 bg-red-100' :
                      'border-green-300 bg-green-100'
                    }`}
                  >
                    {seat.col !== 2 && seat.id}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Smart Seat Management</h2>
        <button 
          onClick={() => setShowDesigner(true)}
          className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 flex items-center"
        >
          <Plus className="w-4 h-4 mr-2" />
          Design Layout
        </button>
      </div>

      {showDesigner ? (
        <SeatDesigner />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {seatLayouts.map((layout) => (
            <motion.div
              key={layout.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-lg shadow-md p-6"
            >
              <h3 className="text-lg font-semibold mb-2">{layout.name}</h3>
              <p className="text-gray-600 mb-4">{layout.vehicle_type}</p>
              <div className="space-y-2 text-sm">
                <div>Total Seats: <span className="font-medium">{layout.total_seats}</span></div>
                <div>Configuration: <span className="font-medium">{layout.rows}x{layout.cols}</span></div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
};

// Flight Operation Management
export const FlightOperationManagement = () => {
  const [flights, setFlights] = useState([]);
  const [airlines, setAirlines] = useState([]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold flex items-center">
          <Plane className="w-8 h-8 mr-3 text-blue-600" />
          Flight Operation Management
        </h2>
        <button className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 flex items-center">
          <Plus className="w-4 h-4 mr-2" />
          Add Flight
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Flights</p>
              <p className="text-2xl font-bold">156</p>
            </div>
            <Plane className="w-8 h-8 text-blue-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Airlines</p>
              <p className="text-2xl font-bold">12</p>
            </div>
            <Building className="w-8 h-8 text-green-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">On-Time Performance</p>
              <p className="text-2xl font-bold">94%</p>
            </div>
            <Clock className="w-8 h-8 text-orange-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Monthly Revenue</p>
              <p className="text-2xl font-bold">$245K</p>
            </div>
            <DollarSign className="w-8 h-8 text-purple-500" />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Flight Schedule Management</h3>
        <div className="text-center py-8">
          <Plane className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">Flight management system will be implemented here</p>
        </div>
      </div>
    </div>
  );
};

// Taxi Operation Management
export const TaxiOperationManagement = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold flex items-center">
          <Car className="w-8 h-8 mr-3 text-yellow-600" />
          Taxi Operation Management
        </h2>
        <button className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 flex items-center">
          <Plus className="w-4 h-4 mr-2" />
          Add Taxi
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Taxis</p>
              <p className="text-2xl font-bold">89</p>
            </div>
            <Car className="w-8 h-8 text-yellow-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Drivers</p>
              <p className="text-2xl font-bold">156</p>
            </div>
            <Users className="w-8 h-8 text-green-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Daily Trips</p>
              <p className="text-2xl font-bold">342</p>
            </div>
            <Navigation className="w-8 h-8 text-blue-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Revenue</p>
              <p className="text-2xl font-bold">$8.5K</p>
            </div>
            <DollarSign className="w-8 h-8 text-purple-500" />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Taxi Fleet Management</h3>
        <div className="text-center py-8">
          <Car className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">Taxi management system will be implemented here</p>
        </div>
      </div>
    </div>
  );
};

// Ferry Operation Management
export const FerryOperationManagement = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold flex items-center">
          <Ship className="w-8 h-8 mr-3 text-blue-600" />
          Ferry Operation Management
        </h2>
        <button className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 flex items-center">
          <Plus className="w-4 h-4 mr-2" />
          Add Ferry
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Active Ferries</p>
              <p className="text-2xl font-bold">24</p>
            </div>
            <Ship className="w-8 h-8 text-blue-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Routes</p>
              <p className="text-2xl font-bold">8</p>
            </div>
            <Route className="w-8 h-8 text-green-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Daily Passengers</p>
              <p className="text-2xl font-bold">1,234</p>
            </div>
            <Users className="w-8 h-8 text-orange-500" />
          </div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Revenue</p>
              <p className="text-2xl font-bold">$12.3K</p>
            </div>
            <DollarSign className="w-8 h-8 text-purple-500" />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Ferry Fleet Management</h3>
        <div className="text-center py-8">
          <Ship className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">Ferry management system will be implemented here</p>
        </div>
      </div>
    </div>
  );
};