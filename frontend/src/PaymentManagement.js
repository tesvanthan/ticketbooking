import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  CreditCard, 
  DollarSign, 
  Smartphone, 
  QrCode, 
  Building, 
  MapPin, 
  Clock, 
  Check, 
  X, 
  Loader2,
  ChevronRight,
  Shield,
  Star,
  Banknote,
  Wallet,
  CreditCardIcon,
  Timer,
  AlertCircle,
  CheckCircle
} from 'lucide-react';
import { useAuth } from './components';

// Enhanced Payment Component with Multiple Methods
export const PaymentManagement = ({ booking, onPaymentComplete, onCancel }) => {
  const [selectedMethod, setSelectedMethod] = useState('');
  const [paymentData, setPaymentData] = useState({});
  const [processing, setProcessing] = useState(false);
  const [timeLeft, setTimeLeft] = useState(480); // 8 minutes in seconds
  const [step, setStep] = useState('select'); // select, details, processing, success
  const { token } = useAuth();

  // Payment methods configuration
  const paymentMethods = {
    popular: [
      { id: 'aba_pay', name: 'ABA PAY', icon: '/images/aba-pay.png', type: 'digital_wallet' },
      { id: 'khqr', name: 'KHQR', icon: '/images/khqr.png', type: 'qr_code' },
      { id: 'cards', name: 'Credit/Debit Cards', icon: '/images/cards.png', type: 'card' }
    ],
    local: [
      { id: 'acleda_pay', name: 'ACLEDA Pay', icon: '/images/acleda-pay.png', type: 'digital_wallet' },
      { id: 'truemoney', name: 'TrueMoney Wallet', icon: '/images/truemoney.png', type: 'digital_wallet' },
      { id: 'chip_mong_pay', name: 'Chip Mong Pay', icon: '/images/chip-mong-pay.png', type: 'digital_wallet' }
    ],
    offline: [
      { id: 'pay_boarding', name: 'Pay on Boarding Point', icon: MapPin, type: 'offline' },
      { id: 'bank_transfer', name: 'Bank Transfer', icon: Building, type: 'bank' },
      { id: 'pay_offline', name: 'Pay at Office', icon: Clock, type: 'offline' }
    ]
  };

  // Countdown timer
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          onCancel();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [onCancel]);

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleMethodSelect = (methodId) => {
    setSelectedMethod(methodId);
    setStep('details');
  };

  const handlePaymentSubmit = async () => {
    setProcessing(true);
    setStep('processing');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          booking_id: booking.id,
          payment_method: selectedMethod,
          payment_data: paymentData
        })
      });

      if (response.ok) {
        const result = await response.json();
        setStep('success');
        setTimeout(() => onPaymentComplete(result), 2000);
      } else {
        throw new Error('Payment failed');
      }
    } catch (error) {
      console.error('Payment error:', error);
      alert('Payment failed. Please try again.');
      setStep('select');
    } finally {
      setProcessing(false);
    }
  };

  // Payment Method Selection Step
  if (step === 'select') {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Payment Methods */}
              <div className="lg:col-span-2">
                <div className="bg-white rounded-lg shadow-md p-6">
                  {/* Timer */}
                  <div className="flex items-center justify-between mb-6 p-4 bg-red-50 rounded-lg border border-red-200">
                    <div className="flex items-center space-x-2">
                      <Timer className="w-5 h-5 text-red-600" />
                      <span className="text-red-800 font-medium">{formatTime(timeLeft)}</span>
                    </div>
                    <span className="text-sm text-red-600">
                      Please complete your payment within 8 minutes. Click on your preferred payment method to pay!
                    </span>
                  </div>

                  {/* Popular Payments */}
                  <div className="mb-8">
                    <div className="flex items-center space-x-2 mb-4">
                      <Star className="w-5 h-5 text-orange-500" />
                      <h3 className="text-lg font-semibold">Popular Payments</h3>
                    </div>
                    <p className="text-gray-600 mb-4">Choose one of the payment methods below.</p>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {paymentMethods.popular.map((method) => (
                        <motion.button
                          key={method.id}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={() => handleMethodSelect(method.id)}
                          className="p-4 border-2 border-gray-200 rounded-lg hover:border-orange-500 transition-colors"
                        >
                          {method.icon.startsWith('/') ? (
                            <img 
                              src={`https://via.placeholder.com/120x60/${method.id === 'aba_pay' ? '0052CC/FFFFFF' : method.id === 'khqr' ? 'DC143C/FFFFFF' : '1E40AF/FFFFFF'}?text=${method.name.replace(/\s+/g, '+')}`}
                              alt={method.name}
                              className="h-12 mx-auto mb-2"
                            />
                          ) : (
                            <CreditCard className="w-12 h-12 mx-auto mb-2 text-gray-600" />
                          )}
                        </motion.button>
                      ))}
                    </div>
                  </div>

                  {/* Credit/Debit Cards */}
                  <div className="mb-8">
                    <div className="flex items-center space-x-2 mb-4">
                      <CreditCardIcon className="w-5 h-5 text-blue-500" />
                      <h3 className="text-lg font-semibold">Credit / Debit Cards</h3>
                    </div>
                    
                    <button
                      onClick={() => handleMethodSelect('credit_card')}
                      className="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-orange-500 transition-colors flex items-center justify-between"
                    >
                      <div className="flex items-center space-x-3">
                        <CreditCard className="w-8 h-8 text-gray-600" />
                        <span className="font-medium">Credit / Debit Cards</span>
                      </div>
                      <ChevronRight className="w-5 h-5 text-gray-400" />
                    </button>
                  </div>

                  {/* Local Payments */}
                  <div className="mb-8">
                    <div className="flex items-center space-x-2 mb-4">
                      <Building className="w-5 h-5 text-green-500" />
                      <h3 className="text-lg font-semibold">Local Payments</h3>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {paymentMethods.local.map((method) => (
                        <motion.button
                          key={method.id}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                          onClick={() => handleMethodSelect(method.id)}
                          className="p-4 border-2 border-gray-200 rounded-lg hover:border-orange-500 transition-colors"
                        >
                          <img 
                            src={`https://via.placeholder.com/120x60/${method.id === 'acleda_pay' ? '8B5CF6/FFFFFF' : method.id === 'truemoney' ? 'EF4444/FFFFFF' : '06B6D4/FFFFFF'}?text=${method.name.replace(/\s+/g, '+')}`}
                            alt={method.name}
                            className="h-12 mx-auto mb-2"
                          />
                        </motion.button>
                      ))}
                    </div>
                  </div>

                  {/* Other Payments */}
                  <div>
                    <div className="flex items-center space-x-2 mb-4">
                      <Banknote className="w-5 h-5 text-purple-500" />
                      <h3 className="text-lg font-semibold">Other Payments</h3>
                    </div>
                    
                    <div className="space-y-3">
                      {paymentMethods.offline.map((method) => {
                        const IconComponent = method.icon;
                        return (
                          <button
                            key={method.id}
                            onClick={() => handleMethodSelect(method.id)}
                            className="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-orange-500 transition-colors flex items-center justify-between"
                          >
                            <div className="flex items-center space-x-3">
                              <IconComponent className="w-6 h-6 text-gray-600" />
                              <span className="font-medium">{method.name}</span>
                            </div>
                            <ChevronRight className="w-5 h-5 text-gray-400" />
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>

              {/* Trip Summary */}
              <div className="lg:col-span-1">
                <div className="bg-white rounded-lg shadow-md p-6 sticky top-8">
                  <h3 className="text-xl font-bold mb-4">TRIP SUMMARY</h3>
                  
                  <div className="space-y-4 mb-6">
                    <div>
                      <div className="text-lg font-semibold">{booking.date} {booking.departure_time}</div>
                      <div className="text-gray-600">
                        {booking.route_details?.origin} → {booking.route_details?.destination}
                      </div>
                      <div className="text-sm text-gray-500">{booking.company}</div>
                      <div className="text-sm text-gray-500">Type: {booking.vehicle_type}</div>
                      <div className="text-sm text-gray-500">Number of Passengers: {booking.seats?.length || 1}</div>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h4 className="font-semibold mb-3">Passenger's Contact</h4>
                    <div className="text-sm text-gray-600">
                      <div>{booking.passenger_details?.[0]?.phone || '+855 10 292 929'}</div>
                      <div>{booking.passenger_details?.[0]?.email || 'tesvanthan@gmail.com'}</div>
                    </div>
                  </div>

                  <div className="border-t pt-4 mt-4">
                    <h4 className="font-semibold mb-3">PAYMENT SUMMARY</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Sub total</span>
                        <span>USD {booking.price || 15.00}</span>
                      </div>
                      <div className="flex justify-between text-green-600">
                        <span>Discount</span>
                        <span>USD 2.50</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Service Fee</span>
                        <span>USD 0.00</span>
                      </div>
                      <div className="border-t pt-2 flex justify-between text-lg font-bold">
                        <span>Total</span>
                        <span className="text-orange-600">USD {((booking.price || 15.00) - 2.50).toFixed(2)}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Payment Details Step
  if (step === 'details') {
    const method = [...paymentMethods.popular, ...paymentMethods.local, ...paymentMethods.offline]
      .find(m => m.id === selectedMethod);

    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold">Payment Details - {method?.name}</h3>
                <button
                  onClick={() => setStep('select')}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              {selectedMethod === 'credit_card' && (
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Card Number</label>
                    <input
                      type="text"
                      placeholder="1234 5678 9012 3456"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                      onChange={(e) => setPaymentData({...paymentData, cardNumber: e.target.value})}
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Expiry Date</label>
                      <input
                        type="text"
                        placeholder="MM/YY"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                        onChange={(e) => setPaymentData({...paymentData, expiryDate: e.target.value})}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">CVV</label>
                      <input
                        type="text"
                        placeholder="123"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                        onChange={(e) => setPaymentData({...paymentData, cvv: e.target.value})}
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Cardholder Name</label>
                    <input
                      type="text"
                      placeholder="John Doe"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                      onChange={(e) => setPaymentData({...paymentData, cardholderName: e.target.value})}
                    />
                  </div>
                </div>
              )}

              {(selectedMethod === 'khqr' || selectedMethod.includes('pay')) && (
                <div className="text-center py-8">
                  <QrCode className="w-32 h-32 mx-auto mb-4 text-gray-400" />
                  <p className="text-lg font-semibold mb-2">Scan QR Code to Pay</p>
                  <p className="text-gray-600">Use your {method?.name} app to scan and complete payment</p>
                  <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600">Amount: USD {((booking.price || 15.00) - 2.50).toFixed(2)}</p>
                  </div>
                </div>
              )}

              {method?.type === 'offline' && (
                <div className="text-center py-8">
                  <AlertCircle className="w-16 h-16 mx-auto mb-4 text-orange-500" />
                  <p className="text-lg font-semibold mb-2">{method?.name}</p>
                  <div className="text-gray-600 space-y-2">
                    {selectedMethod === 'pay_boarding' && (
                      <p>Pay directly at the boarding point before departure. Please arrive 30 minutes early.</p>
                    )}
                    {selectedMethod === 'bank_transfer' && (
                      <div>
                        <p>Transfer to our bank account:</p>
                        <div className="mt-4 p-4 bg-gray-50 rounded-lg text-left">
                          <p><strong>Bank:</strong> ABA Bank</p>
                          <p><strong>Account:</strong> 000 123 456 789</p>
                          <p><strong>Name:</strong> BusTicket Co., Ltd</p>
                          <p><strong>Amount:</strong> USD {((booking.price || 15.00) - 2.50).toFixed(2)}</p>
                        </div>
                      </div>
                    )}
                    {selectedMethod === 'pay_offline' && (
                      <p>Visit our office to complete payment. Office hours: 8AM - 6PM daily.</p>
                    )}
                  </div>
                </div>
              )}

              <div className="mt-6 pt-6 border-t">
                <div className="flex items-center mb-4">
                  <input type="checkbox" className="mr-2" />
                  <span className="text-sm text-gray-600">
                    By completing this booking, I confirm that I have read and agree to BookMeBus' 
                    <a href="#" className="text-orange-500 hover:text-orange-600"> Terms and Privacy Policy</a>.
                  </span>
                </div>
                
                <button
                  onClick={handlePaymentSubmit}
                  disabled={processing}
                  className="w-full bg-green-500 text-white py-3 px-6 rounded-lg font-semibold hover:bg-green-600 disabled:opacity-50 flex items-center justify-center"
                >
                  {processing ? (
                    <Loader2 className="w-5 h-5 animate-spin mr-2" />
                  ) : (
                    <Shield className="w-5 h-5 mr-2" />
                  )}
                  {processing ? 'Processing...' : 'Pay Now'}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Processing Step
  if (step === 'processing') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <Loader2 className="w-16 h-16 animate-spin text-orange-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">Processing Payment...</h3>
          <p className="text-gray-600">Please wait while we process your payment.</p>
        </div>
      </div>
    );
  }

  // Success Step
  if (step === 'success') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">Payment Successful!</h3>
          <p className="text-gray-600">Your booking has been confirmed. Redirecting...</p>
        </div>
      </div>
    );
  }

  return null;
};