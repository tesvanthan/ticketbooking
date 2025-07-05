import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Search, 
  MapPin, 
  Calendar, 
  Users, 
  Bus, 
  Car, 
  Plane, 
  Ship, 
  Star, 
  CheckCircle, 
  Phone, 
  Mail, 
  Clock, 
  Shield, 
  CreditCard, 
  Headphones, 
  Award, 
  Navigation, 
  Wifi, 
  Coffee, 
  Smartphone, 
  Brain, 
  TrendingUp, 
  Eye, 
  MessageCircle, 
  Globe, 
  Menu, 
  X, 
  ArrowRight, 
  ArrowLeft, 
  ChevronDown, 
  ChevronRight,
  User,
  LogOut,
  BookOpen,
  Settings,
  CreditCard as CardIcon,
  BarChart3,
  Loader2,
  Cog
} from 'lucide-react';
import './App.css';
import { 
  AuthProvider, 
  useAuth, 
  LoginModal, 
  RegisterModal,
  SearchResults,
  SeatSelection,
  Payment,
  BookingConfirmation
} from './components';
import { ManagementDashboard } from './ManagementDashboard';
import { UserProfile } from './UserProfile';
import { AffiliateProgram } from './AffiliateProgram';
import { TicketManagement } from './TicketManagement';
import { PaymentManagement } from './PaymentManagement';
import { AdminManagement } from './AdminManagement';
import { SmartTrackingAI, QuickBuyWidget } from './SmartTrackingAI';
import { SmartNotificationSystem } from './SmartNotificationSystem';
import { 
  RouteManagement, 
  AgentManagement, 
  SmartSeatManagement,
  FlightOperationManagement,
  TaxiOperationManagement,
  FerryOperationManagement
} from './OperationManagement';

// Enhanced Header Component with Authentication
const Header = ({ activeTab, setActiveTab }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const { user, logout } = useAuth();

  const tabs = [
    { id: 'bus', label: 'Bus', icon: Bus },
    { id: 'private', label: 'Private Transfer', icon: Car },
    { id: 'airport', label: 'Airport Transfer', icon: Plane },
    { id: 'ferry', label: 'Ferry', icon: Ship }
  ];

  const handleLogout = () => {
    logout();
    setShowUserMenu(false);
  };

  return (
    <>
      <header className="bg-white shadow-lg sticky top-0 z-50">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between py-4">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-red-600 rounded-full flex items-center justify-center">
                <Bus className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-800">BusTicket</span>
            </Link>

            {/* Navigation */}
            <nav className="hidden lg:flex items-center space-x-8">
              <Link to="/" className="text-gray-700 hover:text-orange-500 transition-colors">Home</Link>
              <Link to="/routes" className="text-gray-700 hover:text-orange-500 transition-colors">Routes</Link>
              {user && (
                <>
                  <Link to="/my-bookings" className="text-gray-700 hover:text-orange-500 transition-colors">My Bookings</Link>
                  <Link to="/management" className="text-gray-700 hover:text-orange-500 transition-colors flex items-center space-x-1">
                    <Cog className="w-4 h-4" />
                    <span>Management</span>
                  </Link>
                </>
              )}
              <Link to="/about" className="text-gray-700 hover:text-orange-500 transition-colors">About</Link>
              <Link to="/contact" className="text-gray-700 hover:text-orange-500 transition-colors">Contact</Link>
            </nav>

            {/* Auth Section */}
            <div className="hidden lg:flex items-center space-x-4">
              {user ? (
                <div className="relative">
                  <button
                    onClick={() => setShowUserMenu(!showUserMenu)}
                    className="flex items-center space-x-2 text-gray-700 hover:text-orange-500 transition-colors"
                  >
                    <User className="w-5 h-5" />
                    <span>{user.first_name}</span>
                    <ChevronDown className="w-4 h-4" />
                  </button>
                  
                  {showUserMenu && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2">
                      <Link
                        to="/profile"
                        className="block px-4 py-2 text-gray-700 hover:bg-gray-100 transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        <User className="w-4 h-4 inline mr-2" />
                        Profile
                      </Link>
                      <Link
                        to="/my-bookings"
                        className="block px-4 py-2 text-gray-700 hover:bg-gray-100 transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        <BookOpen className="w-4 h-4 inline mr-2" />
                        My Bookings
                      </Link>
                      <Link
                        to="/management"
                        className="block px-4 py-2 text-gray-700 hover:bg-gray-100 transition-colors"
                        onClick={() => setShowUserMenu(false)}
                      >
                        <Cog className="w-4 h-4 inline mr-2" />
                        Management
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 transition-colors"
                      >
                        <LogOut className="w-4 h-4 inline mr-2" />
                        Logout
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <>
                  <button 
                    onClick={() => setShowLoginModal(true)}
                    className="text-gray-700 hover:text-orange-500 transition-colors"
                  >
                    LOGIN
                  </button>
                  <button 
                    onClick={() => setShowRegisterModal(true)}
                    className="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors"
                  >
                    REGISTER
                  </button>
                </>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button 
              className="lg:hidden"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Service Tabs */}
          <div className="border-t border-gray-200 py-4">
            <div className="flex flex-wrap gap-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                      activeTab === tab.id 
                        ? 'bg-orange-500 text-white' 
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="text-sm font-medium">{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="lg:hidden bg-white border-t border-gray-200"
            >
              <div className="px-4 py-4 space-y-2">
                <Link to="/" className="block py-2 text-gray-700 hover:text-orange-500">Home</Link>
                <Link to="/routes" className="block py-2 text-gray-700 hover:text-orange-500">Routes</Link>
                {user && (
                  <>
                    <Link to="/my-bookings" className="block py-2 text-gray-700 hover:text-orange-500">My Bookings</Link>
                    <Link to="/management" className="block py-2 text-gray-700 hover:text-orange-500">Management</Link>
                  </>
                )}
                <Link to="/about" className="block py-2 text-gray-700 hover:text-orange-500">About</Link>
                <Link to="/contact" className="block py-2 text-gray-700 hover:text-orange-500">Contact</Link>
                
                {user ? (
                  <div className="pt-4 border-t border-gray-200">
                    <div className="text-gray-600 mb-2">Hello, {user.first_name}!</div>
                    <Link to="/profile" className="block py-2 text-gray-700 hover:text-orange-500">Profile</Link>
                    <button onClick={handleLogout} className="block py-2 text-gray-700 hover:text-orange-500">Logout</button>
                  </div>
                ) : (
                  <div className="flex space-x-4 pt-4">
                    <button 
                      onClick={() => setShowLoginModal(true)}
                      className="text-gray-700 hover:text-orange-500"
                    >
                      LOGIN
                    </button>
                    <button 
                      onClick={() => setShowRegisterModal(true)}
                      className="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600"
                    >
                      REGISTER
                    </button>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </header>

      {/* Modals */}
      <LoginModal 
        isOpen={showLoginModal} 
        onClose={() => setShowLoginModal(false)}
        onSwitchToRegister={() => {
          setShowLoginModal(false);
          setShowRegisterModal(true);
        }}
      />
      <RegisterModal 
        isOpen={showRegisterModal} 
        onClose={() => setShowRegisterModal(false)}
        onSwitchToLogin={() => {
          setShowRegisterModal(false);
          setShowLoginModal(true);
        }}
      />
    </>
  );
};

// Enhanced Multi-Transport Search Section with better date handling
const SearchSection = ({ activeTab, onSearch }) => {
  const [searchData, setSearchData] = useState({
    origin: '',
    destination: '',
    date: '',
    passengers: 1
  });
  const [suggestions, setSuggestions] = useState([]);
  const [activeSuggestion, setActiveSuggestion] = useState(null);
  const [loading, setLoading] = useState(false);

  // Set default date to today
  useEffect(() => {
    const today = new Date().toISOString().split('T')[0];
    setSearchData(prev => ({ ...prev, date: today }));
  }, []);

  const handleInputChange = async (field, value) => {
    setSearchData(prev => ({ ...prev, [field]: value }));
    
    if (field === 'origin' || field === 'destination') {
      if (value.length > 2) {
        try {
          const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/suggestions?q=${value}`);
          if (response.ok) {
            const data = await response.json();
            setSuggestions(data);
            setActiveSuggestion(field);
          }
        } catch (error) {
          console.error('Error fetching suggestions:', error);
          // Enhanced fallback suggestions based on transport type
          const transportSuggestions = {
            bus: ['Phnom Penh', 'Siem Reap', 'Sihanoukville', 'Kampot', 'Kep', 'Battambang', 'Poipet'],
            ferry: ['Sihanoukville', 'Koh Rong', 'Koh Rong Sanloem', 'Koh Kong'],
            private: ['Phnom Penh', 'Siem Reap', 'Sihanoukville', 'Airport'],
            airport: ['Phnom Penh Airport', 'Siem Reap Airport', 'Sihanoukville Airport']
          };
          
          const filtered = (transportSuggestions[activeTab] || transportSuggestions.bus)
            .filter(dest => dest.toLowerCase().includes(value.toLowerCase()));
          setSuggestions(filtered.slice(0, 5));
          setActiveSuggestion(field);
        }
      } else {
        setSuggestions([]);
        setActiveSuggestion(null);
      }
    }
  };

  const selectSuggestion = (suggestion) => {
    setSearchData(prev => ({ ...prev, [activeSuggestion]: suggestion }));
    setSuggestions([]);
    setActiveSuggestion(null);
  };

  const handleSearch = async () => {
    if (!searchData.origin || !searchData.destination || !searchData.date) {
      alert('Please fill in all required fields');
      return;
    }

    console.log('Starting search with:', searchData);
    setLoading(true);
    const searchPayload = {
      ...searchData,
      transport_type: activeTab
    };
    
    try {
      await onSearch(searchPayload);
    } catch (error) {
      console.error('Search error:', error);
      alert('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Get search placeholder text based on transport type
  const getPlaceholderText = () => {
    switch (activeTab) {
      case 'private': return { origin: 'Pickup location', destination: 'Drop-off location' };
      case 'airport': return { origin: 'From (City/Airport)', destination: 'To (City/Airport)' };
      case 'ferry': return { origin: 'Port of departure', destination: 'Destination port' };
      default: return { origin: 'Select place of origin', destination: 'Select destination' };
    }
  };

  const placeholders = getPlaceholderText();

  return (
    <section className="relative bg-gradient-to-br from-blue-600 to-purple-700 text-white">
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-20"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1587669011728-ed189a1f6e8d)'
        }}
      />
      <div className="relative container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl lg:text-6xl font-bold mb-4"
          >
            Experience the best way to book your tickets
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl opacity-90"
          >
            Book Bus, Ferry, Taxi around Cambodia, Vietnam, Thailand & Laos
          </motion.p>
        </div>

        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl p-6"
        >
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 items-end">
            {/* Origin */}
            <div className="relative">
              <label className="block text-sm font-medium text-gray-700 mb-2">From</label>
              <div className="relative">
                <MapPin className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={searchData.origin}
                  onChange={(e) => handleInputChange('origin', e.target.value)}
                  placeholder={placeholders.origin}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 text-gray-800"
                />
              </div>
              {activeSuggestion === 'origin' && suggestions.length > 0 && (
                <div className="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-lg shadow-lg z-50 mt-1 max-h-60 overflow-y-auto">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => selectSuggestion(suggestion)}
                      className="w-full text-left px-4 py-3 hover:bg-orange-50 text-gray-800 first:rounded-t-lg last:rounded-b-lg border-b border-gray-100 last:border-b-0 transition-colors"
                    >
                      <div className="flex items-center">
                        <MapPin className="w-4 h-4 text-gray-400 mr-2" />
                        {suggestion}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Destination */}
            <div className="relative">
              <label className="block text-sm font-medium text-gray-700 mb-2">To</label>
              <div className="relative">
                <MapPin className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={searchData.destination}
                  onChange={(e) => handleInputChange('destination', e.target.value)}
                  placeholder={placeholders.destination}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 text-gray-800"
                />
              </div>
              {activeSuggestion === 'destination' && suggestions.length > 0 && (
                <div className="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-lg shadow-lg z-50 mt-1 max-h-60 overflow-y-auto">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => selectSuggestion(suggestion)}
                      className="w-full text-left px-4 py-3 hover:bg-orange-50 text-gray-800 first:rounded-t-lg last:rounded-b-lg border-b border-gray-100 last:border-b-0 transition-colors"
                    >
                      <div className="flex items-center">
                        <MapPin className="w-4 h-4 text-gray-400 mr-2" />
                        {suggestion}
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Departure Date</label>
              <div className="relative">
                <Calendar className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                <input
                  type="date"
                  value={searchData.date}
                  min={new Date().toISOString().split('T')[0]}
                  onChange={(e) => handleInputChange('date', e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 text-gray-800"
                />
              </div>
            </div>

            {/* Passengers */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Passengers</label>
              <div className="relative">
                <Users className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                <select
                  value={searchData.passengers}
                  onChange={(e) => handleInputChange('passengers', parseInt(e.target.value))}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 text-gray-800"
                >
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                    <option key={num} value={num}>{num} {num === 1 ? 'Passenger' : 'Passengers'}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Search Button */}
            <button
              onClick={handleSearch}
              disabled={loading}
              className="bg-green-500 hover:bg-green-600 disabled:opacity-50 text-white px-8 py-3 rounded-lg font-semibold transition-colors flex items-center justify-center space-x-2 h-12"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Search className="w-5 h-5" />
              )}
              <span>{loading ? 'Searching...' : 'Search Tickets'}</span>
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

// Features Section Component (same as before)
const FeaturesSection = () => {
  const features = [
    { icon: Shield, title: 'Easy, Fast, Secured', description: 'Book your tickets quickly and securely' },
    { icon: CreditCard, title: '100% Price Guaranteed', description: 'Best prices guaranteed on all routes' },
    { icon: CheckCircle, title: 'Board with E-Ticket or M-Ticket', description: 'Digital tickets accepted everywhere' },
    { icon: Headphones, title: 'Responsive Support Team', description: '24/7 customer support available' },
    { icon: Award, title: 'Book & Save Points for Rewards', description: 'Earn points with every booking' },
    { icon: Star, title: 'Review & Rate Operators', description: 'Help others with your experiences' },
    { icon: CardIcon, title: 'Pay with VISA, Master Card & more', description: 'Multiple payment options' },
    { icon: Navigation, title: 'Book Transportations & Activities in one place', description: 'Complete travel solutions' }
  ];

  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-6">
            <h2 className="text-3xl font-bold text-gray-800">Why buy tickets with us?</h2>
            <div className="space-y-4">
              {features.map((feature, index) => {
                const Icon = feature.icon;
                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-start space-x-3"
                  >
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                      <Icon className="w-4 h-4 text-green-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800">{feature.title}</h3>
                      <p className="text-gray-600 text-sm">{feature.description}</p>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </div>
          <div className="relative">
            <img 
              src="https://images.unsplash.com/photo-1615514659684-cece95b952f4"
              alt="Modern bus"
              className="w-full h-96 object-cover rounded-2xl shadow-lg"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent rounded-2xl" />
          </div>
        </div>
      </div>
    </section>
  );
};

// Popular Routes Component (same as before)
const PopularRoutes = () => {
  const [routes, setRoutes] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchPopularRoutes();
  }, []);

  const fetchPopularRoutes = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/popular-routes`);
      if (response.ok) {
        const data = await response.json();
        setRoutes(data);
      } else {
        // Fallback to static data if API fails
        setRoutes([
          {
            id: 1,
            title: 'BUS FROM PHNOM PENH TO SIHANOUKVILLE',
            description: 'Everybody knows about Sihanoukville. This is one of the most popular destinations in Cambodia because of its beautiful beaches and wonderful weather.',
            image: 'https://images.unsplash.com/photo-1655793488799-1ffba5b22cbd',
            price: '$12',
            duration: '4h 30m',
            origin: 'Phnom Penh',
            destination: 'Sihanoukville',
            popularity: 95
          },
          {
            id: 2,
            title: 'BUS FROM PHNOM PENH TO SIEM REAP',
            description: 'Exploring Siem Reap gives you a unique glimpse into Cambodia\'s history and culture. Visit some of the most famous temples in the world.',
            image: 'https://images.unsplash.com/photo-1549159939-085440a06624',
            price: '$15',
            duration: '5h 45m',
            origin: 'Phnom Penh',
            destination: 'Siem Reap',
            popularity: 92
          },
          {
            id: 3,
            title: 'BUS FROM SIHANOUKVILLE TO PHNOM PENH',
            description: 'Phnom Penh is the capital of Cambodia, and is situated where the three rivers meet: the Mekong River, Bassac, and Tonle Sap.',
            image: 'https://images.unsplash.com/photo-1566559631133-969041fc5583',
            price: '$12',
            duration: '4h 30m',
            origin: 'Sihanoukville',
            destination: 'Phnom Penh',
            popularity: 88
          },
          {
            id: 4,
            title: 'BUS FROM PHNOM PENH TO KAMPOT',
            description: 'Kampot is the place to visit in Cambodia if you are hungry for some adventures. It is also ideal for those who want to enjoy the French colonial architecture.',
            image: 'https://images.unsplash.com/photo-1549415714-23c875946516',
            price: '$8',
            duration: '3h 15m',
            origin: 'Phnom Penh',
            destination: 'Kampot',
            popularity: 82
          },
          {
            id: 5,
            title: 'BUS FROM SIEM REAP TO PHNOM PENH',
            description: 'Phnom Penh is the capital of Cambodia, and is situated where the three rivers meet: the Mekong River, Bassac, and Tonle Sap.',
            image: 'https://images.unsplash.com/photo-1662074442814-351f09894a05',
            price: '$15',
            duration: '5h 45m',
            origin: 'Siem Reap',
            destination: 'Phnom Penh',
            popularity: 90
          },
          {
            id: 6,
            title: 'BUS FROM PHNOM PENH TO BATTAMBANG',
            description: 'If you want to see another side of Cambodia, visit Battambang. This city is the second largest in the country and is definitely worth visiting.',
            image: 'https://images.unsplash.com/photo-1506721681159-78aeaf19a760',
            price: '$10',
            duration: '4h 00m',
            origin: 'Phnom Penh',
            destination: 'Battambang',
            popularity: 75
          }
        ]);
      }
    } catch (error) {
      console.error('Error fetching popular routes:', error);
      // Use fallback data
    } finally {
      setLoading(false);
    }
  };

  const handleQuickBook = (route) => {
    // Auto-fill search form and redirect
    const searchData = {
      origin: route.origin,
      destination: route.destination,
      date: new Date().toISOString().split('T')[0], // Today's date
      passengers: 1,
      transport_type: 'bus'
    };
    
    // Navigate to search with pre-filled data
    navigate('/', { state: { prefilledSearch: searchData } });
  };

  if (loading) {
    return (
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="flex justify-center items-center py-12">
            <Loader2 className="w-8 h-8 animate-spin text-orange-500" />
            <span className="ml-2 text-gray-600">Loading popular routes...</span>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">Popular Routes</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {routes.map((route, index) => (
            <motion.div
              key={route.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
            >
              <div className="relative h-48">
                <img 
                  src={route.image}
                  alt={route.title}
                  className="w-full h-full object-cover"
                />
                <div className="absolute top-4 right-4 bg-orange-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                  {route.price}
                </div>
                <div className="absolute bottom-4 left-4 bg-black/50 text-white px-3 py-1 rounded-full text-sm">
                  {route.duration}
                </div>
              </div>
              <div className="p-6">
                <h3 className="text-lg font-bold text-gray-800 mb-2">{route.title}</h3>
                <p className="text-gray-600 text-sm mb-4 line-clamp-3">{route.description}</p>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleQuickBook(route)}
                    className="flex-1 bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 transition-colors font-semibold"
                  >
                    Quick Book
                  </button>
                  <button
                    onClick={() => navigate('/', { state: { prefilledSearch: { origin: route.origin, destination: route.destination } } })}
                    className="flex-1 bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600 transition-colors"
                  >
                    View Details
                  </button>
                </div>
                {route.popularity && (
                  <div className="mt-2 flex items-center">
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="text-xs text-gray-600 ml-1">{route.popularity}% popularity</span>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// AI Features Section (same as before)
const AIFeaturesSection = () => {
  const aiFeatures = [
    {
      icon: Brain,
      title: 'AI-Powered Route Suggestions',
      description: 'Get personalized route recommendations based on your travel history and preferences',
      color: 'bg-blue-100 text-blue-600'
    },
    {
      icon: TrendingUp,
      title: 'Smart Price Prediction',
      description: 'AI analyzes market trends to predict the best times to book for maximum savings',
      color: 'bg-green-100 text-green-600'
    },
    {
      icon: Eye,
      title: 'Real-time Availability',
      description: 'Machine learning algorithms provide accurate real-time seat availability updates',
      color: 'bg-purple-100 text-purple-600'
    },
    {
      icon: MessageCircle,
      title: '24/7 AI Assistant',
      description: 'Get instant answers to your questions with our intelligent chatbot assistant',
      color: 'bg-orange-100 text-orange-600'
    },
    {
      icon: Smartphone,
      title: 'Smart Notifications',
      description: 'Receive intelligent alerts about delays, gate changes, and boarding updates',
      color: 'bg-red-100 text-red-600'
    },
    {
      icon: Globe,
      title: 'Multi-language Support',
      description: 'AI-powered translation supports multiple languages for seamless booking',
      color: 'bg-indigo-100 text-indigo-600'
    }
  ];

  return (
    <section className="py-16 bg-gradient-to-br from-gray-900 to-blue-900 text-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold mb-4">AI-Enhanced Travel Experience</h2>
          <p className="text-xl opacity-90">Experience the future of bus booking with our AI-powered features</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {aiFeatures.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 hover:bg-white/20 transition-all"
              >
                <div className={`w-12 h-12 rounded-full ${feature.color} flex items-center justify-center mb-4`}>
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-gray-300">{feature.description}</p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

// Partners and Testimonials sections (same as before)
const PartnersSection = () => {
  const partners = [
    'Partner 1', 'Partner 2', 'Partner 3', 'Partner 4', 'Partner 5', 'Partner 6',
    'Partner 7', 'Partner 8', 'Partner 9', 'Partner 10', 'Partner 11', 'Partner 12'
  ];

  return (
    <section className="py-16 bg-gray-100">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">Our Partners</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-8">
          {partners.map((partner, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.05 }}
              className="bg-white rounded-lg p-4 shadow-md hover:shadow-lg transition-shadow flex items-center justify-center h-20"
            >
              <div className="text-gray-400 text-sm font-medium">{partner}</div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

const TestimonialsSection = () => {
  const testimonials = [
    {
      name: 'Sarah Johnson',
      rating: 5,
      comment: 'I am very satisfied with booking with BusTicket. Very easy to use and the prices are competitive. Confirmation email was at their fastest.',
      avatar: 'https://images.unsplash.com/photo-1494790108755-2616b612e5c8?w=150&h=150&fit=crop&crop=face'
    },
    {
      name: 'Michael Chen',
      rating: 5,
      comment: 'Excellent service! The AI recommendations helped me find the perfect route and saved me money. The booking process was seamless.',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face'
    },
    {
      name: 'Emma Williams',
      rating: 5,
      comment: 'Love the real-time updates and smart notifications. Made my travel planning so much easier. Highly recommend!',
      avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face'
    }
  ];

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">What Our Customers Say</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
              className="bg-gray-50 rounded-2xl p-6 shadow-lg"
            >
              <div className="flex items-center mb-4">
                <img 
                  src={testimonial.avatar}
                  alt={testimonial.name}
                  className="w-12 h-12 rounded-full mr-4"
                />
                <div>
                  <h4 className="font-semibold text-gray-800">{testimonial.name}</h4>
                  <div className="flex items-center">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 text-yellow-400 fill-current" />
                    ))}
                  </div>
                </div>
              </div>
              <p className="text-gray-600 italic">"{testimonial.comment}"</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">BusTicket</h3>
            <p className="text-gray-400 mb-4">Your trusted partner for bus booking across Southeast Asia</p>
            <div className="flex space-x-4">
              <button className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700">
                <span className="text-sm">f</span>
              </button>
              <button className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700">
                <span className="text-sm">t</span>
              </button>
              <button className="w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center hover:bg-gray-700">
                <span className="text-sm">in</span>
              </button>
            </div>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">User</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white">Top Destinations</a></li>
              <li><a href="#" className="hover:text-white">Help</a></li>
              <li><a href="#" className="hover:text-white">Data Deletion</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">Partner</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white">List Property</a></li>
              <li><a href="#" className="hover:text-white">Partnerships</a></li>
              <li><a href="#" className="hover:text-white">Affiliate</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-semibold mb-4">App</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white">Download our iOS Android</a></li>
              <li><a href="#" className="hover:text-white">Operate our iOS Android</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 BusTicket. All rights reserved. | Enhanced with AI for better travel experience</p>
        </div>
      </div>
    </footer>
  );
};

// My Bookings Page
const MyBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/bookings`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setBookings(data);
      }
    } catch (error) {
      console.error('Error fetching bookings:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-orange-500" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">My Bookings</h1>
        
        {bookings.length === 0 ? (
          <div className="text-center py-16">
            <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No bookings found</p>
            <Link
              to="/"
              className="mt-4 inline-block bg-orange-500 text-white px-6 py-3 rounded-lg hover:bg-orange-600"
            >
              Book Your First Trip
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {bookings.map((booking) => (
              <div key={booking.id} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800">
                      {booking.route_details?.origin} → {booking.route_details?.destination}
                    </h3>
                    <p className="text-gray-600">Booking Reference: {booking.booking_reference}</p>
                  </div>
                  <div className="text-right">
                    <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                      booking.status === 'paid' ? 'bg-green-100 text-green-800' :
                      booking.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {booking.status.toUpperCase()}
                    </div>
                    <div className="text-xl font-bold text-orange-500 mt-2">
                      ${booking.total_price}
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                  <div>
                    <span className="font-medium">Date:</span> {booking.date}
                  </div>
                  <div>
                    <span className="font-medium">Seats:</span> {booking.seats.join(', ')}
                  </div>
                  <div>
                    <span className="font-medium">Duration:</span> {booking.route_details?.duration}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// Main Booking Page Component
const BookingPage = () => {
  const [currentStep, setCurrentStep] = useState('search');
  const [searchData, setSearchData] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [selectedRoute, setSelectedRoute] = useState(null);
  const [bookingData, setBookingData] = useState(null);
  const [paymentData, setPaymentData] = useState(null);
  const [activeTab, setActiveTab] = useState('bus');
  const [loading, setLoading] = useState(false);
  const { user, token } = useAuth();
  const navigate = useNavigate();

  const handleSearch = async (data) => {
    setSearchData(data);
    setLoading(true);
    
    try {
      console.log('Searching with data:', data);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });
      
      if (response.ok) {
        const results = await response.json();
        console.log('Search results:', results);
        setSearchResults(results);
        setCurrentStep('results');
      } else {
        throw new Error('Search failed');
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectRoute = async (route) => {
    console.log('Route selected:', route);
    
    // Check if user is authenticated for seat selection
    if (!user) {
      // Store route selection for after login
      sessionStorage.setItem('pendingRouteSelection', route.id);
      alert('Please login to continue booking');
      return;
    }
    
    try {
      console.log('Setting selected route:', route);
      setSelectedRoute(route);
      setCurrentStep('seats');
    } catch (error) {
      console.error('Error handling route selection:', error);
      alert('An error occurred while selecting the route. Please try again.');
    }
  };

  const handleConfirmBooking = async (bookingDetails) => {
    try {
      const { token } = useAuth();
      if (!token) {
        alert('Please login to continue');
        return;
      }
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/bookings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(bookingDetails)
      });

      if (response.ok) {
        const data = await response.json();
        setBookingData(data);
        setCurrentStep('payment');
      } else {
        const errorData = await response.json();
        alert(`Failed to create booking: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error creating booking:', error);
      alert('Network error occurred');
    }
  };

  const handlePaymentSuccess = (payment) => {
    setPaymentData(payment);
    setCurrentStep('confirmation');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      
      {currentStep === 'search' && (
        <>
          <SearchSection activeTab={activeTab} onSearch={handleSearch} />
          <div className="container mx-auto px-4">
            <QuickBuyWidget onQuickBook={(data) => handleSearch(data)} />
          </div>
          <FeaturesSection />
          <PopularRoutes />
          <AIFeaturesSection />
          <PartnersSection />
          <TestimonialsSection />
        </>
      )}

      {currentStep === 'results' && (
        <div className="container mx-auto px-4">
          <div className="py-8">
            <button
              onClick={() => setCurrentStep('search')}
              className="flex items-center text-orange-500 hover:text-orange-600 mb-6"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Back to Search
            </button>
          </div>
          <SearchResults 
            searchData={searchData} 
            searchResults={searchResults}
            loading={loading}
            onSelectRoute={handleSelectRoute} 
          />
        </div>
      )}

      {currentStep === 'seats' && (
        <div className="container mx-auto px-4">
          <div className="py-8">
            <button
              onClick={() => setCurrentStep('results')}
              className="flex items-center text-orange-500 hover:text-orange-600 mb-6"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Back to Results
            </button>
          </div>
          <SeatSelection 
            route={selectedRoute} 
            searchData={searchData} 
            onConfirmBooking={handleConfirmBooking} 
          />
        </div>
      )}

      {currentStep === 'payment' && (
        <div className="container mx-auto px-4">
          <div className="py-8">
            <button
              onClick={() => setCurrentStep('seats')}
              className="flex items-center text-orange-500 hover:text-orange-600 mb-6"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Back to Seat Selection
            </button>
          </div>
          <PaymentManagement 
            booking={bookingData} 
            onPaymentComplete={handlePaymentSuccess}
            onCancel={() => setCurrentStep('seats')}
          />
        </div>
      )}

      {currentStep === 'confirmation' && (
        <div className="container mx-auto px-4">
          <BookingConfirmation paymentData={paymentData} bookingData={bookingData} />
        </div>
      )}

      <Footer />
    </div>
  );
};

// Main App Component
function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<BookingPage />} />
          <Route path="/my-bookings" element={<MyBookings />} />
          <Route path="/management" element={<ManagementDashboard />} />
          <Route path="/admin" element={<AdminManagement />} />
          <Route path="/routes-management" element={<RouteManagement />} />
          <Route path="/agents-management" element={<AgentManagement />} />
          <Route path="/seats-management" element={<SmartSeatManagement />} />
          <Route path="/flight-operations" element={<FlightOperationManagement />} />
          <Route path="/taxi-operations" element={<TaxiOperationManagement />} />
          <Route path="/ferry-operations" element={<FerryOperationManagement />} />
          <Route path="/notifications" element={<SmartNotificationSystem />} />
          <Route path="/profile" element={<UserProfile />} />
          <Route path="/affiliate" element={<AffiliateProgram />} />
          <Route path="/affiliate-program" element={<AffiliateProgram />} />
          <Route path="/tickets" element={<TicketManagement />} />
          <Route path="/print-tickets" element={<TicketManagement />} />
          <Route path="/payment" element={<PaymentManagement />} />
          <Route path="/track/:bookingId" element={<SmartTrackingAI />} />
          <Route path="/tracking" element={<SmartTrackingAI />} />
          <Route path="/routes" element={<BookingPage />} />
          <Route path="/about" element={<BookingPage />} />
          <Route path="/contact" element={<BookingPage />} />
          <Route path="/search/bus/:origin/:destination" element={<BookingPage />} />
          <Route path="/search/ferry/:origin/:destination" element={<BookingPage />} />
          <Route path="/search/private_taxi/:origin/:destination" element={<BookingPage />} />
          <Route path="/search/airport_shuttle/:origin/:destination" element={<BookingPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;