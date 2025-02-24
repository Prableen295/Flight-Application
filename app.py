import streamlit as st
from datetime import datetime, timedelta
import random

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
            "IndiGo": "6E",
            "Air India": "AI",
            "SpiceJet": "SG",
            "Vistara": "UK"
        }
        self.fare_families = ["Economy", "Premium Economy", "Business"]

    def generate_sample_flights(self):
        flights = []
        
        for _ in range(3):
            airline = random.choice(list(self.airlines_data.keys()))
            # Using string formatting to avoid leading zeros issue
            departure_hour = random.randint(0,23)
            departure_minute = random.choice(['00', '30'])
            arrival_hour = random.randint(0,23)
            arrival_minute = random.choice(['00', '30'])
            
            flight = {
                "airline": airline,
                "flight_log": f"{self.airlines_data[airline]}-{random.randint(1000, 9999)}",
                "departure": f"{departure_hour:02d}:{departure_minute}",
                "arrival": f"{arrival_hour:02d}:{arrival_minute}",
                "price": f"₹{random.randint(3000, 8000):,}",
                "fare_family": random.choice(self.fare_families)
            }
            flights.append(flight)
        return flights

    def run(self):
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .flight-header {
            display: flex;
            align-items: center;
            padding: 1rem;
            background-color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .flight-card {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .search-container {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

        # Header with Logo
        st.markdown("""
        <div class="flight-header">
            <h1>✈️ Flight Booking System</h1>
        </div>
        """, unsafe_allow_html=True)

        # Search Container
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        # Trip Type Selection
        trip_type = st.radio("Select Trip Type", ["One Way", "Round Trip"], horizontal=True)

        # Create two columns for inputs
        col1, col2 = st.columns(2)

        with col1:
            from_city = st.selectbox("From:", self.cities, index=0)
            departure_date = st.date_input(
                "Departure Date:",
                min_value=datetime.now().date(),
                value=datetime.now().date()
            )

        with col2:
            to_city = st.selectbox("To:", self.cities, index=1)
            adults = st.number_input("Number of Adults:", min_value=1, max_value=9, value=1)

        # Optional return date for round trip
        if trip_type == "Round Trip":
            return_date = st.date_input(
                "Return Date:",
                min_value=departure_date,
                value=departure_date + timedelta(days=7)
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Search Flights", type="primary"):
            if from_city == to_city:
                st.error("Departure and arrival cities cannot be the same!")
                return

            st.subheader("Available Flights")

            # Display outbound flights
            st.markdown(f"**Outbound: {from_city} → {to_city}, {departure_date}**")
            flights = self.generate_sample_flights()

            for flight in flights:
                st.markdown(f"""
                <div class="flight-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{flight['airline']}</strong><br>
                            {flight['flight_log']}
                        </div>
                        <div>
                            <strong>{flight['departure']}</strong><br>
                            Departure
                        </div>
                        <div>
                            <strong>{flight['arrival']}</strong><br>
                            Arrival
                        </div>
                        <div>
                            <strong>{flight['price']}</strong><br>
                            {flight['fare_family']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Book button outside the markdown
                st.button("Book", key=f"out_{flight['flight_log']}_{flight['departure']}")

            # If round trip, show return flights
            if trip_type == "Round Trip":
                st.markdown(f"**Return: {to_city} → {from_city}, {return_date}**")
                return_flights = self.generate_sample_flights()

                for flight in return_flights:
                    st.markdown(f"""
                    <div class="flight-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>{flight['airline']}</strong><br>
                                {flight['flight_log']}
                            </div>
                            <div>
                                <strong>{flight['departure']}</strong><br>
                                Departure
                            </div>
                            <div>
                                <strong>{flight['arrival']}</strong><br>
                                Arrival
                            </div>
                            <div>
                                <strong>{flight['price']}</strong><br>
                                {flight['fare_family']}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Book button outside the markdown
                    st.button("Book", key=f"ret_{flight['flight_log']}_{flight['departure']}")

if __name__ == "__main__":
    app = FlightBookingApp()
    app.run()
