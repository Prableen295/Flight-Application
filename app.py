import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Plane, Calendar, Users, ArrowRightLeft } from 'lucide-react';

const FlightBookingApp = () => {
  const [roundTrip, setRoundTrip] = useState(false);
  
  const cities = [
    "Mumbai (BOM)",
    "Delhi (DEL)",
    "Bangalore (BLR)",
    "Chennai (MAA)",
    "Kolkata (CCU)",
    "Hyderabad (HYD)",
    "Pune (PNQ)",
    "Ahmedabad (AMD)"
  ];

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Header with Logo */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-2">
          <Plane className="h-8 w-8 text-blue-600" />
          <span className="text-2xl font-bold text-blue-600">Flight Booking</span>
        </div>
      </div>

      {/* Main Search Card */}
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle>Search Flights</CardTitle>
          <div className="flex gap-4 mt-4">
            <Button 
              variant={!roundTrip ? "default" : "outline"}
              onClick={() => setRoundTrip(false)}
              className="flex-1"
            >
              One Way
            </Button>
            <Button 
              variant={roundTrip ? "default" : "outline"}
              onClick={() => setRoundTrip(true)}
              className="flex-1"
            >
              Round Trip
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* From City */}
            <div className="space-y-2">
              <label className="text-sm font-medium">From</label>
              <Select>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select city" />
                </SelectTrigger>
                <SelectContent>
                  {cities.map(city => (
                    <SelectItem key={city} value={city}>{city}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* To City */}
            <div className="space-y-2">
              <label className="text-sm font-medium">To</label>
              <Select>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select city" />
                </SelectTrigger>
                <SelectContent>
                  {cities.map(city => (
                    <SelectItem key={city} value={city}>{city}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Departure Date */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Departure</label>
              <div className="flex items-center border rounded-md p-2">
                <Calendar className="h-4 w-4 mr-2 text-gray-500" />
                <input type="date" className="w-full outline-none bg-transparent" />
              </div>
            </div>

            {/* Return Date (Conditional) */}
            {roundTrip && (
              <div className="space-y-2">
                <label className="text-sm font-medium">Return</label>
                <div className="flex items-center border rounded-md p-2">
                  <Calendar className="h-4 w-4 mr-2 text-gray-500" />
                  <input type="date" className="w-full outline-none bg-transparent" />
                </div>
              </div>
            )}

            {/* Travelers */}
            <div className="space-y-2">
              <label className="text-sm font-medium">Travelers</label>
              <div className="flex items-center border rounded-md p-2">
                <Users className="h-4 w-4 mr-2 text-gray-500" />
                <select className="w-full outline-none bg-transparent">
                  {[1,2,3,4,5,6,7,8,9].map(num => (
                    <option key={num} value={num}>{num} Adult{num > 1 ? 's' : ''}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Search Button */}
          <Button className="w-full mt-6 bg-blue-600 hover:bg-blue-700">
            Search Flights
          </Button>
        </CardContent>
      </Card>

      {/* Sample Flight Results */}
      <div className="max-w-4xl mx-auto mt-8 space-y-4">
        {[1,2,3].map(flight => (
          <Card key={flight}>
            <CardContent className="flex items-center justify-between p-6">
              <div className="flex items-center gap-4">
                <Plane className="h-6 w-6 text-blue-600" />
                <div>
                  <h3 className="font-semibold">IndiGo</h3>
                  <p className="text-sm text-gray-500">6E-1234</p>
                </div>
              </div>
              <div className="text-center">
                <p className="font-semibold">09:00</p>
                <p className="text-sm text-gray-500">BOM</p>
              </div>
              <ArrowRightLeft className="h-4 w-4 text-gray-400" />
              <div className="text-center">
                <p className="font-semibold">11:30</p>
                <p className="text-sm text-gray-500">DEL</p>
              </div>
              <div>
                <p className="font-semibold">₹4,999</p>
                <p className="text-sm text-gray-500">Economy</p>
              </div>
              <Button>Book Now</Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default FlightBookingApp;
