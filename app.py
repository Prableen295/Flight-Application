import streamlit as st
from datetime import datetime, timedelta
import random
import base64

class FlightBookingApp:
    def __init__(self):
        self.cities = [
            "Mumbai (BOM)",
            "Delhi (DEL)",
            "Bangalore (BLR)",
            "Chennai (MAA)",
            "Kolkata (CCU)",
            "Hyderabad (HYD)",
            "Pune (PNQ)",
            "Ahmedabad (AMD)"
        ]
        self.airlines_data = {
            "IndiGo": {"code": "6E", "color": "#1b1fd1"},
            "Air India": {"code": "AI", "color": "#e31837"},
            "SpiceJet": {"code": "SG", "color": "#ff4f00"},
            "Vistara": {"code": "UK", "color": "#4b286d"}
        }
        self.fare_families = ["Economy", "Premium Economy", "Business"]

    def generate_sample_flights(self):
        flights = []
        
        for _ in range(3):
            airline = random.choice(list(self.airlines_data.keys()))
            departure_hour = random.randint(0,23)
            departure_minute = random.choice(['00', '30'])
            arrival_hour = random.randint(0,23)
            arrival_minute = random.choice(['00', '30'])
            
            flight = {
                "airline": airline,
                "airline_color": self.airlines_data[airline]["color"],
                "flight_log": f"{self.airlines_data[airline]['code']}-{random.randint(1000, 9999)}",
                "departure": f"{departure_hour:02d}:{departure_minute}",
                "arrival": f"{arrival_hour:02d}:{arrival_minute}",
                "price": random.randint(3000, 8000),
                "fare_family": random.choice(self.fare_families)
            }
            flights.append(flight)
        return flights

    def run(self):
        # Custom CSS for MakeMyTrip-like styling
        st.markdown("""
        <style>
        .stApp {
            background-color: #f2f2f2;
        }
        .main-header {
            background: linear-gradient(to right, #051423, #15457c);
            padding: 1rem;
            margin: -1rem -1rem 2rem -1rem;
            color: white;
        }
        .search-container {
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .flight-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        .flight-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .airline-logo {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            margin-right: 1rem;
        }
        .trip-type-selector {
            background-color: #f8f9fa;
            padding: 0.5rem;
            border-radius: 4px;
            margin-bottom: 1.5rem;
        }
        .price-tag {
            font-size: 1.25rem;
            font-weight: bold;
            color: #d63b3b;
        }
        .city-input {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 0.5rem;
        }
        .flight-time {
            font-size: 1.1rem;
            font-weight: bold;
            color: #333;
        }
        .flight-detail {
            color: #666;
            font-size: 0.9rem;
        }
        .book-button {
            background-color: #008cff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
        }
        .book-button:hover {
            background-color: #0070cc;
        }
        </style>
        """, unsafe_allow_html=True)

        # Header with gradient background
        st.markdown("""
        <div class="main-header">
            <h1>✈️ Flight Booking</h1>
        </div>
        """, unsafe_allow_html=True)

        # Search Container
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        # Trip Type Selection with better styling
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            trip_type = st.radio("", ["One Way", "Round Trip"], horizontal=True, key="trip_type")

        # Create three columns for inputs to match MakeMyTrip layout
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<p style="font-weight: bold; color: #333;">From</p>', unsafe_allow_html=True)
            from_city = st.selectbox("", self.cities, index=0, key="from_city")

        with col2:
            st.markdown('<p style="font-weight: bold; color: #333;">To</p>', unsafe_allow_html=True)
            to_city = st.selectbox("", self.cities, index=1, key="to_city")

        with col3:
            st.markdown('<p style="font-weight: bold; color: #333;">Departure Date</p>', unsafe_allow_html=True)
            departure_date = st.date_input(
                "",
                min_value=datetime.now().date(),
                value=datetime.now().date()
            )

        # Second row of inputs
        col1, col2 = st.columns(2)

        with col1:
            if trip_type == "Round Trip":
                st.markdown('<p style="font-weight: bold; color: #333;">Return Date</p>', unsafe_allow_html=True)
                return_date = st.date_input(
                    "",
                    min_value=departure_date,
                    value=departure_date + timedelta(days=7)
                )

        with col2:
            st.markdown('<p style="font-weight: bold; color: #333;">Travelers</p>', unsafe_allow_html=True)
            adults = st.number_input("", min_value=1, max_value=9, value=1)

        # Search button with MakeMyTrip styling
        if st.button("SEARCH FLIGHTS", type="primary"):
            if from_city == to_city:
                st.error("Departure and arrival cities cannot be the same!")
                return

            st.markdown("### Available Flights")
            flights = self.generate_sample_flights()

            for flight in flights:
                st.markdown(f"""
                <div class="flight-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="display: flex; align-items: center;">
                            <div class="airline-logo" style="background-color: {flight['airline_color']}">
                                {flight['airline'][:2]}
                            </div>
                            <div>
                                <div style="font-weight: bold;">{flight['airline']}</div>
                                <div class="flight-detail">{flight['flight_log']}</div>
                            </div>
                        </div>
                        <div style="text-align: center;">
                            <div class="flight-time">{flight['departure']}</div>
                            <div class="flight-detail">{from_city.split('(')[0]}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #666;">→</div>
                        </div>
                        <div style="text-align: center;">
                            <div class="flight-time">{flight['arrival']}</div>
                            <div class="flight-detail">{to_city.split('(')[0]}</div>
                        </div>
                        <div style="text-align: right;">
                            <div class="price-tag">₹{flight['price']:,}</div>
                            <div class="flight-detail">{flight['fare_family']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if trip_type == "Round Trip":
                st.markdown("### Return Flights")
                return_flights = self.generate_sample_flights()
                
                for flight in return_flights:
                    st.markdown(f"""
                    <div class="flight-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="display: flex; align-items: center;">
                                <div class="airline-logo" style="background-color: {flight['airline_color']}">
                                    {flight['airline'][:2]}
                                </div>
                                <div>
                                    <div style="font-weight: bold;">{flight['airline']}</div>
                                    <div class="flight-detail">{flight['flight_log']}</div>
                                </div>
                            </div>
                            <div style="text-align: center;">
                                <div class="flight-time">{flight['departure']}</div>
                                <div class="flight-detail">{to_city.split('(')[0]}</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="color: #666;">→</div>
                            </div>
                            <div style="text-align: center;">
                                <div class="flight-time">{flight['arrival']}</div>
                                <div class="flight-detail">{from_city.split('(')[0]}</div>
                            </div>
                            <div style="text-align: right;">
                                <div class="price-tag">₹{flight['price']:,}</div>
                                <div class="flight-detail">{flight['fare_family']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    app = FlightBookingApp()
    app.run()
