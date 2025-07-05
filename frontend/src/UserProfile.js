import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  User, 
  CreditCard, 
  Calendar, 
  Clock, 
  MapPin, 
  Mail, 
  Phone, 
  Edit2, 
  Save, 
  X, 
  Download, 
  Share, 
  Copy, 
  Gift, 
  Users as UsersIcon, 
  Link as LinkIcon,
  Code,
  Printer,
  Send,
  Key,
  DollarSign,
  Star,
  Loader2,
  CheckCircle,
  AlertCircle,
  Eye,
  EyeOff
} from 'lucide-react';
import { useAuth } from './components';

// BMB Credit Component
const BMBCredit = () => {
  const [creditBalance, setCreditBalance] = useState(0);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();

  useEffect(() => {
    fetchCreditData();
  }, []);

  const fetchCreditData = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/user/credit`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setCreditBalance(data.balance);
        setTransactions(data.transactions || []);
      }
    } catch (error) {
      console.error('Error fetching credit data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center py-8"><Loader2 className="w-6 h-6 animate-spin" /></div>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-orange-500 to-red-600 rounded-lg p-6 text-white">
        <h3 className="text-xl font-bold mb-2">BMB Credit Balance</h3>
        <div className="text-3xl font-bold">${creditBalance}</div>
        <p className="text-orange-100 mt-2">Use credits for discounts on your next booking</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h4 className="text-lg font-semibold mb-4">Recent Transactions</h4>
        {transactions.length === 0 ? (
          <p className="text-gray-600">No transactions yet</p>
        ) : (
          <div className="space-y-3">
            {transactions.map((transaction, index) => (
              <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <div>
                  <div className="font-medium">{transaction.description}</div>
                  <div className="text-sm text-gray-600">{transaction.date}</div>
                </div>
                <div className={`font-bold ${transaction.amount > 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {transaction.amount > 0 ? '+' : ''}${transaction.amount}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// Upcoming Bookings Component
const UpcomingBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();

  useEffect(() => {
    fetchUpcomingBookings();
  }, []);

  const fetchUpcomingBookings = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/bookings/upcoming`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setBookings(data);
      }
    } catch (error) {
      console.error('Error fetching upcoming bookings:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center py-8"><Loader2 className="w-6 h-6 animate-spin" /></div>;
  }

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold">Upcoming Bookings</h3>
      {bookings.length === 0 ? (
        <div className="text-center py-8">
          <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No upcoming bookings</p>
        </div>
      ) : (
        bookings.map((booking) => (
          <motion.div
            key={booking.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <h4 className="text-lg font-semibold">{booking.route_details?.origin} → {booking.route_details?.destination}</h4>
                <p className="text-gray-600">Booking #{booking.booking_reference}</p>
              </div>
              <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                {booking.status}
              </span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <div className="text-gray-600">Date</div>
                <div className="font-medium">{booking.date}</div>
              </div>
              <div>
                <div className="text-gray-600">Seats</div>
                <div className="font-medium">{booking.seats.join(', ')}</div>
              </div>
              <div>
                <div className="text-gray-600">Duration</div>
                <div className="font-medium">{booking.route_details?.duration}</div>
              </div>
              <div>
                <div className="text-gray-600">Total</div>
                <div className="font-medium text-orange-600">${booking.total_price}</div>
              </div>
            </div>
            <div className="flex space-x-2 mt-4">
              <button className="bg-orange-500 text-white px-4 py-2 rounded hover:bg-orange-600 text-sm">
                View Details
              </button>
              <button className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 text-sm">
                Cancel Booking
              </button>
            </div>
          </motion.div>
        ))
      )}
    </div>
  );
};

// Past Bookings Component
const PastBookings = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuth();

  useEffect(() => {
    fetchPastBookings();
  }, []);

  const fetchPastBookings = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/bookings/past`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setBookings(data);
      }
    } catch (error) {
      console.error('Error fetching past bookings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRateBooking = (bookingId) => {
    // Implement rating functionality
    console.log('Rate booking:', bookingId);
  };

  if (loading) {
    return <div className="flex justify-center py-8"><Loader2 className="w-6 h-6 animate-spin" /></div>;
  }

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold">Past Bookings</h3>
      {bookings.length === 0 ? (
        <div className="text-center py-8">
          <Clock className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No past bookings</p>
        </div>
      ) : (
        bookings.map((booking) => (
          <motion.div
            key={booking.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg shadow-md p-6"
          >
            <div className="flex justify-between items-start mb-4">
              <div>
                <h4 className="text-lg font-semibold">{booking.route_details?.origin} → {booking.route_details?.destination}</h4>
                <p className="text-gray-600">Booking #{booking.booking_reference}</p>
              </div>
              <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm font-medium">
                Completed
              </span>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
              <div>
                <div className="text-gray-600">Date</div>
                <div className="font-medium">{booking.date}</div>
              </div>
              <div>
                <div className="text-gray-600">Seats</div>
                <div className="font-medium">{booking.seats.join(', ')}</div>
              </div>
              <div>
                <div className="text-gray-600">Duration</div>
                <div className="font-medium">{booking.route_details?.duration}</div>
              </div>
              <div>
                <div className="text-gray-600">Total</div>
                <div className="font-medium text-orange-600">${booking.total_price}</div>
              </div>
            </div>
            <div className="flex space-x-2">
              <button 
                onClick={() => handleRateBooking(booking.id)}
                className="bg-orange-500 text-white px-4 py-2 rounded hover:bg-orange-600 text-sm flex items-center"
              >
                <Star className="w-4 h-4 mr-1" />
                Rate Trip
              </button>
              <button className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600 text-sm">
                Download Receipt
              </button>
            </div>
          </motion.div>
        ))
      )}
    </div>
  );
};

// Invite Component
const InviteSection = () => {
  const [inviteCode, setInviteCode] = useState('BMB2025USER123');
  const [invitesSent, setInvitesSent] = useState(0);
  const [creditsEarned, setCreditsEarned] = useState(0);
  const [email, setEmail] = useState('');
  const [sending, setSending] = useState(false);

  const copyInviteCode = () => {
    navigator.clipboard.writeText(inviteCode);
    alert('Invite code copied to clipboard!');
  };

  const sendInvite = async () => {
    if (!email) {
      alert('Please enter an email address');
      return;
    }
    
    setSending(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/user/invite`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ email, invite_code: inviteCode })
      });
      
      if (response.ok) {
        alert('Invite sent successfully!');
        setEmail('');
        setInvitesSent(prev => prev + 1);
      }
    } catch (error) {
      alert('Failed to send invite');
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="space-y-6">
      <h3 className="text-xl font-bold">Invite Friends & Earn Credits</h3>
      
      <div className="bg-gradient-to-r from-green-500 to-blue-600 rounded-lg p-6 text-white">
        <h4 className="text-lg font-bold mb-2">Your Invite Code</h4>
        <div className="flex items-center space-x-2">
          <code className="bg-white bg-opacity-20 px-3 py-2 rounded font-mono text-lg">
            {inviteCode}
          </code>
          <button
            onClick={copyInviteCode}
            className="bg-white bg-opacity-20 p-2 rounded hover:bg-opacity-30"
          >
            <Copy className="w-5 h-5" />
          </button>
        </div>
        <p className="text-green-100 mt-2">Share this code and earn $5 for each successful signup!</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="text-2xl font-bold text-orange-600">{invitesSent}</div>
          <div className="text-gray-600">Invites Sent</div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="text-2xl font-bold text-green-600">${creditsEarned}</div>
          <div className="text-gray-600">Credits Earned</div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h4 className="text-lg font-semibold mb-4">Send Invite via Email</h4>
        <div className="flex space-x-2">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter friend's email address"
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
          />
          <button
            onClick={sendInvite}
            disabled={sending}
            className="bg-orange-500 text-white px-6 py-2 rounded-lg hover:bg-orange-600 disabled:opacity-50 flex items-center"
          >
            {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
            {sending ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

// Account Settings Component
const AccountSettings = () => {
  const { user } = useAuth();
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    phone: user?.phone || ''
  });
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/user/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        alert('Profile updated successfully!');
        setEditing(false);
      }
    } catch (error) {
      alert('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-xl font-bold">Account Settings</h3>
        {!editing ? (
          <button
            onClick={() => setEditing(true)}
            className="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 flex items-center"
          >
            <Edit2 className="w-4 h-4 mr-2" />
            Edit Profile
          </button>
        ) : (
          <div className="flex space-x-2">
            <button
              onClick={handleSave}
              disabled={saving}
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 flex items-center"
            >
              {saving ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Save className="w-4 h-4 mr-2" />}
              {saving ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={() => {
                setEditing(false);
                setFormData({
                  first_name: user?.first_name || '',
                  last_name: user?.last_name || '',
                  email: user?.email || '',
                  phone: user?.phone || ''
                });
              }}
              className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 flex items-center"
            >
              <X className="w-4 h-4 mr-2" />
              Cancel
            </button>
          </div>
        )}
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
            {editing ? (
              <input
                type="text"
                value={formData.first_name}
                onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              />
            ) : (
              <div className="px-3 py-2 bg-gray-50 rounded-lg">{formData.first_name}</div>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
            {editing ? (
              <input
                type="text"
                value={formData.last_name}
                onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              />
            ) : (
              <div className="px-3 py-2 bg-gray-50 rounded-lg">{formData.last_name}</div>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            {editing ? (
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              />
            ) : (
              <div className="px-3 py-2 bg-gray-50 rounded-lg">{formData.email}</div>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
            {editing ? (
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({...formData, phone: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
              />
            ) : (
              <div className="px-3 py-2 bg-gray-50 rounded-lg">{formData.phone}</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Change Password Component
const ChangePassword = () => {
  const [formData, setFormData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.newPassword !== formData.confirmPassword) {
      alert('New passwords do not match');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/user/change-password`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          current_password: formData.currentPassword,
          new_password: formData.newPassword
        })
      });
      
      if (response.ok) {
        alert('Password changed successfully!');
        setFormData({ currentPassword: '', newPassword: '', confirmPassword: '' });
      } else {
        alert('Failed to change password');
      }
    } catch (error) {
      alert('Network error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h3 className="text-xl font-bold">Change Password</h3>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
            <div className="relative">
              <input
                type={showPasswords.current ? 'text' : 'password'}
                value={formData.currentPassword}
                onChange={(e) => setFormData({...formData, currentPassword: e.target.value})}
                className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                required
              />
              <button
                type="button"
                onClick={() => setShowPasswords({...showPasswords, current: !showPasswords.current})}
                className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
              >
                {showPasswords.current ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">New Password</label>
            <div className="relative">
              <input
                type={showPasswords.new ? 'text' : 'password'}
                value={formData.newPassword}
                onChange={(e) => setFormData({...formData, newPassword: e.target.value})}
                className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                required
              />
              <button
                type="button"
                onClick={() => setShowPasswords({...showPasswords, new: !showPasswords.new})}
                className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
              >
                {showPasswords.new ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
            <div className="relative">
              <input
                type={showPasswords.confirm ? 'text' : 'password'}
                value={formData.confirmPassword}
                onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                className="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                required
              />
              <button
                type="button"
                onClick={() => setShowPasswords({...showPasswords, confirm: !showPasswords.confirm})}
                className="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600"
              >
                {showPasswords.confirm ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 disabled:opacity-50 flex items-center justify-center"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin mr-2" /> : <Key className="w-5 h-5 mr-2" />}
            {loading ? 'Changing Password...' : 'Change Password'}
          </button>
        </form>
      </div>
    </div>
  );
};

// Embed Widget Component
const EmbedWidget = () => {
  const [widgetCode] = useState(`<iframe src="https://463918e2-1f42-4cce-be47-8127013d3681.preview.emergentagent.com/widget" width="400" height="600" frameborder="0"></iframe>`);
  const [copied, setCopied] = useState(false);

  const copyWidgetCode = () => {
    navigator.clipboard.writeText(widgetCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <h3 className="text-xl font-bold">Embed Widget</h3>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <h4 className="text-lg font-semibold mb-4">Add BusTicket search to your website</h4>
        <p className="text-gray-600 mb-4">
          Copy and paste this code into your website to add a bus booking widget.
        </p>
        
        <div className="bg-gray-50 rounded-lg p-4 mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Widget Code</span>
            <button
              onClick={copyWidgetCode}
              className="bg-orange-500 text-white px-3 py-1 rounded text-sm hover:bg-orange-600 flex items-center"
            >
              {copied ? <CheckCircle className="w-4 h-4 mr-1" /> : <Copy className="w-4 h-4 mr-1" />}
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <code className="text-sm text-gray-800 break-all">{widgetCode}</code>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h5 className="font-semibold text-blue-800 mb-2">Widget Features:</h5>
          <ul className="text-blue-700 text-sm space-y-1">
            <li>• Complete bus search functionality</li>
            <li>• Responsive design that fits any website</li>
            <li>• Secure booking process</li>
            <li>• Real-time availability</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

// Banner Link Component
const BannerLink = () => {
  const [bannerCode] = useState(`<a href="https://463918e2-1f42-4cce-be47-8127013d3681.preview.emergentagent.com"><img src="https://463918e2-1f42-4cce-be47-8127013d3681.preview.emergentagent.com/banner.png" alt="Book Bus Tickets" /></a>`);
  const [copied, setCopied] = useState(false);

  const copyBannerCode = () => {
    navigator.clipboard.writeText(bannerCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <h3 className="text-xl font-bold">Banner Link</h3>
      
      <div className="bg-white rounded-lg shadow-md p-6">
        <h4 className="text-lg font-semibold mb-4">Promote BusTicket on your website</h4>
        <p className="text-gray-600 mb-4">
          Use our banner to promote bus booking services and earn affiliate commissions.
        </p>
        
        <div className="bg-gradient-to-r from-orange-500 to-red-600 rounded-lg p-4 mb-4">
          <img 
            src="https://via.placeholder.com/400x100/FF6B35/FFFFFF?text=BusTicket+-+Book+Your+Journey" 
            alt="BusTicket Banner" 
            className="w-full rounded"
          />
        </div>

        <div className="bg-gray-50 rounded-lg p-4 mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Banner Code</span>
            <button
              onClick={copyBannerCode}
              className="bg-orange-500 text-white px-3 py-1 rounded text-sm hover:bg-orange-600 flex items-center"
            >
              {copied ? <CheckCircle className="w-4 h-4 mr-1" /> : <Copy className="w-4 h-4 mr-1" />}
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <code className="text-sm text-gray-800 break-all">{bannerCode}</code>
        </div>
      </div>
    </div>
  );
};

// Main User Profile Component
export const UserProfile = () => {
  const [activeTab, setActiveTab] = useState('bmb-credit');
  const { user } = useAuth();

  const tabs = [
    { id: 'bmb-credit', label: 'BMB Credit', icon: CreditCard },
    { id: 'upcoming-booking', label: 'Upcoming Bookings', icon: Calendar },
    { id: 'past-booking', label: 'Past Bookings', icon: Clock },
    { id: 'invite', label: 'Invite Friends', icon: Gift },
    { id: 'account', label: 'Account Settings', icon: User },
    { id: 'change-password', label: 'Change Password', icon: Key },
    { id: 'embed-widget', label: 'Embed Widget', icon: Code },
    { id: 'banner-link', label: 'Banner Link', icon: LinkIcon }
  ];

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800">User Profile</h1>
          <p className="text-gray-600">Welcome back, {user?.first_name}!</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="text-center mb-6">
                <div className="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <User className="w-10 h-10 text-orange-600" />
                </div>
                <h3 className="text-xl font-semibold">{user?.first_name} {user?.last_name}</h3>
                <p className="text-gray-600">{user?.email}</p>
              </div>

              <nav className="space-y-2">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                        activeTab === tab.id
                          ? 'bg-orange-100 text-orange-700 border-orange-200'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span>{tab.label}</span>
                    </button>
                  );
                })}
              </nav>
            </div>
          </div>

          {/* Content */}
          <div className="lg:col-span-3">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
            >
              {activeTab === 'bmb-credit' && <BMBCredit />}
              {activeTab === 'upcoming-booking' && <UpcomingBookings />}
              {activeTab === 'past-booking' && <PastBookings />}
              {activeTab === 'invite' && <InviteSection />}
              {activeTab === 'account' && <AccountSettings />}
              {activeTab === 'change-password' && <ChangePassword />}
              {activeTab === 'embed-widget' && <EmbedWidget />}
              {activeTab === 'banner-link' && <BannerLink />}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};