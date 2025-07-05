import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Bell, 
  Clock, 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  Mail, 
  Smartphone, 
  Globe, 
  Settings, 
  X, 
  Volume2, 
  VolumeX, 
  Calendar, 
  MapPin, 
  Bus, 
  Users, 
  Zap, 
  Target, 
  Activity, 
  TrendingUp, 
  BarChart3, 
  Filter, 
  Search, 
  Trash2, 
  Eye, 
  EyeOff, 
  Download, 
  RefreshCw,
  Send,
  MessageSquare,
  Phone,
  Wifi,
  Battery,
  Signal
} from 'lucide-react';
import { useAuth } from './components';

// Smart Notification System with AI-powered alerts
export const SmartNotificationSystem = () => {
  const [notifications, setNotifications] = useState([]);
  const [settings, setSettings] = useState({
    push_notifications: true,
    email_notifications: true,
    sms_notifications: true,
    sound_enabled: true,
    trip_alerts: true,
    booking_alerts: true,
    payment_alerts: true,
    system_alerts: true,
    weather_alerts: true,
    traffic_alerts: true
  });
  const [schedules, setSchedules] = useState([]);
  const [showSettings, setShowSettings] = useState(false);
  const [filter, setFilter] = useState('all');
  const { user, token } = useAuth();

  // Simulate real-time notifications
  useEffect(() => {
    // Initialize with sample notifications
    const sampleNotifications = [
      {
        id: 1,
        type: 'trip_update',
        title: 'Bus Approaching Next Stop',
        message: 'Your bus to Siem Reap will arrive at Kampong Chhnang in 5 minutes',
        timestamp: new Date(),
        read: false,
        priority: 'high',
        actions: ['view_location', 'contact_driver'],
        data: { booking_id: 'BMB123456', eta: '5 minutes' }
      },
      {
        id: 2,
        type: 'schedule_reminder',
        title: 'Upcoming Trip Reminder',
        message: 'Your trip from Phnom Penh to Siem Reap is scheduled for tomorrow at 6:00 AM',
        timestamp: new Date(Date.now() - 3600000),
        read: false,
        priority: 'medium',
        actions: ['view_ticket', 'set_alarm'],
        data: { booking_id: 'BMB123457', departure_time: '06:00' }
      },
      {
        id: 3,
        type: 'payment_success',
        title: 'Payment Confirmed',
        message: 'Your payment of $15.00 has been successfully processed',
        timestamp: new Date(Date.now() - 7200000),
        read: true,
        priority: 'medium',
        actions: ['download_receipt', 'view_booking'],
        data: { amount: 15.00, transaction_id: 'TXN789' }
      },
      {
        id: 4,
        type: 'weather_alert',
        title: 'Weather Advisory',
        message: 'Heavy rain expected on your route. Departure may be delayed by 30 minutes',
        timestamp: new Date(Date.now() - 10800000),
        read: false,
        priority: 'high',
        actions: ['view_alternatives', 'contact_support'],
        data: { route: 'Phnom Penh → Siem Reap', delay: '30 minutes' }
      },
      {
        id: 5,
        type: 'promotion',
        title: 'Special Offer',
        message: 'Get 20% off your next booking! Use code SAVE20',
        timestamp: new Date(Date.now() - 14400000),
        read: false,
        priority: 'low',
        actions: ['use_code', 'book_now'],
        data: { code: 'SAVE20', discount: '20%' }
      }
    ];
    setNotifications(sampleNotifications);

    // Set up real-time notification polling
    const interval = setInterval(() => {
      // Simulate new notifications
      if (Math.random() > 0.7) {
        addNewNotification();
      }
    }, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const addNewNotification = () => {
    const newNotification = {
      id: Date.now(),
      type: 'trip_update',
      title: 'Live Update',
      message: 'Your bus is running 5 minutes ahead of schedule',
      timestamp: new Date(),
      read: false,
      priority: 'medium',
      actions: ['view_location'],
      data: { status: 'ahead_of_schedule' }
    };
    
    setNotifications(prev => [newNotification, ...prev]);
    
    // Play notification sound
    if (settings.sound_enabled) {
      playNotificationSound();
    }
    
    // Send push notification if enabled
    if (settings.push_notifications) {
      sendPushNotification(newNotification);
    }
  };

  const playNotificationSound = () => {
    // Create audio context for notification sound
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0, audioContext.currentTime);
    gainNode.gain.linearRampToValueAtTime(0.1, audioContext.currentTime + 0.1);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
  };

  const sendPushNotification = (notification) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(notification.title, {
        body: notification.message,
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        tag: notification.id.toString()
      });
    }
  };

  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      return permission === 'granted';
    }
    return false;
  };

  const markAsRead = (id) => {
    setNotifications(prev =>
      prev.map(notif =>
        notif.id === id ? { ...notif, read: true } : notif
      )
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev =>
      prev.map(notif => ({ ...notif, read: true }))
    );
  };

  const deleteNotification = (id) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  };

  const handleAction = (action, notification) => {
    switch (action) {
      case 'view_location':
        window.open(`/tracking/${notification.data.booking_id}`, '_blank');
        break;
      case 'contact_driver':
        alert('Contacting driver...');
        break;
      case 'view_ticket':
        window.open(`/tickets/${notification.data.booking_id}`, '_blank');
        break;
      case 'set_alarm':
        scheduleAlarmReminder(notification.data);
        break;
      case 'download_receipt':
        downloadReceipt(notification.data.transaction_id);
        break;
      case 'use_code':
        copyToClipboard(notification.data.code);
        break;
      default:
        console.log('Action not implemented:', action);
    }
    markAsRead(notification.id);
  };

  const scheduleAlarmReminder = (data) => {
    const alarmTime = new Date();
    alarmTime.setDate(alarmTime.getDate() + 1);
    alarmTime.setHours(5, 30, 0, 0); // 30 minutes before departure
    
    const newSchedule = {
      id: Date.now(),
      title: 'Trip Departure Reminder',
      time: alarmTime,
      type: 'trip_reminder',
      enabled: true,
      data
    };
    
    setSchedules(prev => [...prev, newSchedule]);
    alert('Alarm set for 30 minutes before departure');
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert(`Code "${text}" copied to clipboard!`);
  };

  const downloadReceipt = (transactionId) => {
    // Simulate receipt download
    alert(`Downloading receipt for transaction ${transactionId}`);
  };

  const filteredNotifications = notifications.filter(notif => {
    if (filter === 'all') return true;
    if (filter === 'unread') return !notif.read;
    return notif.type === filter;
  });

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'trip_update': return <Bus className="w-5 h-5" />;
      case 'schedule_reminder': return <Clock className="w-5 h-5" />;
      case 'payment_success': return <CheckCircle className="w-5 h-5" />;
      case 'weather_alert': return <AlertTriangle className="w-5 h-5" />;
      case 'promotion': return <Target className="w-5 h-5" />;
      default: return <Info className="w-5 h-5" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'border-l-red-500 bg-red-50';
      case 'medium': return 'border-l-orange-500 bg-orange-50';
      case 'low': return 'border-l-blue-500 bg-blue-50';
      default: return 'border-l-gray-500 bg-gray-50';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 flex items-center">
                <Bell className="w-8 h-8 mr-3 text-orange-500" />
                Smart Notifications & Alerts
              </h1>
              <p className="text-gray-600 mt-2">AI-powered notifications with smart scheduling and multi-channel alerts</p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setShowSettings(!showSettings)}
                className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 flex items-center"
              >
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </button>
              <button
                onClick={markAllAsRead}
                className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 flex items-center"
              >
                <CheckCircle className="w-4 h-4 mr-2" />
                Mark All Read
              </button>
            </div>
          </div>

          {/* Settings Panel */}
          <AnimatePresence>
            {showSettings && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-white rounded-lg shadow-md p-6 mb-8"
              >
                <h3 className="text-lg font-semibold mb-4">Notification Settings</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <div className="space-y-4">
                    <h4 className="font-medium text-gray-700">Delivery Channels</h4>
                    {[
                      { key: 'push_notifications', label: 'Push Notifications', icon: Bell },
                      { key: 'email_notifications', label: 'Email Alerts', icon: Mail },
                      { key: 'sms_notifications', label: 'SMS Alerts', icon: Smartphone }
                    ].map(({ key, label, icon: Icon }) => (
                      <label key={key} className="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          checked={settings[key]}
                          onChange={(e) => setSettings(prev => ({ ...prev, [key]: e.target.checked }))}
                          className="rounded"
                        />
                        <Icon className="w-4 h-4 text-gray-600" />
                        <span className="text-sm">{label}</span>
                      </label>
                    ))}
                  </div>

                  <div className="space-y-4">
                    <h4 className="font-medium text-gray-700">Alert Types</h4>
                    {[
                      { key: 'trip_alerts', label: 'Trip Updates' },
                      { key: 'booking_alerts', label: 'Booking Alerts' },
                      { key: 'payment_alerts', label: 'Payment Notifications' },
                      { key: 'system_alerts', label: 'System Updates' }
                    ].map(({ key, label }) => (
                      <label key={key} className="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          checked={settings[key]}
                          onChange={(e) => setSettings(prev => ({ ...prev, [key]: e.target.checked }))}
                          className="rounded"
                        />
                        <span className="text-sm">{label}</span>
                      </label>
                    ))}
                  </div>

                  <div className="space-y-4">
                    <h4 className="font-medium text-gray-700">Smart Alerts</h4>
                    {[
                      { key: 'weather_alerts', label: 'Weather Updates' },
                      { key: 'traffic_alerts', label: 'Traffic Conditions' },
                      { key: 'sound_enabled', label: 'Sound Notifications' }
                    ].map(({ key, label }) => (
                      <label key={key} className="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          checked={settings[key]}
                          onChange={(e) => setSettings(prev => ({ ...prev, [key]: e.target.checked }))}
                          className="rounded"
                        />
                        <span className="text-sm">{label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="mt-6 pt-6 border-t">
                  <button
                    onClick={requestNotificationPermission}
                    className="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 flex items-center"
                  >
                    <Bell className="w-4 h-4 mr-2" />
                    Enable Browser Notifications
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Filter Tabs */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex flex-wrap gap-2">
              {[
                { key: 'all', label: 'All', count: notifications.length },
                { key: 'unread', label: 'Unread', count: notifications.filter(n => !n.read).length },
                { key: 'trip_update', label: 'Trip Updates', count: notifications.filter(n => n.type === 'trip_update').length },
                { key: 'schedule_reminder', label: 'Reminders', count: notifications.filter(n => n.type === 'schedule_reminder').length },
                { key: 'payment_success', label: 'Payments', count: notifications.filter(n => n.type === 'payment_success').length }
              ].map(({ key, label, count }) => (
                <button
                  key={key}
                  onClick={() => setFilter(key)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    filter === key
                      ? 'bg-orange-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {label} {count > 0 && `(${count})`}
                </button>
              ))}
            </div>
          </div>

          {/* Notifications List */}
          <div className="space-y-4">
            {filteredNotifications.length === 0 ? (
              <div className="bg-white rounded-lg shadow-md p-8 text-center">
                <Bell className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-700 mb-2">No notifications</h3>
                <p className="text-gray-600">You're all caught up! No {filter !== 'all' ? filter : ''} notifications to show.</p>
              </div>
            ) : (
              filteredNotifications.map((notification) => (
                <motion.div
                  key={notification.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className={`bg-white rounded-lg shadow-md p-6 border-l-4 ${getPriorityColor(notification.priority)} ${
                    !notification.read ? 'ring-2 ring-orange-200' : ''
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-4">
                      <div className={`p-2 rounded-lg ${
                        notification.priority === 'high' ? 'bg-red-100 text-red-600' :
                        notification.priority === 'medium' ? 'bg-orange-100 text-orange-600' :
                        'bg-blue-100 text-blue-600'
                      }`}>
                        {getNotificationIcon(notification.type)}
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h4 className="font-semibold text-gray-800">{notification.title}</h4>
                          {!notification.read && (
                            <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                          )}
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            notification.priority === 'high' ? 'bg-red-100 text-red-800' :
                            notification.priority === 'medium' ? 'bg-orange-100 text-orange-800' :
                            'bg-blue-100 text-blue-800'
                          }`}>
                            {notification.priority.toUpperCase()}
                          </span>
                        </div>
                        
                        <p className="text-gray-600 mb-3">{notification.message}</p>
                        
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-500">
                            {notification.timestamp.toLocaleString()}
                          </span>
                          
                          {notification.actions && notification.actions.length > 0 && (
                            <div className="flex space-x-2">
                              {notification.actions.map((action) => (
                                <button
                                  key={action}
                                  onClick={() => handleAction(action, notification)}
                                  className="bg-orange-500 text-white px-3 py-1 rounded text-xs hover:bg-orange-600 transition-colors"
                                >
                                  {action.replace('_', ' ').toUpperCase()}
                                </button>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex space-x-2">
                      {!notification.read && (
                        <button
                          onClick={() => markAsRead(notification.id)}
                          className="text-gray-400 hover:text-green-600"
                          title="Mark as read"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                      )}
                      <button
                        onClick={() => deleteNotification(notification.id)}
                        className="text-gray-400 hover:text-red-600"
                        title="Delete notification"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))
            )}
          </div>

          {/* Scheduled Reminders */}
          {schedules.length > 0 && (
            <div className="mt-8">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Scheduled Reminders</h3>
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="space-y-4">
                  {schedules.map((schedule) => (
                    <div key={schedule.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Clock className="w-5 h-5 text-blue-600" />
                        <div>
                          <div className="font-medium">{schedule.title}</div>
                          <div className="text-sm text-gray-600">
                            {schedule.time.toLocaleString()}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={schedule.enabled}
                            onChange={(e) => setSchedules(prev =>
                              prev.map(s => s.id === schedule.id ? { ...s, enabled: e.target.checked } : s)
                            )}
                            className="rounded"
                          />
                          <span className="ml-2 text-sm">Enabled</span>
                        </label>
                        <button
                          onClick={() => setSchedules(prev => prev.filter(s => s.id !== schedule.id))}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};