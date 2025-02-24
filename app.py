import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd
from PIL import Image
import io
import requests
import time

# Set page config
st.set_page_config(
    page_title="Flight Booking App",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

class FlightBookingApp:
    def __init__(self):
        # Initialize city and airline data
        self.cities = [
            "Mumbai (BOM)", "Delhi (DEL)", "Bangalore (BLR)", 
            "Chennai (MAA)", "Kolkata (CCU)", "Hyderabad (HYD)",
            "Pune (PNQ)", "Ahmedabad (AMD)", "Goa (GOI)", "Jaipur (JAI)",
            "Lucknow (LKO)", "Kochi (COK)", "Guwahati (GAU)"
        ]
        
        self.airlines = {
            "IndiGo": {
                "code": "6E", 
                "color": "#0052CC",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/IndiGo_Airlines_logo.svg/512px-IndiGo_Airlines_logo.svg.png"
            },
            "Air India": {
                "code": "AI", 
                "color": "#e31837",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Air_India_Logo.svg/512px-Air_India_Logo.svg.png"
            },
            "SpiceJet": {
                "code": "SG", 
                "color": "#ff4e00",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/SpiceJet_logo.svg/512px-SpiceJet_logo.svg.png"
            },
            "Vistara": {
                "code": "UK", 
                "color": "#4b286d",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Vistara_Logo.svg/512px-Vistara_Logo.svg.png"
            },
            "Akasa Air": {
                "code": "QP", 
                "color": "#FF6D38",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Akasa_Air_logo.svg"
            },
            "Alliance Air": {
                "code": "9I", 
                "color": "#2B3990",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Alliance_Air_India_Logo.svg/512px-Alliance_Air_India_Logo.svg.png"
            }
        }
        
        self.fare_classes = ["Economy", "Premium Economy", "Business"]
        
        self.fare_rules = {
            "Economy": {
                "Cancellation Fee": "₹3,500 per passenger",
                "Date Change Fee": "₹3,000 per passenger",
                "Seat Selection": "Chargeable",
                "Baggage Allowance": "15 kg",
                "Meal": "Not Included",
                "Refundable": "Partial"
            },
            "Premium Economy": {
                "Cancellation Fee": "₹2,500 per passenger",
                "Date Change Fee": "₹2,000 per passenger",
                "Seat Selection": "Free",
                "Baggage Allowance": "20 kg",
                "Meal": "Included",
                "Refundable": "Yes"
            },
            "Business": {
                "Cancellation Fee": "₹2,000 per passenger",
                "Date Change Fee": "₹1,500 per passenger",
                "Seat Selection": "Free",
                "Baggage Allowance": "35 kg",
                "Meal": "Included",
                "Refundable": "Yes"
            }
        }
        
        # Apply custom CSS
        self.apply_custom_css()
        
        # Initialize session state
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'search_performed' not in st.session_state:
            st.session_state.search_performed = False
        if 'selected_flight' not in st.session_state:
            st.session_state.selected_flight = None
        if 'selected_return_flight' not in st.session_state:
            st.session_state.selected_return_flight = None
        if 'flight_results' not in st.session_state:
            st.session_state.flight_results = []
        if 'return_flight_results' not in st.session_state:
            st.session_state.return_flight_results = []
        if 'view_booking' not in st.session_state:
            st.session_state.view_booking = False
        if 'passengers' not in st.session_state:
            st.session_state.passengers = 1
        if 'sort_by' not in st.session_state:
            st.session_state.sort_by = "price"
        if 'filter_airlines' not in st.session_state:
            st.session_state.filter_airlines = list(self.airlines.keys())
        if 'filter_classes' not in st.session_state:
            st.session_state.filter_classes = self.fare_classes.copy()
    
    def apply_custom_css(self):
        """Apply custom CSS styling for better UI"""
        st.markdown("""
        <style>
            .main {
                padding: 0 !important;
                margin: 0 !important;
            }
            
            .app-header {
                background: linear-gradient(135deg, #0d47a1, #42a5f5);
                padding: 1.5rem;
                color: white;
                border-radius: 0px;
                margin-bottom: 1rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .search-form {
                background-color: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                margin-bottom: 1.5rem;
                border: 1px solid #e0e0e0;
            }
            
            .flight-card {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
                transition: transform 0.2s;
                background-color: white;
            }
            
            .flight-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            
            .selected-flight {
                border: 2px solid #1976d2;
                background-color: #f5f9ff;
            }
            
            .flight-time {
                font-size: 1.2rem;
                font-weight: bold;
            }
            
            .airline-name {
                font-weight: bold;
            }
            
            .flight-price {
                color: #d32f2f;
                font-size: 1.3rem;
                font-weight: bold;
            }
            
            .flight-detail {
                color: #616161;
                font-size: 0.9rem;
            }
            
            .flight-duration {
                text-align: center;
                color: #616161;
                font-weight: bold;
                font-size: 0.9rem;
                position: relative;
            }
            
            .flight-class-tag {
                background-color: #e3f2fd;
                color: #1976d2;
                padding: 0.2rem 0.6rem;
                border-radius: 4px;
                font-size: 0.8rem;
                font-weight: bold;
            }
            
            .filter-panel {
                background-color: white;
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                margin-bottom: 1rem;
            }
            
            .progress-container {
                display: flex;
                justify-content: space-between;
                margin-bottom: 2rem;
                position: relative;
            }
            
            .progress-step {
                display: flex;
                flex-direction: column;
                align-items: center;
                z-index: 2;
            }
            
            .step-circle {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background-color: #e0e0e0;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #616161;
                font-weight: bold;
                margin-bottom: 8px;
            }
            
            .active-step .step-circle {
                background-color: #1976d2;
                color: white;
            }
            
            .step-title {
                font-size: 0.8rem;
                color: #616161;
                text-align: center;
            }
            
            .active-step .step-title {
                color: #1976d2;
                font-weight: bold;
            }
            
            .progress-line {
                position: absolute;
                top: 15px;
                left: 15%;
                right: 15%;
                height: 2px;
                background-color: #e0e0e0;
                z-index: 1;
            }
            
            .divider {
                display: flex;
                align-items: center;
                margin: 1rem 0;
            }
            
            .divider-line {
                flex-grow: 1;
                height: 1px;
                background-color: #e0e0e0;
            }
            
            .divider-text {
                margin: 0 10px;
                color: #616161;
                font-size: 0.9rem;
            }
            
            .price-breakdown {
                background-color: #f5f9ff;
                padding: 1rem;
                border-radius: 8px;
                margin-top: 1rem;
                border: 1px solid #e3f2fd;
            }
            
            .fare-rules {
                background-color: #f9f9f9;
                padding: 1rem;
                border-radius: 8px;
                margin-top: 1rem;
                border: 1px solid #e0e0e0;
            }
            
            /* Button styling */
            .stButton>button {
                background-color: #1976d2;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                font-weight: bold;
                width: 100%;
                height: 2.5rem;
            }
            
            /* Add animation to loading spinner */
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .loading-spinner {
                border: 4px solid rgba(0, 0, 0, 0.1);
                width: 36px;
                height: 36px;
                border-radius: 50%;
                border-left-color: #1976d2;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            /* Responsive fixes */
            @media (max-width: 768px) {
                .flight-card {
                    padding: 0.8rem;
                }
                .flight-time {
                    font-size: 1rem;
                }
                .flight-price {
                    font-size: 1.1rem;
                }
            }
            
            /* Hide default Streamlit elements */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Style expander headers */
            .st-eb {
                font-weight: bold !important;
                color: #1976d2 !important;
            }
            
            /* Improve the tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: white;
                border-radius: 4px 4px 0 0;
                border: 1px solid #e0e0e0;
                border-bottom: none;
                padding: 0.5rem 1rem;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #1976d2 !important;
                color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)

    def run(self):
        """Main function to run the app"""
        # Display app header
        st.markdown('<div class="app-header"><h1>✈️ Flight Booking App</h1></div>', unsafe_allow_html=True)
        
        # If already in booking flow, show booking details
        if st.session_state.view_booking:
            self.display_booking_page()
            return
            
        # Show search form
        self.display_search_form()
        
        # Show flight results if search performed
        if st.session_state.search_performed:
            self.display_flight_results()

    def display_search_form(self):
        """Display the flight search form"""
        with st.container():
            st.markdown('<div class="search-form">', unsafe_allow_html=True)
            
            # Trip type selection
            trip_type = st.radio(
                "Trip Type",
                ["One Way", "Round Trip"],
                horizontal=True,
                key="trip_type"
            )
            
            # City selection
            col1, col2 = st.columns(2)
            with col1:
                from_city = st.selectbox("From", self.cities, index=0)
            
            with col2:
                # Filter out the from_city to avoid same source and destination
                to_cities = [city for city in self.cities if city != from_city]
                to_city = st.selectbox("To", to_cities, index=0)
            
            # Date selection
            col1, col2 = st.columns(2)
            with col1:
                today = datetime.now()
                departure_date = st.date_input(
                    "Departure Date",
                    min_value=today,
                    value=today + timedelta(days=3),
                    key="departure_date"
                )
            
            with col2:
                if trip_type == "Round Trip":
                    min_return_date = departure_date + timedelta(days=1)
                    return_date = st.date_input(
                        "Return Date",
                        min_value=min_return_date,
                        value=min_return_date + timedelta(days=7),
                        key="return_date"
                    )
                else:
                    st.markdown("<br>", unsafe_allow_html=True)
            
            # Passenger selection
            col1, col2 = st.columns(2)
            with col1:
                passengers = st.number_input(
                    "Passengers",
                    min_value=1,
                    max_value=9,
                    value=st.session_state.passengers,
                    key="passenger_count"
                )
                st.session_state.passengers = passengers
            
            with col2:
                travel_class = st.selectbox(
                    "Class",
                    ["All Classes", "Economy", "Premium Economy", "Business"],
                    index=0,
                    key="travel_class"
                )
            
            # Search button
            if st.button("SEARCH FLIGHTS", key="search_button"):
                st.session_state.search_performed = True
                
                # Generate flight results
                if travel_class == "All Classes":
                    filter_class = None
                else:
                    filter_class = travel_class
                
                # Show loading spinner
                with st.spinner("Searching for the best flights..."):
                    # Generate outbound flight results
                    st.session_state.flight_results = self.generate_flights(
                        from_city, to_city, departure_date, 12
                    )
                    
                    # Generate return flight results if round trip
                    if trip_type == "Round Trip":
                        st.session_state.return_flight_results = self.generate_flights(
                            to_city, from_city, return_date, 12
                        )
                    else:
                        st.session_state.return_flight_results = []
                    
                    # Reset selected flights
                    st.session_state.selected_flight = None
                    st.session_state.selected_return_flight = None
                    
                    # Simulate a short delay for realism
                    time.sleep(1.5)
                
                st.experimental_rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    def display_flight_results(self):
        """Display flight search results"""
        # Reset view_booking if back button was used
        st.session_state.view_booking = False
        
        # Check if we have results
        if not st.session_state.flight_results:
            st.warning("No flights found. Please try different search criteria.")
            return
            
        # Display filter and sort options
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown("<h3>Filters</h3>", unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
                
                # Airline filters
                st.subheader("Airlines")
                for airline in self.airlines:
                    is_selected = airline in st.session_state.filter_airlines
                    if st.checkbox(airline, value=is_selected, key=f"airline_{airline}"):
                        if airline not in st.session_state.filter_airlines:
                            st.session_state.filter_airlines.append(airline)
                    else:
                        if airline in st.session_state.filter_airlines:
                            st.session_state.filter_airlines.remove(airline)
                
                # Class filters
                st.subheader("Class")
                for fare_class in self.fare_classes:
                    is_selected = fare_class in st.session_state.filter_classes
                    if st.checkbox(fare_class, value=is_selected, key=f"class_{fare_class}"):
                        if fare_class not in st.session_state.filter_classes:
                            st.session_state.filter_classes.append(fare_class)
                    else:
                        if fare_class in st.session_state.filter_classes:
                            st.session_state.filter_classes.remove(fare_class)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Tabs for outbound and return flights
            if st.session_state.return_flight_results:
                tabs = st.tabs(["Outbound Flight", "Return Flight"])
                
                # Outbound flight tab
                with tabs[0]:
                    st.markdown("<h3>Outbound Flights</h3>", unsafe_allow_html=True)
                    
                    # Sort options
                    sort_by = st.selectbox(
                        "Sort By",
                        ["Price (low to high)", "Duration (short to long)", "Departure (early to late)", "Arrival (early to late)"],
                        index=0,
                        key="sort_outbound"
                    )
                    
                    if "Price" in sort_by:
                        st.session_state.sort_by = "price"
                    elif "Duration" in sort_by:
                        st.session_state.sort_by = "duration"
                    elif "Departure" in sort_by:
                        st.session_state.sort_by = "departure"
                    elif "Arrival" in sort_by:
                        st.session_state.sort_by = "arrival"
                    
                    # Filter and display flights
                    filtered_flights = self.filter_and_sort_flights(st.session_state.flight_results)
                    
                    if not filtered_flights:
                        st.warning("No flights match your filters. Please adjust your criteria.")
                    else:
                        for idx, flight in enumerate(filtered_flights):
                            self.display_flight_card(flight, idx, is_return=False)
                
                # Return flight tab
                with tabs[1]:
                    st.markdown("<h3>Return Flights</h3>", unsafe_allow_html=True)
                    
                    # Sort options
                    sort_by = st.selectbox(
                        "Sort By",
                        ["Price (low to high)", "Duration (short to long)", "Departure (early to late)", "Arrival (early to late)"],
                        index=0,
                        key="sort_return"
                    )
                    
                    if "Price" in sort_by:
                        st.session_state.sort_by = "price"
                    elif "Duration" in sort_by:
                        st.session_state.sort_by = "duration"
                    elif "Departure" in sort_by:
                        st.session_state.sort_by = "departure"
                    elif "Arrival" in sort_by:
                        st.session_state.sort_by = "arrival"
                    
                    # Filter and display flights
                    filtered_return_flights = self.filter_and_sort_flights(st.session_state.return_flight_results)
                    
                    if not filtered_return_flights:
                        st.warning("No flights match your filters. Please adjust your criteria.")
                    else:
                        for idx, flight in enumerate(filtered_return_flights):
                            self.display_flight_card(flight, idx, is_return=True)
            else:
                # Only outbound flights
                st.markdown("<h3>Available Flights</h3>", unsafe_allow_html=True)
                
                # Sort options
                sort_by = st.selectbox(
                    "Sort By",
                    ["Price (low to high)", "Duration (short to long)", "Departure (early to late)", "Arrival (early to late)"],
                    index=0,
                    key="sort_outbound"
                )
                
                if "Price" in sort_by:
                    st.session_state.sort_by = "price"
                elif "Duration" in sort_by:
                    st.session_state.sort_by = "duration"
                elif "Departure" in sort_by:
                    st.session_state.sort_by = "departure"
                elif "Arrival" in sort_by:
                    st.session_state.sort_by = "arrival"
                
                # Filter and display flights
                filtered_flights = self.filter_and_sort_flights(st.session_state.flight_results)
                
                if not filtered_flights:
                    st.warning("No flights match your filters. Please adjust your criteria.")
                else:
                    for idx, flight in enumerate(filtered_flights):
                        self.display_flight_card(flight, idx, is_return=False)
        
        with col3:
            # Booking summary and proceed button
            if st.session_state.selected_flight is not None:
                # Display selected flight summary
                st.markdown("<h3>Selected Flights</h3>", unsafe_allow_html=True)
                
                # Calculate total price
                total_price = 0
                
                # Calculate outbound flight price
                if st.session_state.selected_flight is not None:
                    flight = st.session_state.flight_results[st.session_state.selected_flight]
                    base_fare = flight['price']
                    taxes = int(base_fare * 0.18)
                    convenience_fee = 350
                    flight_price = (base_fare + taxes + convenience_fee) * st.session_state.passengers
                    total_price += flight_price
                
                # Calculate return flight price if selected
                if st.session_state.return_flight_results and st.session_state.selected_return_flight is not None:
                    flight = st.session_state.return_flight_results[st.session_state.selected_return_flight]
                    base_fare = flight['price']
                    taxes = int(base_fare * 0.18)
                    convenience_fee = 350
                    flight_price = (base_fare + taxes + convenience_fee) * st.session_state.passengers
                    total_price += flight_price
                
                # Display price and proceed button
                st.markdown(f"<div class='price-breakdown'><h4>Price Summary</h4>", unsafe_allow_html=True)
                st.markdown(f"<p>Passengers: {st.session_state.passengers}</p>", unsafe_allow_html=True)
                st.markdown(f"<p>Total Fare: <span class='flight-price'>₹{total_price:,}</span></p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Check if return flight is required but not selected
                proceed_disabled = False
                if st.session_state.return_flight_results and st.session_state.selected_return_flight is None:
                    st.warning("Please select a return flight to proceed.")
                    proceed_disabled = True
                
                # Proceed button
                if st.button("CONTINUE BOOKING", disabled=proceed_disabled):
                    st.session_state.view_booking = True
                    st.experimental_rerun()

    def display_booking_page(self):
        """Display booking and passenger details page"""
        # Add back button
        if st.button("← Back to Flight Selection"):
            st.session_state.view_booking = False
            st.experimental_rerun()
        
        # Display booking summary
        self.display_booking_summary()
        
        # Passenger details form
        st.markdown("<h3>Passenger Details</h3>", unsafe_allow_html=True)
        
        for i in range(st.session_state.passengers):
            st.markdown(f"<h4>Passenger {i+1}</h4>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.selectbox("Title", ["Mr.", "Mrs.", "Ms.", "Dr."], key=f"title_{i}")
            
            with col2:
                st.text_input("First Name", key=f"first_name_{i}")
            
            with col3:
                st.text_input("Last Name", key=f"last_name_{i}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.date_input("Date of Birth", datetime.now() - timedelta(days=365*25), key=f"dob_{i}")
            
            with col2:
                st.text_input("Nationality", "Indian", key=f"nationality_{i}")
            
            # Add more fields as needed
            st.markdown("<hr>", unsafe_allow_html=True)
        
        # Contact details
        st.markdown("<h3>Contact Details</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Email Address")
        
        with col2:
            st.text_input("Mobile Number")
        
        # Complete booking button
        if st.button("PROCEED TO PAYMENT", key="complete_booking"):
            st.success("Booking details saved! Redirecting to payment page...")
            # In a real app, this would redirect to a payment gateway

    def display_flight_card(self, flight, index, is_return=False):
        """Display a flight card with all details"""
        airline = flight["airline"]
        flight_number = flight["flight_number"]
        duration_mins = self.get_flight_time_in_minutes(flight["departure_time"], flight["arrival_time"])
        duration_text = self.format_duration(duration_mins)
        
        # Calculate fare details
        base_fare = flight['price']
        taxes = int(base_fare * 0.18)  # GST
        convenience_fee = 350
        total_fare = base_fare + taxes + convenience_fee
        
        # Check if this flight is selected
        is_selected = (is_return and st.session_state.selected_return_flight == index) or \
                     (not is_return and st.session_state.selected_flight == index)
        
        # Create flight card container
        card_style = "flight-card selected-flight" if is_selected else "flight-card"
        
        with st.container():
            st.markdown(f"<div class='{card_style}'>", unsafe_allow_html=True)
            
            # Top row with airline and price
            col1, col2, col3 = st.columns([3, 5, 2])
            
            with col1:
                # Display airline name and flight number
                st.markdown(f"<div class='airline-name'>{airline}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='flight-detail'>{flight_number}</div>", unsafe_allow_html=True)
                st.markdown(f"<span class='flight-class-tag'>{flight['class']}</span>", unsafe_allow_html=True)
            
            with col2:
                # Flight times and route with duration
                subcol1, subcol2, subcol3 = st.columns([2, 1, 2])
                
                with subcol1:
                    st.markdown(f"<div class='flight-time'>{flight['departure_time']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='flight-detail'>{flight['from_city'].split('(')[0].strip()}</div>", unsafe_allow_html=True)
                    airport_code = flight['from_city'].split('(')[1].replace(')', '')
                    st.markdown(f"<div class='flight-detail'>{airport_code}</div>", unsafe_allow_html=True)
                
                with subcol2:
                    st.markdown(f"<div class='flight-duration'>{duration_text}</div>", unsafe_allow_html=True)
                    st.markdown("→", unsafe_allow_html=True)
                
                with subcol3:
                    st.markdown(f"<div class='flight-time'>{flight['arrival_time']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='flight-detail'>{flight['to_city'].split('(')[0].strip()}</div>", unsafe_allow_html=True)
                    airport_code = flight['to_city'].split('(')[1].replace(')', '')
                    st.markdown(f"<div class='flight-detail'>{airport_code}</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"<div class='flight-price'>₹{total_fare:,}</div>", unsafe_allow_html=True)
                st.markdown("<div class='flight-detail'>per passenger</div>", unsafe_allow_html=True)
            
            # Expandable sections
            col1, col2 = st
