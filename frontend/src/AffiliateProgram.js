import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  DollarSign, 
  Users, 
  TrendingUp, 
  Gift, 
  Copy, 
  Download, 
  BarChart3, 
  Calendar,
  Link as LinkIcon,
  Mail,
  Phone,
  Globe,
  CheckCircle,
  AlertCircle,
  Loader2,
  Star,
  Award,
  Target,
  CreditCard,
  ArrowRight
} from 'lucide-react';
import { useAuth } from './components';

// Affiliate Dashboard Stats
const AffiliateStats = ({ stats }) => {
  const statCards = [
    {
      title: 'Total Earnings',
      value: `$${stats.totalEarnings || 0}`,
      icon: DollarSign,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Referrals',
      value: stats.totalReferrals || 0,
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Conversion Rate',
      value: `${stats.conversionRate || 0}%`,
      icon: TrendingUp,
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    },
    {
      title: 'This Month',
      value: `$${stats.monthlyEarnings || 0}`,
      icon: Calendar,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {statCards.map((card, index) => {
        const Icon = card.icon;
        return (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">{card.title}</p>
                <p className="text-2xl font-bold text-gray-800">{card.value}</p>
              </div>
              <div className={`${card.bgColor} p-3 rounded-lg`}>
                <Icon className={`w-6 h-6 ${card.color}`} />
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};

// Affiliate Registration Form
const AffiliateRegistrationForm = ({ onRegistrationSuccess }) => {
  const [formData, setFormData] = useState({
    companyName: '',
    website: '',
    description: '',
    monthlySales: '',
    marketingChannels: [],
    agreeToTerms: false
  });
  const [loading, setLoading] = useState(false);
  const { user, token } = useAuth();

  const marketingChannelOptions = [
    'Website', 'Social Media', 'Email Marketing', 'Paid Advertising', 
    'Content Marketing', 'YouTube', 'Influencer Marketing', 'Other'
  ];

  const handleChannelChange = (channel) => {
    setFormData(prev => ({
      ...prev,
      marketingChannels: prev.marketingChannels.includes(channel)
        ? prev.marketingChannels.filter(c => c !== channel)
        : [...prev.marketingChannels, channel]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.agreeToTerms) {
      alert('Please agree to the terms and conditions');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/affiliate/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        onRegistrationSuccess(data);
        alert('Affiliate registration successful!');
      } else {
        alert('Registration failed. Please try again.');
      }
    } catch (error) {
      alert('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Join Our Affiliate Program</h2>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Company/Business Name</label>
            <input
              type="text"
              value={formData.companyName}
              onChange={(e) => setFormData({...formData, companyName: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Website URL</label>
            <input
              type="url"
              value={formData.website}
              onChange={(e) => setFormData({...formData, website: e.target.value})}
              placeholder="https://example.com"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Business Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              placeholder="Tell us about your business and how you plan to promote our services..."
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Estimated Monthly Sales</label>
            <select
              value={formData.monthlySales}
              onChange={(e) => setFormData({...formData, monthlySales: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              required
            >
              <option value="">Select range</option>
              <option value="0-1000">$0 - $1,000</option>
              <option value="1000-5000">$1,000 - $5,000</option>
              <option value="5000-10000">$5,000 - $10,000</option>
              <option value="10000+">$10,000+</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Marketing Channels</label>
            <div className="grid grid-cols-2 gap-2">
              {marketingChannelOptions.map((channel) => (
                <label key={channel} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.marketingChannels.includes(channel)}
                    onChange={() => handleChannelChange(channel)}
                    className="mr-2"
                  />
                  <span className="text-sm">{channel}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              checked={formData.agreeToTerms}
              onChange={(e) => setFormData({...formData, agreeToTerms: e.target.checked})}
              className="mr-2"
              required
            />
            <label className="text-sm text-gray-700">
              I agree to the <a href="#" className="text-orange-500 hover:text-orange-600">Terms and Conditions</a> and <a href="#" className="text-orange-500 hover:text-orange-600">Privacy Policy</a>
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-500 text-white py-3 px-4 rounded-lg hover:bg-orange-600 disabled:opacity-50 flex items-center justify-center"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin mr-2" /> : <CheckCircle className="w-5 h-5 mr-2" />}
            {loading ? 'Submitting...' : 'Submit Application'}
          </button>
        </form>
      </div>
    </div>
  );
};

// Affiliate Dashboard
const AffiliateDashboard = ({ affiliateData }) => {
  const [stats, setStats] = useState({});
  const [recentActivity, setRecentActivity] = useState([]);
  const [affiliateLinks, setAffiliateLinks] = useState([]);
  const { token } = useAuth();

  useEffect(() => {
    fetchAffiliateStats();
    fetchRecentActivity();
    fetchAffiliateLinks();
  }, []);

  const fetchAffiliateStats = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/affiliate/stats`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error('Error fetching affiliate stats:', error);
    }
  };

  const fetchRecentActivity = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/affiliate/activity`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setRecentActivity(data);
      }
    } catch (error) {
      console.error('Error fetching activity:', error);
    }
  };

  const fetchAffiliateLinks = async () => {
    const links = [
      { id: 1, name: 'Homepage', url: `https://463918e2-1f42-4cce-be47-8127013d3681.preview.emergentagent.com?ref=${affiliateData.affiliateCode}`, clicks: 45 },
      { id: 2, name: 'Search Bus', url: `https://463918e2-1f42-4cce-be47-8127013d3681.preview.emergentagent.com/search/bus?ref=${affiliateData.affiliateCode}`, clicks: 32 },
      { id: 3, name: 'Ferry Booking', url: `https://463918e2-1f42-4cce-be47-8127013d3681.preview.emergentagent.com/search/ferry?ref=${affiliateData.affiliateCode}`, clicks: 18 }
    ];
    setAffiliateLinks(links);
  };

  const copyLink = (url) => {
    navigator.clipboard.writeText(url);
    alert('Link copied to clipboard!');
  };

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Affiliate Dashboard</h2>
          <p className="text-gray-600">Track your performance and earnings</p>
        </div>
        <div className="bg-orange-100 px-4 py-2 rounded-lg">
          <span className="text-orange-800 font-medium">Affiliate ID: {affiliateData.affiliateCode}</span>
        </div>
      </div>

      <AffiliateStats stats={stats} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Affiliate Links */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Your Affiliate Links</h3>
          <div className="space-y-4">
            {affiliateLinks.map((link) => (
              <div key={link.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-medium">{link.name}</h4>
                  <span className="text-sm text-gray-600">{link.clicks} clicks</span>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={link.url}
                    readOnly
                    className="flex-1 px-3 py-2 bg-gray-50 border border-gray-300 rounded text-sm"
                  />
                  <button
                    onClick={() => copyLink(link.url)}
                    className="bg-orange-500 text-white p-2 rounded hover:bg-orange-600"
                  >
                    <Copy className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
          {recentActivity.length === 0 ? (
            <p className="text-gray-600">No recent activity</p>
          ) : (
            <div className="space-y-3">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <div className="flex-1">
                    <p className="text-sm font-medium">{activity.description}</p>
                    <p className="text-xs text-gray-600">{activity.date}</p>
                  </div>
                  <span className="text-sm font-medium text-green-600">+${activity.commission}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Commission Structure */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold mb-4">Commission Structure</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 border border-gray-200 rounded-lg">
            <Target className="w-8 h-8 text-orange-500 mx-auto mb-2" />
            <h4 className="font-semibold">Bus Bookings</h4>
            <p className="text-2xl font-bold text-orange-600">5%</p>
            <p className="text-sm text-gray-600">Per completed booking</p>
          </div>
          <div className="text-center p-4 border border-gray-200 rounded-lg">
            <Award className="w-8 h-8 text-blue-500 mx-auto mb-2" />
            <h4 className="font-semibold">Ferry Bookings</h4>
            <p className="text-2xl font-bold text-blue-600">7%</p>
            <p className="text-sm text-gray-600">Per completed booking</p>
          </div>
          <div className="text-center p-4 border border-gray-200 rounded-lg">
            <Star className="w-8 h-8 text-purple-500 mx-auto mb-2" />
            <h4 className="font-semibold">Referral Signup</h4>
            <p className="text-2xl font-bold text-purple-600">$10</p>
            <p className="text-sm text-gray-600">Per new user signup</p>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main Affiliate Program Component
export const AffiliateProgram = () => {
  const [isAffiliate, setIsAffiliate] = useState(false);
  const [affiliateData, setAffiliateData] = useState(null);
  const [loading, setLoading] = useState(true);
  const { user, token } = useAuth();

  useEffect(() => {
    checkAffiliateStatus();
  }, []);

  const checkAffiliateStatus = async () => {
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/affiliate/status`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setIsAffiliate(data.isAffiliate);
        setAffiliateData(data.affiliateData);
      }
    } catch (error) {
      console.error('Error checking affiliate status:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRegistrationSuccess = (data) => {
    setIsAffiliate(true);
    setAffiliateData(data);
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
        {!user ? (
          // Not logged in
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl font-bold text-gray-800 mb-6">Join Our Affiliate Program</h1>
            <p className="text-xl text-gray-600 mb-8">Earn money by promoting BusTicket services</p>
            
            <div className="bg-white rounded-lg shadow-md p-8 mb-8">
              <h2 className="text-2xl font-bold mb-6">Why Join Our Affiliate Program?</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <DollarSign className="w-12 h-12 text-green-500 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">High Commissions</h3>
                  <p className="text-gray-600">Earn up to 7% commission on every booking plus $10 for each referral signup</p>
                </div>
                <div className="text-center">
                  <TrendingUp className="w-12 h-12 text-blue-500 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Growing Market</h3>
                  <p className="text-gray-600">Join the growing online travel booking industry with increasing demand</p>
                </div>
                <div className="text-center">
                  <Award className="w-12 h-12 text-purple-500 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Marketing Support</h3>
                  <p className="text-gray-600">Get access to banners, widgets, and marketing materials to boost your success</p>
                </div>
              </div>
            </div>

            <div className="bg-orange-500 text-white rounded-lg p-6">
              <h3 className="text-xl font-bold mb-2">Ready to Start Earning?</h3>
              <p className="mb-4">Create an account and apply for our affiliate program today!</p>
              <button className="bg-white text-orange-500 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100">
                Sign Up Now
              </button>
            </div>
          </div>
        ) : !isAffiliate ? (
          // Logged in but not an affiliate
          <AffiliateRegistrationForm onRegistrationSuccess={handleRegistrationSuccess} />
        ) : (
          // Affiliate dashboard
          <AffiliateDashboard affiliateData={affiliateData} />
        )}
      </div>
    </div>
  );
};