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
            "IndiGo": "https://via.placeholder.com/100x50.png?text=IndiGo",
            "Air India": "https://via.placeholder.com/100x50.png?text=Air+India",
            "SpiceJet": "https://via.placeholder.com/100x50.png?text=SpiceJet",
            "Vistara": "https://via.placeholder.com/100x50.png?text=Vistara"
        }
        self.fare_families = ["Economy", "Premium Economy", "Business"]

    def generate_sample_flights(self):
        flights = []
        
        for _ in range(3):
            airline = random.choice(list(self.airlines_data.keys()))
            flight = {
                "airline": airline,
                "image": self.airlines_data[airline],
                "departure": f"{random.randint(0,23):02d}:{random.choice(['00', '30'])}",
                "arrival": f"{random.randint(0,23):02d}:{random.choice(['00', '30'])}",
                "price": f"₹{random.randint(3000, 8000):,}",
                "fare_family": random.choice(self.fare_families)
            }
            flights.append(flight)
        return flights

    def run(self):
        st.title("Flight Booking System")

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

        # Optional return date
        return_date = st.date_input(
            "Return Date (Optional):",
            min_value=departure_date,
            value=departure_date + timedelta(days=7)
        )

        if st.button("Search Flights"):
            if from_city == to_city:
                st.error("Departure and arrival cities cannot be the same!")
                return

            st.subheader("Available Flights")

            # Display outbound flights
            st.write(f"**Outbound: {from_city} → {to_city}, {departure_date}**")
            flights = self.generate_sample_flights()

            for flight in flights:
                with st.container():
                    cols = st.columns([1, 2, 2, 2, 2, 1])

                    with cols[0]:
                        st.image(flight["image"], use_column_width=True)

                    with cols[1]:
                        st.write(f"**{flight['airline']}**")

                    with cols[2]:
                        st.write(f"Departure: {flight['departure']}")

                    with cols[3]:
                        st.write(f"Arrival: {flight['arrival']}")

                    with cols[4]:
                        st.write(f"Price: {flight['price']}\n({flight['fare_family']})")

                    with cols[5]:
                        st.button("Book", key=f"out_{flight['departure']}")

                    st.divider()

            # If return date is different, show return flights
            if return_date != departure_date:
                st.write(f"**Return: {to_city} → {from_city}, {return_date}**")
                return_flights = self.generate_sample_flights()

                for flight in return_flights:
                    with st.container():
                        cols = st.columns([1, 2, 2, 2, 2, 1])

                        with cols[0]:
                            st.image(flight["image"], use_column_width=True)

                        with cols[1]:
                            st.write(f"**{flight['airline']}**")

                        with cols[2]:
                            st.write(f"Departure: {flight['departure']}")

                        with cols[3]:
                            st.write(f"Arrival: {flight['arrival']}")

                        with cols[4]:
                            st.write(f"Price: {flight['price']}\n({flight['fare_family']})")

                        with cols[5]:
                            st.button("Book", key=f"ret_{flight['departure']}")

                        st.divider()

if __name__ == "__main__":
    app = FlightBookingApp()
    app.run()
