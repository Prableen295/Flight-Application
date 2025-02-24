import streamlit as st
from datetime import datetime, timedelta
import random

class FlightBookingApp:
    def __init__(self):
        # Initialize city and airline data
        self.cities = [
            "Mumbai (BOM)", "Delhi (DEL)", "Bangalore (BLR)", 
            "Chennai (MAA)", "Kolkata (CCU)", "Hyderabad (HYD)",
            "Pune (PNQ)", "Ahmedabad (AMD)"
        ]
        
        self.airlines = {
            "IndiGo": {"code": "6E", "color": "#0052CC"},
            "Air India": {"code": "AI", "color": "#e31837"},
            "SpiceJet": {"code": "SG", "color": "#ff4e00"},
            "Vistara": {"code": "UK", "color": "#4b286d"}
        }
        
        self.fare_classes = ["Economy", "Premium Economy", "Business"]

    def apply_custom_css(self):
        st.markdown("""
            <style>
                /* Main container styling */
                .main {
                    padding: 0;
                    margin: 0;
                }
                
                /* Header styling */
                .header {
                    background: linear-gradient(to right, #041527, #154880);
                    color: white;
                    padding: 20px;
                    margin: -1rem -1rem 2rem -1rem;
                }
                
                /* Search box styling */
                .search-box {
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }
                
                /* Flight card styling */
                .flight-card {
                    background-color: white;
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                
                /* Airline logo */
                .airline-circle {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    margin-right: 10px;
                }
                
                /* Price styling */
                .price {
                    color: #d63b3b;
                    font-size: 20px;
                    font-weight: bold;
                }
                
                /* Flight details */
                .flight-details {
                    color: #4a4a4a;
                    font-size: 14px;
                }
                
                /* Button styling */
                .stButton>button {
                    background-color: #008cff;
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 10px 20px;
                    width: 100%;
                }
                
                /* Trip type selector */
                .stRadio>label {
                    font-weight: bold;
                    color: #333;
                }
                
                /* Input labels */
                .stSelectbox>label {
                    font-weight: bold;
                    color: #333;
                }
            </style>
        """, unsafe_allow_html=True)

    def create_flight_card(self, flight, from_city, to_city):
        airline = flight["airline"]
        color = self.airlines[airline]["color"]
        
        return f"""
            <div class="flight-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center;">
                        <div class="airline-circle" style="background-color: {color}">
                            {airline[:2]}
                        </div>
                        <div>
                            <div style="font-weight: bold">{airline}</div>
                            <div class="flight-details">{flight['flight_number']}</div>
                        </div>
                    </div>
                    <div style="text-align: center">
                        <div style="font-weight: bold">{flight['departure_time']}</div>
                        <div class="flight-details">{from_city.split('(')[0]}</div>
                    </div>
                    <div style="text-align: center; margin: 0 20px">
                        <div>→</div>
                    </div>
                    <div style="text-align: center">
                        <div style="font-weight: bold">{flight['arrival_time']}</div>
                        <div class="flight-details">{to_city.split('(')[0]}</div>
                    </div>
                    <div style="text-align: right">
                        <div class="price">₹{flight['price']:,}</div>
                        <div class="flight-details">{flight['class']}</div>
                    </div>
                </div>
            </div>
        """

    def generate_flight(self):
        airline = random.choice(list(self.airlines.keys()))
        departure_hour = random.randint(0, 23)
        departure_minute = random.choice(['00', '30'])
        arrival_hour = (departure_hour + random.randint(1, 3)) % 24
        arrival_minute = random.choice(['00', '30'])
        
        return {
            "airline": airline,
            "flight_number": f"{self.airlines[airline]['code']}-{random.randint(1000, 9999)}",
            "departure_time": f"{departure_hour:02d}:{departure_minute}",
            "arrival_time": f"{arrival_hour:02d}:{arrival_minute}",
            "price": random.randint(3000, 15000),
            "class": random.choice(self.fare_classes)
        }

    def run(self):
        self.apply_custom_css()
        
        # Header
        st.markdown('<div class="header"><h1>✈️ Flight Search</h1></div>', unsafe_allow_html=True)
        
        # Search container
        st.markdown('<div class="search-box">', unsafe_allow_html=True)
        
        # Trip type selection
        trip_type = st.radio("Select Trip Type", ["One Way", "Round Trip"], horizontal=True)
        
        # Search form
        col1, col2, col3 = st.columns(3)
        
        with col1:
            from_city = st.selectbox("From", self.cities, index=0)
            
        with col2:
            to_city = st.selectbox("To", self.cities, index=1)
            
        with col3:
            departure_date = st.date_input(
                "Departure Date",
                min_value=datetime.now().date(),
                value=datetime.now().date()
            )
        
        # Additional inputs row
        col1, col2 = st.columns(2)
        
        with col1:
            if trip_type == "Round Trip":
                return_date = st.date_input(
                    "Return Date",
                    min_value=departure_date,
                    value=departure_date + timedelta(days=7)
                )
                
        with col2:
            passengers = st.number_input("Passengers", min_value=1, max_value=9, value=1)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Search button
        if st.button("SEARCH FLIGHTS", type="primary"):
            if from_city == to_city:
                st.error("Please select different cities for departure and arrival!")
                return
                
            # Display outbound flights
            st.markdown("### Available Flights")
            for _ in range(5):
                flight = self.generate_flight()
                st.markdown(
                    self.create_flight_card(flight, from_city, to_city),
                    unsafe_allow_html=True
                )
                
            # Display return flights for round trips
            if trip_type == "Round Trip":
                st.markdown("### Return Flights")
                for _ in range(5):
                    flight = self.generate_flight()
                    st.markdown(
                        self.create_flight_card(flight, to_city, from_city),
                        unsafe_allow_html=True
                    )

if __name__ == "__main__":
    app = FlightBookingApp()
    app.run()
