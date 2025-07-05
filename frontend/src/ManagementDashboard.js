import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BarChart3, 
  Users, 
  Bus, 
  Route, 
  UserCog, 
  Settings, 
  TrendingUp, 
  AlertTriangle, 
  Clock, 
  DollarSign, 
  MapPin, 
  Calendar, 
  Eye, 
  Plus, 
  Edit3, 
  Trash2, 
  Download, 
  RefreshCw, 
  Search, 
  Filter, 
  ChevronDown, 
  CheckCircle, 
  XCircle, 
  AlertCircle,
  Brain,
  Zap,
  Target,
  Activity,
  Gauge,
  Layers,
  ShieldCheck,
  PieChart,
  LineChart,
  Building,
  Car,
  UserCheck,
  CreditCard,
  Star
} from 'lucide-react';
import { useAuth } from './components';

// Management Dashboard Component
export const ManagementDashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'operators', label: 'Bus Operators', icon: Building },
    { id: 'vehicles', label: 'Fleet Management', icon: Bus },
    { id: 'routes', label: 'Route Management', icon: Route },
    { id: 'agents', label: 'Travel Agents', icon: UserCog },
    { id: 'bookings', label: 'Seat Management', icon: Users },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'ai', label: 'AI Insights', icon: Brain }
  ];

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/management/realtime/dashboard`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-red-600 rounded-full flex items-center justify-center">
                <Bus className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">BusTicket Management</h1>
                <p className="text-sm text-gray-500">Smart AI-Powered Platform</p>
              </div>
            </div>
            <button
              onClick={fetchDashboardData}
              className="flex items-center space-x-2 bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Refresh</span>
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex space-x-8">
          {/* Sidebar Navigation */}
          <div className="w-64 space-y-2">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                    activeTab === tab.id
                      ? 'bg-orange-500 text-white'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{tab.label}</span>
                </button>
              );
            })}
          </div>

          {/* Main Content */}
          <div className="flex-1">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.2 }}
              >
                {activeTab === 'dashboard' && <DashboardOverview data={dashboardData} loading={loading} />}
                {activeTab === 'operators' && <OperatorManagement token={token} />}
                {activeTab === 'vehicles' && <VehicleManagement token={token} />}
                {activeTab === 'routes' && <RouteManagement token={token} />}
                {activeTab === 'agents' && <AgentManagement token={token} />}
                {activeTab === 'bookings' && <SeatManagement token={token} />}
                {activeTab === 'analytics' && <AnalyticsDashboard token={token} />}
                {activeTab === 'ai' && <AIInsights token={token} />}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
};

// Dashboard Overview Component
const DashboardOverview = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center py-16">
        <RefreshCw className="w-8 h-8 animate-spin text-orange-500" />
      </div>
    );
  }

  const stats = [
    { label: 'Active Bookings', value: data?.active_bookings || 0, icon: Users, color: 'text-blue-600 bg-blue-100' },
    { label: 'Today\'s Revenue', value: `$${data?.revenue_today || 0}`, icon: DollarSign, color: 'text-green-600 bg-green-100' },
    { label: 'Active Vehicles', value: data?.active_vehicles || 0, icon: Bus, color: 'text-purple-600 bg-purple-100' },
    { label: 'System Alerts', value: data?.alerts?.length || 0, icon: AlertTriangle, color: 'text-red-600 bg-red-100' }
  ];

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl shadow-sm p-6"
            >
              <div className="flex items-center">
                <div className={`w-12 h-12 rounded-lg ${stat.color} flex items-center justify-center`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Alerts */}
      {data?.alerts && data.alerts.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Alerts</h3>
          <div className="space-y-3">
            {data.alerts.map((alert, index) => (
              <div key={index} className={`flex items-center p-3 rounded-lg ${
                alert.priority === 'high' ? 'bg-red-50 border border-red-200' :
                alert.priority === 'medium' ? 'bg-yellow-50 border border-yellow-200' :
                'bg-blue-50 border border-blue-200'
              }`}>
                <AlertTriangle className={`w-5 h-5 ${
                  alert.priority === 'high' ? 'text-red-500' :
                  alert.priority === 'medium' ? 'text-yellow-500' :
                  'text-blue-500'
                }`} />
                <span className="ml-3 text-sm text-gray-700">{alert.message}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="flex flex-col items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors">
            <Plus className="w-6 h-6 text-blue-600 mb-2" />
            <span className="text-sm font-medium text-blue-600">Add Operator</span>
          </button>
          <button className="flex flex-col items-center p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
            <Car className="w-6 h-6 text-green-600 mb-2" />
            <span className="text-sm font-medium text-green-600">Add Vehicle</span>
          </button>
          <button className="flex flex-col items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
            <Route className="w-6 h-6 text-purple-600 mb-2" />
            <span className="text-sm font-medium text-purple-600">Add Route</span>
          </button>
          <button className="flex flex-col items-center p-4 bg-orange-50 rounded-lg hover:bg-orange-100 transition-colors">
            <BarChart3 className="w-6 h-6 text-orange-600 mb-2" />
            <span className="text-sm font-medium text-orange-600">View Analytics</span>
          </button>
        </div>
      </div>
    </div>
  );
};

// Operator Management Component
const OperatorManagement = ({ token }) => {
  const [operators, setOperators] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    fetchOperators();
  }, []);

  const fetchOperators = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/management/operators`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setOperators(data);
      }
    } catch (error) {
      console.error('Error fetching operators:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Bus Operators</h2>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center space-x-2 bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Add Operator</span>
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-16">
          <RefreshCw className="w-8 h-8 animate-spin text-orange-500" />
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Operator</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Contact</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fleet</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Revenue</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {operators.map((operator) => (
                  <tr key={operator.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center">
                          <Building className="w-5 h-5 text-orange-600" />
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{operator.name}</div>
                          <div className="text-sm text-gray-500">{operator.license_number}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{operator.email}</div>
                      <div className="text-sm text-gray-500">{operator.phone}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{operator.total_buses} vehicles</div>
                      <div className="text-sm text-gray-500">{operator.total_routes} routes</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">${operator.revenue || 0}</div>
                      <div className="text-sm text-gray-500">{operator.total_bookings} bookings</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        operator.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {operator.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                      <button className="text-blue-600 hover:text-blue-900">
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button className="text-red-600 hover:text-red-900">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Create Operator Modal */}
      <CreateOperatorModal 
        isOpen={showCreateModal} 
        onClose={() => setShowCreateModal(false)} 
        onSuccess={fetchOperators}
        token={token}
      />
    </div>
  );
};

// Create Operator Modal
const CreateOperatorModal = ({ isOpen, onClose, onSuccess, token }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    license_number: '',
    commission_rate: 0.10
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/management/operators`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        onSuccess();
        onClose();
        setFormData({
          name: '', email: '', phone: '', address: '', license_number: '', commission_rate: 0.10
        });
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error creating operator:', error);
      alert('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-md">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Operator</h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">License Number</label>
            <input
              type="text"
              value={formData.license_number}
              onChange={(e) => setFormData({...formData, license_number: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Commission Rate</label>
            <input
              type="number"
              step="0.01"
              min="0"
              max="1"
              value={formData.commission_rate}
              onChange={(e) => setFormData({...formData, commission_rate: parseFloat(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              required
            />
          </div>

          <div className="flex space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Operator'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Vehicle Management Component
const VehicleManagement = ({ token }) => {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchVehicles();
  }, []);

  const fetchVehicles = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/management/vehicles`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setVehicles(data);
      }
    } catch (error) {
      console.error('Error fetching vehicles:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Fleet Management</h2>
        <button className="flex items-center space-x-2 bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors">
          <Plus className="w-4 h-4" />
          <span>Add Vehicle</span>
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-16">
          <RefreshCw className="w-8 h-8 animate-spin text-orange-500" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {vehicles.map((vehicle) => (
            <div key={vehicle.id} className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Bus className="w-6 h-6 text-blue-600" />
                </div>
                <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                  vehicle.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {vehicle.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>

              <h3 className="text-lg font-semibold text-gray-900 mb-2">{vehicle.license_plate}</h3>
              <p className="text-sm text-gray-600 mb-4">{vehicle.brand} {vehicle.model} ({vehicle.year})</p>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Type:</span>
                  <span className="text-gray-900">{vehicle.vehicle_type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Seats:</span>
                  <span className="text-gray-900">{vehicle.total_seats}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Total Trips:</span>
                  <span className="text-gray-900">{vehicle.total_trips || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Revenue:</span>
                  <span className="text-gray-900">${vehicle.revenue || 0}</span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200 flex space-x-2">
                <button className="flex-1 text-sm text-blue-600 hover:text-blue-800">Edit</button>
                <button className="flex-1 text-sm text-red-600 hover:text-red-800">Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// AI Insights Component
const AIInsights = ({ token }) => {
  const [insights, setInsights] = useState(null);
  const [pricing, setPricing] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAIInsights();
  }, []);

  const fetchAIInsights = async () => {
    try {
      const [insightsResponse, pricingResponse] = await Promise.all([
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/management/ai/optimize-routes`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/management/ai/dynamic-pricing`, {
          method: 'POST',
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ route_id: "sample_route", date: "2025-07-10" })
        })
      ]);

      if (insightsResponse.ok) {
        const insightsData = await insightsResponse.json();
        setInsights(insightsData);
      }

      if (pricingResponse.ok) {
        const pricingData = await pricingResponse.json();
        setPricing(pricingData);
      }
    } catch (error) {
      console.error('Error fetching AI insights:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">AI Insights & Optimization</h2>
        <button
          onClick={fetchAIInsights}
          className="flex items-center space-x-2 bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors"
        >
          <Brain className="w-4 h-4" />
          <span>Refresh Insights</span>
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-16">
          <RefreshCw className="w-8 h-8 animate-spin text-orange-500" />
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Route Optimization */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Route Optimization</h3>
            </div>

            {insights?.recommendations && insights.recommendations.length > 0 ? (
              <div className="space-y-3">
                {insights.recommendations.map((rec, index) => (
                  <div key={index} className="bg-blue-50 rounded-lg p-4">
                    <div className="flex items-start space-x-3">
                      <Zap className="w-5 h-5 text-blue-600 mt-0.5" />
                      <div>
                        <p className="font-medium text-gray-900">{rec.route}</p>
                        <p className="text-sm text-gray-600 mt-1">{rec.suggested_action}</p>
                        <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                          <span>Demand: {rec.demand}%</span>
                          <span>Type: {rec.type}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No optimization recommendations available.</p>
            )}
          </div>

          {/* Dynamic Pricing */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <DollarSign className="w-5 h-5 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Smart Pricing</h3>
            </div>

            {pricing ? (
              <div className="space-y-4">
                <div className="bg-green-50 rounded-lg p-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">Base Price</span>
                    <span className="text-lg font-bold text-gray-900">${pricing.base_price}</span>
                  </div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700">Optimized Price</span>
                    <span className="text-lg font-bold text-green-600">${pricing.dynamic_price}</span>
                  </div>
                  <div className="text-xs text-gray-500 mt-2">
                    Recommendation: {pricing.recommendation}
                  </div>
                </div>

                <div className="space-y-2">
                  <h4 className="text-sm font-medium text-gray-700">Pricing Factors</h4>
                  {Object.entries(pricing.factors).map(([key, value]) => (
                    <div key={key} className="flex justify-between text-sm">
                      <span className="text-gray-600 capitalize">{key.replace('_', ' ')}</span>
                      <span className="text-gray-900">{value.toFixed(2)}x</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-gray-500">No pricing data available.</p>
            )}
          </div>

          {/* Performance Metrics */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <Activity className="w-5 h-5 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">AI Performance Metrics</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">95%</div>
                <div className="text-sm text-gray-600">Prediction Accuracy</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">23%</div>
                <div className="text-sm text-gray-600">Revenue Increase</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">87%</div>
                <div className="text-sm text-gray-600">Optimization Success</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Seat Management Component  
const SeatManagement = ({ token }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Smart Seat Management</h2>
      <div className="bg-white rounded-xl shadow-sm p-6">
        <p className="text-gray-600">Advanced seat management features coming soon...</p>
      </div>
    </div>
  );
};

// Route Management Component
const RouteManagement = ({ token }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Route Management</h2>
      <div className="bg-white rounded-xl shadow-sm p-6">
        <p className="text-gray-600">Route management features coming soon...</p>
      </div>
    </div>
  );
};

// Agent Management Component
const AgentManagement = ({ token }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Travel Agent Management</h2>
      <div className="bg-white rounded-xl shadow-sm p-6">
        <p className="text-gray-600">Agent management features coming soon...</p>
      </div>
    </div>
  );
};

// Analytics Dashboard Component
const AnalyticsDashboard = ({ token }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Analytics & Reports</h2>
      <div className="bg-white rounded-xl shadow-sm p-6">
        <p className="text-gray-600">Advanced analytics features coming soon...</p>
      </div>
    </div>
  );
};

export default ManagementDashboard;