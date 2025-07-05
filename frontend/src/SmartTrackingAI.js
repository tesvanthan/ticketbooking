import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { 
  MapPin, 
  Clock, 
  Bus, 
  Navigation, 
  AlertCircle, 
  CheckCircle, 
  Phone, 
  MessageCircle, 
  Bell,
  Eye,
  Route,
  Users,
  Calendar,
  Star,
  ThumbsUp,
  Share2,
  Download,
  Zap,
  Target,
  TrendingUp,
  BarChart3,
  Settings,
  Loader2,
  Smartphone,
  Wifi,
  Battery,
  Signal,
  Search,
  Filter,
  ArrowRight,
  MapPinIcon,
  ClockIcon,
  BusIcon
} from 'lucide-react';
import { useAuth } from './components';

// AI-Powered Real-time Tracking Component
export const SmartTrackingAI = ({ bookingId, tripData }) => {
  const [trackingData, setTrackingData] = useState({
    currentLocation: 'Phnom Penh Central Station',
    nextStop: 'Kampong Chhnang',
    estimatedArrival: '2025-07-05 14:30:00',
    busStatus: 'on_time',
    progress: 65,
    delay: 0,
    driver: {
      name: 'Mr. Sophea Chea',
      rating: 4.8,
      phone: '+855 12 345 678'
    },
    weather: 'sunny',
    traffic: 'light',
    passengers: 28,
    capacity: 45
  });

  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'info',
      message: 'Your bus is currently 5 minutes ahead of schedule',
      time: '13:45',
      read: false
    },
    {
      id: 2,
      type: 'update',
      message: 'Next stop: Kampong Chhnang in 15 minutes',
      time: '13:40',
      read: false
    }
  ]);

  const [isLiveTracking, setIsLiveTracking] = useState(true);
  const [smartAlerts, setSmartAlerts] = useState(true);
  const [shareTracking, setShareTracking] = useState(false);
  const { user } = useAuth();

  // Simulate real-time updates
  useEffect(() => {
    if (!isLiveTracking) return;

    const interval = setInterval(() => {
      // Simulate progress updates
      setTrackingData(prev => ({
        ...prev,
        progress: Math.min(prev.progress + Math.random() * 2, 100),
        estimatedArrival: calculateNewETA(prev.estimatedArrival),
        passengers: Math.max(20, prev.passengers + Math.floor(Math.random() * 3 - 1))
      }));
    }, 10000); // Update every 10 seconds

    return () => clearInterval(interval);
  }, [isLiveTracking]);

  const calculateNewETA = (currentETA) => {
    // AI logic to calculate new ETA based on traffic, weather, etc.
    const eta = new Date(currentETA);
    const adjustment = Math.floor(Math.random() * 4 - 2); // -2 to +2 minutes
    eta.setMinutes(eta.getMinutes() + adjustment);
    return eta.toISOString();
  };

  const formatTime = (timeStr) => {
    return new Date(timeStr).toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'on_time': return 'text-green-600 bg-green-100';
      case 'delayed': return 'text-yellow-600 bg-yellow-100';
      case 'early': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const shareTrackingInfo = () => {
    const message = `🚌 Live Bus Tracking: ${trackingData.currentLocation} → ${tripData?.destination}\n📍 Current: ${trackingData.currentLocation}\n⏰ ETA: ${formatTime(trackingData.estimatedArrival)}\n📊 Progress: ${trackingData.progress}%\n\nTrack live: https://busticket.com/track/${bookingId}`;
    
    if (navigator.share) {
      navigator.share({
        title: 'Live Bus Tracking',
        text: message,
        url: `https://busticket.com/track/${bookingId}`
      });
    } else {
      navigator.clipboard.writeText(message);
      alert('Tracking info copied to clipboard!');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-xl p-6 mb-8"
          >
            <div className="flex justify-between items-center mb-4">
              <h1 className="text-3xl font-bold text-gray-800">🚌 Smart AI Tracking</h1>
              <div className="flex items-center space-x-4">
                <div className={`flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(trackingData.busStatus)}`}>
                  <div className="w-2 h-2 bg-current rounded-full mr-2 animate-pulse"></div>
                  {trackingData.busStatus.replace('_', ' ').toUpperCase()}
                </div>
                <button
                  onClick={() => setIsLiveTracking(!isLiveTracking)}
                  className={`p-2 rounded-lg ${isLiveTracking ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-600'}`}
                >
                  {isLiveTracking ? <Zap className="w-5 h-5" /> : <Loader2 className="w-5 h-5" />}
                </button>
                <button
                  onClick={shareTrackingInfo}
                  className="p-2 rounded-lg bg-blue-100 text-blue-600 hover:bg-blue-200"
                >
                  <Share2 className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Trip Info */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center space-x-3">
                <MapPin className="w-5 h-5 text-orange-500" />
                <div>
                  <div className="text-sm text-gray-600">From</div>
                  <div className="font-semibold">{tripData?.origin || 'Phnom Penh'}</div>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Navigation className="w-5 h-5 text-purple-500" />
                <div>
                  <div className="text-sm text-gray-600">To</div>
                  <div className="font-semibold">{tripData?.destination || 'Siem Reap'}</div>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Clock className="w-5 h-5 text-blue-500" />
                <div>
                  <div className="text-sm text-gray-600">ETA</div>
                  <div className="font-semibold">{formatTime(trackingData.estimatedArrival)}</div>
                </div>
              </div>
            </div>
          </motion.div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Live Map & Progress */}
            <div className="lg:col-span-2 space-y-6">
              {/* Progress Bar */}
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-xl font-bold mb-4">Journey Progress</h3>
                <div className="relative">
                  <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
                    <motion.div
                      className="bg-gradient-to-r from-green-400 to-blue-500 h-4 rounded-full relative"
                      style={{ width: `${trackingData.progress}%` }}
                      initial={{ width: 0 }}
                      animate={{ width: `${trackingData.progress}%` }}
                      transition={{ duration: 1 }}
                    >
                      <div className="absolute -right-2 -top-1 w-6 h-6 bg-blue-500 rounded-full border-2 border-white shadow-lg flex items-center justify-center">
                        <Bus className="w-3 h-3 text-white" />
                      </div>
                    </motion.div>
                  </div>
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>{tripData?.origin || 'Start'}</span>
                    <span className="font-medium">{trackingData.progress}% Complete</span>
                    <span>{tripData?.destination || 'End'}</span>
                  </div>
                </div>
              </motion.div>

              {/* Live Map Placeholder */}
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-xl font-bold mb-4">Live Location</h3>
                <div className="h-80 bg-gradient-to-br from-blue-100 to-green-100 rounded-lg flex items-center justify-center relative overflow-hidden">
                  {/* Animated background pattern */}
                  <div className="absolute inset-0 opacity-20">
                    <div className="absolute top-4 left-4 w-2 h-2 bg-blue-400 rounded-full animate-ping"></div>
                    <div className="absolute top-12 right-8 w-1 h-1 bg-green-400 rounded-full animate-pulse"></div>
                    <div className="absolute bottom-8 left-12 w-3 h-3 bg-purple-400 rounded-full animate-bounce"></div>
                  </div>
                  
                  <div className="text-center z-10">
                    <MapPin className="w-16 h-16 text-orange-500 mx-auto mb-4 animate-bounce" />
                    <h4 className="text-xl font-bold text-gray-700 mb-2">Currently at:</h4>
                    <p className="text-lg font-semibold text-orange-600">{trackingData.currentLocation}</p>
                    <p className="text-sm text-gray-600 mt-2">Next: {trackingData.nextStop}</p>
                  </div>
                  
                  {/* Live indicators */}
                  <div className="absolute top-4 right-4 flex items-center space-x-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                    <span className="text-sm font-medium text-gray-700">LIVE</span>
                  </div>
                </div>
              </motion.div>

              {/* Trip Statistics */}
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-xl font-bold mb-4">Trip Analytics</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <Users className="w-8 h-8 text-blue-500 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-blue-600">{trackingData.passengers}</div>
                    <div className="text-sm text-gray-600">Passengers</div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <Target className="w-8 h-8 text-green-500 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-green-600">{trackingData.capacity}</div>
                    <div className="text-sm text-gray-600">Capacity</div>
                  </div>
                  <div className="text-center p-4 bg-yellow-50 rounded-lg">
                    <TrendingUp className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-yellow-600">4.8★</div>
                    <div className="text-sm text-gray-600">Trip Rating</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <Zap className="w-8 h-8 text-purple-500 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-purple-600">95%</div>
                    <div className="text-sm text-gray-600">On-Time</div>
                  </div>
                </div>
              </motion.div>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Smart Notifications */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-bold">Smart Alerts</h3>
                  <button
                    onClick={() => setSmartAlerts(!smartAlerts)}
                    className={`p-2 rounded-lg ${smartAlerts ? 'bg-orange-100 text-orange-600' : 'bg-gray-100 text-gray-600'}`}
                  >
                    <Bell className={`w-4 h-4 ${smartAlerts ? 'animate-ring' : ''}`} />
                  </button>
                </div>
                
                <div className="space-y-3 max-h-60 overflow-y-auto">
                  {notifications.map((notification) => (
                    <motion.div
                      key={notification.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className={`p-3 rounded-lg border-l-4 ${
                        notification.type === 'info' ? 'bg-blue-50 border-blue-400' :
                        notification.type === 'update' ? 'bg-green-50 border-green-400' :
                        'bg-yellow-50 border-yellow-400'
                      }`}
                    >
                      <div className="flex justify-between items-start">
                        <p className="text-sm text-gray-700">{notification.message}</p>
                        <span className="text-xs text-gray-500">{notification.time}</span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>

              {/* Driver Info */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-lg font-bold mb-4">Driver Information</h3>
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-red-500 rounded-full mx-auto mb-3 flex items-center justify-center">
                    <span className="text-white font-bold text-xl">SC</span>
                  </div>
                  <h4 className="font-semibold text-gray-800">{trackingData.driver.name}</h4>
                  <div className="flex items-center justify-center mt-2">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="ml-1 text-sm text-gray-600">{trackingData.driver.rating}</span>
                  </div>
                  <button className="mt-3 flex items-center justify-center w-full bg-green-100 text-green-700 py-2 px-4 rounded-lg hover:bg-green-200 transition-colors">
                    <Phone className="w-4 h-4 mr-2" />
                    Call Driver
                  </button>
                </div>
              </motion.div>

              {/* Quick Actions */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-lg font-bold mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <button className="w-full flex items-center justify-between p-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors">
                    <span className="flex items-center">
                      <MessageCircle className="w-4 h-4 mr-2" />
                      Contact Support
                    </span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                  
                  <button className="w-full flex items-center justify-between p-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors">
                    <span className="flex items-center">
                      <Download className="w-4 h-4 mr-2" />
                      Download Ticket
                    </span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                  
                  <button className="w-full flex items-center justify-between p-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors">
                    <span className="flex items-center">
                      <ThumbsUp className="w-4 h-4 mr-2" />
                      Rate Trip
                    </span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>

              {/* System Status */}
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-lg font-bold mb-4">System Status</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="flex items-center text-sm text-gray-600">
                      <Wifi className="w-4 h-4 mr-2" />
                      Connection
                    </span>
                    <div className="flex items-center text-green-600">
                      <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                      <span className="text-sm font-medium">Excellent</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="flex items-center text-sm text-gray-600">
                      <Signal className="w-4 h-4 mr-2" />
                      GPS Signal
                    </span>
                    <div className="flex items-center text-green-600">
                      <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                      <span className="text-sm font-medium">Strong</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="flex items-center text-sm text-gray-600">
                      <Battery className="w-4 h-4 mr-2" />
                      Device Battery
                    </span>
                    <div className="flex items-center text-blue-600">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                      <span className="text-sm font-medium">78%</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Quick Buy Component for Easy Booking
export const QuickBuyWidget = ({ onQuickBook }) => {
  const [quickSearch, setQuickSearch] = useState({
    from: '',
    to: '',
    date: new Date().toISOString().split('T')[0]
  });
  const [popularRoutes] = useState([
    { from: 'Phnom Penh', to: 'Siem Reap', price: 15, duration: '6h' },
    { from: 'Phnom Penh', to: 'Sihanoukville', price: 12, duration: '4h' },
    { from: 'Siem Reap', to: 'Battambang', price: 8, duration: '3h' }
  ]);

  const handleQuickBook = (route) => {
    onQuickBook({
      ...route,
      date: quickSearch.date
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-xl shadow-lg p-6 mb-8"
    >
      <h3 className="text-xl font-bold mb-4">⚡ Quick Book</h3>
      
      {/* Quick Search */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">From</label>
          <input
            type="text"
            value={quickSearch.from}
            onChange={(e) => setQuickSearch({...quickSearch, from: e.target.value})}
            placeholder="Origin"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">To</label>
          <input
            type="text"
            value={quickSearch.to}
            onChange={(e) => setQuickSearch({...quickSearch, to: e.target.value})}
            placeholder="Destination"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
          <input
            type="date"
            value={quickSearch.date}
            onChange={(e) => setQuickSearch({...quickSearch, date: e.target.value})}
            min={new Date().toISOString().split('T')[0]}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
          />
        </div>
        <div className="flex items-end">
          <button className="w-full bg-gradient-to-r from-orange-500 to-red-500 text-white py-2 px-4 rounded-lg hover:from-orange-600 hover:to-red-600 transition-all transform hover:scale-105">
            Search & Book
          </button>
        </div>
      </div>

      {/* Popular Routes */}
      <div>
        <h4 className="font-semibold text-gray-800 mb-3">🔥 Popular Routes</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {popularRoutes.map((route, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="border border-gray-200 rounded-lg p-4 hover:border-orange-300 hover:shadow-md transition-all cursor-pointer"
              onClick={() => handleQuickBook(route)}
            >
              <div className="flex justify-between items-center mb-2">
                <span className="font-medium">{route.from} → {route.to}</span>
                <span className="text-orange-600 font-bold">${route.price}</span>
              </div>
              <div className="text-sm text-gray-600">{route.duration} journey</div>
              <button className="w-full mt-2 bg-orange-500 text-white py-1 px-3 rounded text-sm hover:bg-orange-600 transition-colors">
                Book Now
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};