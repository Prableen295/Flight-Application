import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd
from PIL import Image
import io
import requests
from streamlit_extras.stylable_container import stylable_container
import time

# Try to import streamlit_extras, if not available, define a placeholder
try:
    from streamlit_extras.colored_header import colored_header
    from streamlit_extras.card import card
except ImportError:
    # Define placeholder functions if imports aren't available
    def colored_header(label, description=None, color_name=None):
        st.header(label)
        if description:
            st.write(description)
    
    def card(title, text, image=None, url=None):
        st.subheader(title)
        st.write(text)
        if image:
            st.image(image)
        if url:
            st.markdown(f"[More info]({url})")

class EnhancedFlightBookingApp:
    def __init__(self):
        # Set page config
        st.set_page_config(
            page_title="Flight Booking App",
            page_icon="✈️",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
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
        
        self.apply_custom_css()
        
        # Session state initialization
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
        """Apply custom CSS styling to improve the app's appearance"""
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
            
            /* Improve button styling */
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

    def load_airline_logo(self, airline):
        """Load airline logo from URL or use a placeholder"""
        try:
            logo_url = self.airlines[airline]["logo_url"]
            response = requests.get(logo_url)
            logo = Image.open(io.BytesIO(response.content))
            return logo
        except:
            # Return a simple colored square with airline initials as placeholder
            color = self.airlines[airline]["color"]
            code = self.airlines[airline]["code"]
            # Create placeholder text saying this would be the logo
            return f"[{code}]"

    def get_flight_time_in_minutes(self, departure_time, arrival_time):
        """Calculate flight duration in minutes"""
        dept_hour, dept_min = map(int, departure_time.split(':'))
        arr_hour, arr_min = map(int, arrival_time.split(':'))
        
        # Handle flights that cross midnight
        if (arr_hour < dept_hour) or (arr_hour == dept_hour and arr_min < dept_min):
            arr_hour += 24
            
        # Calculate total minutes
        dept_total_mins = dept_hour * 60 + dept_min
        arr_total_mins = arr_hour * 60 + arr_min
        
        return arr_total_mins - dept_total_mins

    def format_duration(self, minutes):
        """Format duration from minutes to Xh Ym format"""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m"

    def display_flight_card(self, flight, index, is_return=False):
        """Display a flight card using Streamlit components"""
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
        
        # Add flight card with custom styling
        card_key = f"flight_card_{index}{'_return' if is_return else ''}"
        
        # Create flight card with container
        with stylable_container(
            key=card_key,
            css_styles=f"""
                .flight-card {{
                    border: {f'2px solid #1976d2;' if is_selected else '1px solid #e0e0e0;'}
                    background-color: {f'#f5f9ff;' if is_selected else 'white;'}
                }}
            """
        ):
            with st.container():
                # Top row with airline and price
                col1, col2, col3 = st.columns([3, 5, 2])
                
                with col1:
                    # Try to display airline logo first, if it fails just show text
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
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.expander("Fare Breakup"):
                        st.markdown(f"""
                        | Item | Amount |
                        | ---- | ------ |
                        | Base Fare | ₹{base_fare:,} |
                        | Taxes & Fees | ₹{taxes:,} |
                        | Convenience Fee | ₹{convenience_fee} |
                        | **Total Amount** | **₹{total_fare:,}** |
                        """)
                
                with col2:
                    with st.expander("Fare Rules"):
                        fare_class = flight['class']
                        rules = self.fare_rules[fare_class]
                        
                        st.markdown(f"""
                        | Rule | Details |
                        | ---- | ------- |
                        | Cancellation Fee | {rules['Cancellation Fee']} |
                        | Date Change Fee | {rules['Date Change Fee']} |
                        | Seat Selection | {rules['Seat Selection']} |
                        | Baggage Allowance | {rules['Baggage Allowance']} |
                        | Meal | {rules['Meal']} |
                        | Refundable | {rules['Refundable']} |
                        """)
                
                # Select button
                if is_selected:
                    select_button_label = "SELECTED ✓"
                else:
                    select_button_label = "SELECT FLIGHT"
                
                # Function to handle flight selection
                def select_flight(idx, is_ret):
                    if is_ret:
                        st.session_state.selected_return_flight = idx
                    else:
                        st.session_state.selected_flight = idx
                
                # Button to select this flight
                if st.button(select_button_label, key=f"select_{index}{'_return' if is_return else ''}"):
                    select_flight(index, is_return)
                    st.experimental_rerun()

    def generate_flight(self, from_city, to_city, departure_date, fare_class=None):
        """Generate a realistic flight with appropriate times based on cities"""
        airline = random.choice(list(self.airlines.keys()))
        
        # More realistic time generation
        departure_hour = random.randint(6, 22)  # Flights between 6 AM and 10 PM
        departure_minute = random.choice(['00', '10', '15', '20', '30', '40', '45', '50'])
        
        # Flight duration based on cities (simulating real distances)
        city_pairs = {
            # Format: (from, to): (min_minutes, max_minutes)
            ('Mumbai', 'Delhi'): (120, 150),
            ('Delhi', 'Mumbai'): (120, 150),
            ('Mumbai', 'Bangalore'): (90, 110),
            ('Bangalore', 'Mumbai'): (90, 110),
            ('Delhi', 'Bangalore'): (150, 180),
            ('Bangalore', 'Delhi'): (150, 180),
            ('Mumbai', 'Chennai'): (110, 130),
            ('Chennai', 'Mumbai'): (110, 130),
            ('Delhi', 'Chennai'): (160, 190),
            ('Chennai', 'Delhi'): (160, 190),
            ('Mumbai', 'Kolkata'): (160, 190),
            ('Kolkata', 'Mumbai'): (160, 190),
            ('Delhi', 'Kolkata'): (120, 150),
            ('Kolkata', 'Delhi'): (120, 150),
        }
        
        # Get from/to city main names
        from_main = from_city.split('(')[0].strip()
        to_main = to_city.split('(')[0].strip()
        
        # Get duration range or use default
        duration_range = city_pairs.get((from_main, to_main), (60, 180))
        flight_duration = random.randint(duration_range[0], duration_range[1])
        
        # Calculate arrival time
        departure_time_mins = departure_hour * 60 + int(departure_minute)
        arrival_time_mins = departure_time_mins + flight_duration
        
        arrival_hour = (arrival_time_mins // 60) % 24
        arrival_minute = arrival_time_mins % 60
        
        # Generate price based on class
        if not fare_class:
            fare_class = random.choice(self.fare_classes)
            
        base_prices = {
            "Economy": (3000, 8000),
            "Premium Economy": (6000, 12000),
            "Business": (15000, 35000)
        }
        
        price_range = base_prices[fare_class]
        price = random.randint(price_range[0], price_range[1])
        
        # Generate a realistic flight number
        flight_number = f"{self.airlines[airline]['code']}-{random.randint(100, 999)}"
        
        return {
            "airline": airline,
            "flight_number": flight_number,
            "departure_time": f"{departure_hour:02d}:{departure_minute}",
            "arrival_time": f"{arrival_hour:02d}:{arrival_minute:02d}",
            "price": price,
            "class": fare_class,
            "from_city": from_city,
            "to_city": to_city,
            "date": departure_date.strftime("%d %b %Y"),
            "duration_mins": flight_duration
        }

    def generate_flights(self, from_city, to_city, date, count=8):
        """Generate multiple flights between cities"""
        flights = []
        
        # Ensure we have flights for all classes
        for fare_class in self.fare_classes:
            # Generate 2-3 flights for each class
            for _ in range(random.randint(2, 3)):
                flights.append(self.generate_flight(from_city, to_city, date, fare_class))
        
        # Add more random flights to reach the count
        while len(flights) < count:
            flights.append(self.generate_flight(from_city, to_city, date))
            
        return flights

    def filter_and_sort_flights(self, flights):
        """Filter and sort flight results based on user preferences"""
        # Filter by airlines
        filtered_flights = [f for f in flights if f["airline"] in st.session_state.filter_airlines]
        
        # Filter by class
        filtered_flights = [f for f in filtered_flights if f["class"] in st.session_state.filter_classes]
        
        # Sort flights
        if st.session_state.sort_by == "price":
            filtered_flights.sort(key=lambda x: x["price"])
        elif st.session_state.sort_by == "duration":
            filtered_flights.sort(key=lambda x: x["duration_mins"])
        elif st.session_state.sort_by == "departure":
            filtered_flights.sort(key=lambda x: x["departure_time"])
        elif st.session_state.sort_by == "arrival":
            filtered_flights.sort(key=lambda x: x["arrival_time"])
            
        return filtered_flights

    def display_booking_summary(self):
        """Display booking summary after flight selection"""
        st.markdown("<h3>Your Booking Summary</h3>", unsafe_allow_html=True)
        
        # Booking progress indicator
        st.markdown("""
        <div class="progress-container">
            <div class="progress-line"></div>
            <div class="progress-step active-step">
                <div class="step-circle">1</div>
                <div class="step-title">Select Flights</div>
            </div>
            <div class="progress-step">
                <div class="step-circle">2</div>
                <div class="step-title">Passenger Details</div>
            </div>
            <div class="progress-step">
                <div class="step-circle">3</div>
                <div class="step-title">Seat Selection</div>
            </div>
            <div class="progress-step">
                <div class="step-circle">4</div>
                <div class="step-title">Payment</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Outbound flight summary
            if st.session_state.selected_flight is not None:
                flight = st.session_state.flight_results[st.session_state.selected_flight]
                
                st.markdown("<div class='divider'><div class='divider-line'></div><div class='divider-text'>OUTBOUND FLIGHT</div><div class='divider-line'></div></div>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 3, 1])
                
                with col1:
                    st.markdown(f"<div class='airline-name'>{flight['airline']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='flight-detail'>{flight['flight_number']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='flight-detail'>{flight['date']}</div>", unsafe_allow_html=True)
                
                with col2:
                    cols = st.columns([2, 1, 2])
                    with cols[0]:
                        st.markdown(f"<div class='flight-time'>{flight['departure_time']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='flight-detail'>{flight['from_city'].split('(')[0].strip()}</div>", unsafe_allow_html=True)
                    
                    with cols[1]:
                        duration = self.format_duration(flight['duration_mins'])
                        st.markdown(f"<div class='flight-duration'>{duration}</div>", unsafe_allow_html=True)
                        st.markdown("→", unsafe_allow_html=True)
                        
                    with cols[2]:
                        st.markdown(f"<div class='flight-time'>{flight['arrival_time']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='flight-detail'>{flight['to_city'].split('(')[0].strip()}</div>", unsafe_allow_html=True)
                
                with col3:
                    base_fare = flight['price']
                    taxes = int(base_fare * 0.18)
                    convenience_fee = 350
                    total_fare = base_fare + taxes + convenience_fee
                    st.markdown(f"<div class='flight-price'>₹{total_fare:,}</div>", unsafe_allow_html=True)
            
            # Return flight summary if applicable
            if 'return_flight_results' in st.session_state and st.session_state.return_flight_results and st.session_state.selected_return_flight is not None:
                st.markdown("<div class='divider'><div class='divider-line'></div><div class='divider-text'>RETURN FLIGHT</div><div class='divider-line'></div></div>", unsafe_allow_html=True)
                
                flight = st.session_state.return_flight_results[st.session_state.selected_return_flight]
                
                col1, col2, col3 = st.columns([2, 3, 1])
                
                with col1:
                    st.markdown(f"<div class='airline-name'>{flight['airline']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='flight-detail'>{flight['flight_number']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='flight-detail'>{flight['date']}</div>", unsafe_allow_html=True)
                
                with col2:
                    cols = st.columns([2, 1, 2])
                    with cols[0]:
                        st.markdown(f"<div class='flight-time'>{flight['
