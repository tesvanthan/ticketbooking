import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Download, 
  Send, 
  Mail, 
  Printer, 
  QrCode, 
  Calendar, 
  MapPin, 
  Clock, 
  Users, 
  Bus,
  CheckCircle,
  AlertCircle,
  Loader2,
  FileText,
  Share2,
  Smartphone,
  Globe,
  Copy,
  Eye
} from 'lucide-react';
import { useAuth } from './components';

// QR Code Component (using a placeholder for now)
const QRCodeComponent = ({ value, size = 200 }) => {
  return (
    <div 
      className="border border-gray-300 flex items-center justify-center bg-gray-50"
      style={{ width: size, height: size }}
    >
      <div className="text-center">
        <QrCode className="w-12 h-12 text-gray-400 mx-auto mb-2" />
        <div className="text-xs text-gray-600 break-all px-2">{value}</div>
      </div>
    </div>
  );
};

// Individual Ticket Component
const TicketCard = ({ booking, onPrint, onSend, onDownload }) => {
  const [showQR, setShowQR] = useState(false);
  
  const qrValue = `BMB-${booking.booking_reference}-${booking.id}`;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-md overflow-hidden"
    >
      {/* Ticket Header */}
      <div className="bg-gradient-to-r from-orange-500 to-red-600 text-white p-6">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-xl font-bold">BusTicket</h3>
            <p className="text-orange-100">E-Ticket</p>
          </div>
          <div className="text-right">
            <div className="text-sm opacity-90">Booking Reference</div>
            <div className="text-lg font-bold">{booking.booking_reference}</div>
          </div>
        </div>
      </div>

      {/* Route Information */}
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-800">{booking.departure_time || '06:00'}</div>
            <div className="text-gray-600">{booking.route_details?.origin || 'Phnom Penh'}</div>
          </div>
          <div className="flex-1 flex items-center mx-6">
            <div className="h-px bg-gray-300 flex-1"></div>
            <Bus className="w-6 h-6 text-orange-500 mx-4" />
            <div className="h-px bg-gray-300 flex-1"></div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-gray-800">{booking.arrival_time || '11:45'}</div>
            <div className="text-gray-600">{booking.route_details?.destination || 'Siem Reap'}</div>
          </div>
        </div>

        {/* Ticket Details */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div>
            <div className="text-sm text-gray-600">Date</div>
            <div className="font-semibold">{booking.date}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Seats</div>
            <div className="font-semibold">{booking.seats.join(', ')}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Duration</div>
            <div className="font-semibold">{booking.route_details?.duration || '5h 45m'}</div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Total Price</div>
            <div className="font-semibold text-orange-600">${booking.total_price}</div>
          </div>
        </div>

        {/* Passenger Details */}
        {booking.passenger_details && booking.passenger_details.length > 0 && (
          <div className="mb-6">
            <h4 className="font-semibold text-gray-800 mb-2">Passenger Details</h4>
            <div className="space-y-2">
              {booking.passenger_details.map((passenger, index) => (
                <div key={index} className="bg-gray-50 rounded p-3">
                  <div className="font-medium">{passenger.firstName} {passenger.lastName}</div>
                  <div className="text-sm text-gray-600">{passenger.email}</div>
                  {passenger.phone && <div className="text-sm text-gray-600">{passenger.phone}</div>}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* QR Code Section */}
        <div className="text-center mb-6">
          <button
            onClick={() => setShowQR(!showQR)}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
          >
            {showQR ? 'Hide QR Code' : 'Show QR Code'}
          </button>
          
          {showQR && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="mt-4"
            >
              <div className="flex justify-center">
                <QRCodeComponent value={qrValue} size={150} />
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Scan this QR code at the boarding gate
              </p>
            </motion.div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => onDownload(booking)}
            className="flex-1 bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 transition-colors flex items-center justify-center"
          >
            <Download className="w-4 h-4 mr-2" />
            Download PDF
          </button>
          <button
            onClick={() => onPrint(booking)}
            className="flex-1 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors flex items-center justify-center"
          >
            <Printer className="w-4 h-4 mr-2" />
            Print
          </button>
          <button
            onClick={() => onSend(booking)}
            className="flex-1 bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors flex items-center justify-center"
          >
            <Send className="w-4 h-4 mr-2" />
            Send
          </button>
        </div>
      </div>
    </motion.div>
  );
};

// Send Ticket Modal
const SendTicketModal = ({ isOpen, onClose, booking, onSend }) => {
  const [recipients, setRecipients] = useState('');
  const [message, setMessage] = useState('');
  const [sendMethod, setSendMethod] = useState('email');
  const [sending, setSending] = useState(false);

  const handleSend = async () => {
    if (!recipients.trim()) {
      alert('Please enter recipient information');
      return;
    }

    setSending(true);
    try {
      await onSend(booking, {
        recipients: recipients.split(',').map(r => r.trim()),
        message,
        method: sendMethod
      });
      onClose();
      setRecipients('');
      setMessage('');
    } catch (error) {
      alert('Failed to send ticket');
    } finally {
      setSending(false);
    }
  };

  if (!isOpen) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-white rounded-lg p-6 max-w-md w-full"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 className="text-xl font-bold mb-4">Send Ticket</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Send Method</label>
            <div className="flex space-x-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  value="email"
                  checked={sendMethod === 'email'}
                  onChange={(e) => setSendMethod(e.target.value)}
                  className="mr-2"
                />
                <Mail className="w-4 h-4 mr-1" />
                Email
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  value="sms"
                  checked={sendMethod === 'sms'}
                  onChange={(e) => setSendMethod(e.target.value)}
                  className="mr-2"
                />
                <Smartphone className="w-4 h-4 mr-1" />
                SMS
              </label>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {sendMethod === 'email' ? 'Email Addresses' : 'Phone Numbers'}
            </label>
            <input
              type="text"
              value={recipients}
              onChange={(e) => setRecipients(e.target.value)}
              placeholder={sendMethod === 'email' ? 'email1@example.com, email2@example.com' : '+1234567890, +0987654321'}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            />
            <p className="text-xs text-gray-600 mt-1">Separate multiple recipients with commas</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Message (Optional)</label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows={3}
              placeholder="Add a personal message..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            />
          </div>

          <div className="flex space-x-2">
            <button
              onClick={handleSend}
              disabled={sending}
              className="flex-1 bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 disabled:opacity-50 flex items-center justify-center"
            >
              {sending ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : <Send className="w-4 h-4 mr-2" />}
              {sending ? 'Sending...' : 'Send'}
            </button>
            <button
              onClick={onClose}
              className="flex-1 bg-gray-500 text-white py-2 px-4 rounded-lg hover:bg-gray-600"
            >
              Cancel
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

// Main Ticket Management Component
export const TicketManagement = () => {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedBooking, setSelectedBooking] = useState(null);
  const [showSendModal, setShowSendModal] = useState(false);
  const [filter, setFilter] = useState('all');
  const { token } = useAuth();

  useEffect(() => {
    fetchBookings();
  }, []);

  const fetchBookings = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/bookings`, {
        headers: { 'Authorization': `Bearer ${token}` }
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

  const handleDownload = async (booking) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/tickets/download/${booking.id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ticket-${booking.booking_reference}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        alert('Failed to download ticket');
      }
    } catch (error) {
      console.error('Error downloading ticket:', error);
      alert('Failed to download ticket');
    }
  };

  const handlePrint = (booking) => {
    // Create a printable version of the ticket
    const printWindow = window.open('', '_blank');
    const ticketHTML = generateTicketHTML(booking);
    
    printWindow.document.write(`
      <html>
        <head>
          <title>BusTicket - ${booking.booking_reference}</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .ticket { border: 2px solid #f97316; border-radius: 10px; padding: 20px; max-width: 600px; }
            .header { background: linear-gradient(to right, #f97316, #dc2626); color: white; padding: 20px; margin: -20px -20px 20px -20px; border-radius: 8px 8px 0 0; }
            .route { display: flex; align-items: center; justify-content: space-between; margin: 20px 0; }
            .details { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0; }
            .qr-placeholder { text-align: center; margin: 20px 0; }
            @media print { body { margin: 0; } }
          </style>
        </head>
        <body>
          ${ticketHTML}
        </body>
      </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
  };

  const handleSend = async (booking, sendData) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/tickets/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          booking_id: booking.id,
          ...sendData
        })
      });
      
      if (response.ok) {
        alert('Ticket sent successfully!');
      } else {
        throw new Error('Failed to send ticket');
      }
    } catch (error) {
      console.error('Error sending ticket:', error);
      throw error;
    }
  };

  const generateTicketHTML = (booking) => {
    return `
      <div class="ticket">
        <div class="header">
          <h1>BusTicket E-Ticket</h1>
          <p>Booking Reference: ${booking.booking_reference}</p>
        </div>
        
        <div class="route">
          <div>
            <h2>${booking.departure_time || '06:00'}</h2>
            <p>${booking.route_details?.origin || 'Phnom Penh'}</p>
          </div>
          <div style="text-align: center;">
            <p>🚌</p>
            <p>${booking.route_details?.duration || '5h 45m'}</p>
          </div>
          <div>
            <h2>${booking.arrival_time || '11:45'}</h2>
            <p>${booking.route_details?.destination || 'Siem Reap'}</p>
          </div>
        </div>
        
        <div class="details">
          <div><strong>Date:</strong> ${booking.date}</div>
          <div><strong>Seats:</strong> ${booking.seats.join(', ')}</div>
          <div><strong>Total Price:</strong> $${booking.total_price}</div>
          <div><strong>Status:</strong> ${booking.status}</div>
        </div>
        
        ${booking.passenger_details ? `
          <div>
            <h3>Passenger Details</h3>
            ${booking.passenger_details.map(p => `
              <p><strong>${p.firstName} ${p.lastName}</strong><br>
              ${p.email} ${p.phone ? `<br>${p.phone}` : ''}</p>
            `).join('')}
          </div>
        ` : ''}
        
        <div class="qr-placeholder">
          <p>[QR Code: BMB-${booking.booking_reference}-${booking.id}]</p>
          <p>Scan this code at the boarding gate</p>
        </div>
      </div>
    `;
  };

  const filteredBookings = bookings.filter(booking => {
    if (filter === 'all') return true;
    if (filter === 'upcoming') return new Date(booking.date) >= new Date();
    if (filter === 'past') return new Date(booking.date) < new Date();
    return booking.status === filter;
  });

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
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-4">Ticket Management</h1>
          <p className="text-gray-600">Print, download, or send your tickets</p>
        </div>

        {/* Filter Buttons */}
        <div className="flex flex-wrap gap-2 mb-8">
          {[
            { key: 'all', label: 'All Tickets' },
            { key: 'upcoming', label: 'Upcoming' },
            { key: 'past', label: 'Past Trips' },
            { key: 'confirmed', label: 'Confirmed' },
            { key: 'paid', label: 'Paid' }
          ].map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setFilter(key)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                filter === key
                  ? 'bg-orange-500 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {/* Tickets Grid */}
        {filteredBookings.length === 0 ? (
          <div className="text-center py-16">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-800 mb-2">No tickets found</h3>
            <p className="text-gray-600">You don't have any tickets matching the selected filter.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {filteredBookings.map((booking) => (
              <TicketCard
                key={booking.id}
                booking={booking}
                onDownload={handleDownload}
                onPrint={handlePrint}
                onSend={(booking) => {
                  setSelectedBooking(booking);
                  setShowSendModal(true);
                }}
              />
            ))}
          </div>
        )}

        {/* Send Ticket Modal */}
        <SendTicketModal
          isOpen={showSendModal}
          onClose={() => {
            setShowSendModal(false);
            setSelectedBooking(null);
          }}
          booking={selectedBooking}
          onSend={handleSend}
        />
      </div>
    </div>
  );
};