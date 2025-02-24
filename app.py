import streamlit as st
from datetime import datetime, timedelta
import random
import time
import base64

class EnhancedFlightBookingApp:
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
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/IndiGo_Airlines_logo.svg/512px-IndiGo_Airlines_logo.svg.png"
            },
            "Air India": {
                "code": "AI", 
                "color": "#e31837",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Air_India_Logo.svg/512px-Air_India_Logo.svg.png"
            },
            "SpiceJet": {
                "code": "SG", 
                "color": "#ff4e00",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/SpiceJet_logo.svg/512px-SpiceJet_logo.svg.png"
            },
            "Vistara": {
                "code": "UK", 
                "color": "#4b286d",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Vistara_Logo.svg/512px-Vistara_Logo.svg.png"
            },
            "Akasa Air": {
                "code": "QP", 
                "color": "#FF6D38",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Akasa_Air_logo.svg"
            },
            "Alliance Air": {
                "code": "9I", 
                "color": "#2B3990",
                "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Alliance_Air_India_Logo.svg/512px-Alliance_Air_India_Logo.svg.png"
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
        
        # Session state initialization
        if 'search_performed' not in st.session_state:
            st.session_state.search_performed = False
        if 'selected_flight' not in st.session_state:
            st.session_state.selected_flight = None
        if 'selected_return_flight' not in st.session_state:
            st.session_state.selected_return_flight = None
        if 'fare_details_open' not in st.session_state:
            st.session_state.fare_details_open = {}
        if 'fare_rules_open' not in st.session_state:
            st.session_state.fare_rules_open = {}
        if 'flight_results' not in st.session_state:
            st.session_state.flight_results = []
        if 'return_flight_results' not in st.session_state:
            st.session_state.return_flight_results = []
        if 'view_booking' not in st.session_state:
            st.session_state.view_booking = False
        if 'passengers' not in st.session_state:
            st.session_state.passengers = 1

    def get_placeholder_image(self):
        # Fallback placeholder for airline logos
        return "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1wbGFuZSI+PHBhdGggZD0iTTE3LjgxOCA0LjU5OGwxLjYtMS42YTEgMSAwIDEgMSAxLjQxNCAxLjQxNGwtMS42IDEuNmExIDEgMCAwIDEtMS40MTQtMS40MTR6Ii8+PHBhdGggZD0iTTEzIDMuNVYyYTEgMSAwIDAgMSAxLTFoMi45NTRhMS43OCAxLjc4IDAgMCAxIDEuNzggMS43OHYuNzJhMSAxIDAgMCAxLS41MTMuODc0bC0zLjc2IDEuOTU0QTExIDExIDAgMCAxIDbpV6mG9OUmJucmdCJ+ldx9eXcYbFGDnZXRib3g9IjAgMCAyNCAyNCI+YXCIn1sInRvdGFsIl19PC9wYXRoPjwvc3ZnPg=="

    def apply_custom_css(self):
        st.markdown("""
            <style>
                /* Main container styling */
                .main {
                    padding: 0;
                    margin: 0;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                
                /* Header styling */
                .header {
                    background: linear-gradient(135deg, #0d47a1, #42a5f5);
                    color: white;
                    padding: 20px;
                    margin: -1rem -1rem 2rem -1rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }
                
                /* Search box styling */
                .search-box {
                    background-color: white;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                    margin-bottom: 25px;
                    border: 1px solid #e0e0e0;
                }
                
                /* Flight card styling */
                .flight-card {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 15px 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    border: 1px solid #f0f0f0;
                    transition: all 0.3s ease;
                }
                
                .flight-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
                }
                
                /* Selected flight */
                .flight-card-selected {
                    border: 2px solid #1976d2;
                    background-color: #f5f9ff;
                }
                
                /* Airline logo */
                .airline-logo {
                    width: 40px;
                    height: 40px;
                    object-fit: contain;
                    margin-right: 12px;
                }
                
                /* Price styling */
                .price {
                    color: #d63b3b;
                    font-size: 22px;
                    font-weight: bold;
                }
                
                /* Flight details */
                .flight-details {
                    color: #4a4a4a;
                    font-size: 14px;
                }
                
                /* Duration line */
                .duration-line {
                    height: 2px;
                    background-color: #e0e0e0;
                    position: relative;
                    margin: 0 15px;
                    flex-grow: 1;
                }
                
                .duration-line::before,
                .duration-line::after {
                    content: '•';
                    position: absolute;
                    top: -8px;
                    color: #555;
                    font-size: 16px;
                }
                
                .duration-line::before {
                    left: -5px;
                }
                
                .duration-line::after {
                    right: -5px;
                }
                
                /* Duration text */
                .duration-text {
                    position: absolute;
                    top: -10px;
                    left: 50%;
                    transform: translateX(-50%);
                    background-color: white;
                    padding: 0 10px;
                    color: #555;
                    font-size: 12px;
                    font-weight: bold;
                }
                
                /* Button styling */
                .stButton>button {
                    background-color: #1976d2;
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 10px 20px;
                    width: 100%;
                    border-radius: 4px;
                    transition: all 0.2s ease-in-out;
                }
                
                .stButton>button:hover {
                    background-color: #1565c0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                }
                
                /* Trip type selector */
                .stRadio>label {
                    font-weight: bold;
                    color: #333;
                }
                
                /* Input labels */
                .stSelectbox>label, .stDateInput>label, .stNumberInput>label {
                    font-weight: bold;
                    color: #333;
                }
                
                /* Fare details */
                .fare-details {
                    background-color: #f5f9ff;
                    padding: 15px;
                    border-radius: 4px;
                    margin-top: 10px;
                    border: 1px solid #e0e0e0;
                }
                
                .fare-details-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    cursor: pointer;
                    padding: 8px 0;
                }
                
                .fare-rules {
                    background-color: #f9f9f9;
                    padding: 15px;
                    border-radius: 4px;
                    margin-top: 10px;
                    border: 1px solid #e0e0e0;
                }
                
                /* Tabs styling */
                .stTabs>div>div:first-child {
                    background-color: #f5f5f5;
                    border-radius: 8px 8px 0 0;
                }

                /* Filter section */
                .filter-section {
                    background-color: white;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                    border: 1px solid #f0f0f0;
                }
                
                /* View booking panel */
                .booking-panel {
                    background-color: #f8f8f8;
                    padding: 20px;
                    border-radius: 8px;
                    margin-top: 20px;
                    border: 1px solid #e0e0e0;
                }
                
                /* Progress bar */
                .booking-progress {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 30px;
                    position: relative;
                }
                
                .booking-step {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    z-index: 1;
                    position: relative;
                }
                
                .step-number {
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    background-color: #e0e0e0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: #555;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                
                .active-step .step-number {
                    background-color: #1976d2;
                    color: white;
                }
                
                .step-label {
                    font-size: 12px;
                    color: #555;
                }
                
                .active-step .step-label {
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
                    z-index: 0;
                }
                
                .progress-line-active {
                    position: absolute;
                    top: 15px;
                    left: 15%;
                    width: 0%;
                    height: 2px;
                    background-color: #1976d2;
                    z-index: 0;
                    transition: width 0.3s ease;
                }
                
                /* Badge styles */
                .badge {
                    display: inline-block;
                    padding: 3px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: bold;
                    margin-left: 8px;
                }
                
                .badge-blue {
                    background-color: #e3f2fd;
                    color: #1976d2;
                }
                
                .badge-green {
                    background-color: #e8f5e9;
                    color: #2e7d32;
                }
                
                .badge-orange {
                    background-color: #fff3e0;
                    color: #e65100;
                }
                
                /* Convenience fee tooltip */
                .tooltip {
                    position: relative;
                    display: inline-block;
                    cursor: help;
                    margin-left: 5px;
                }
                
                .tooltip .tooltiptext {
                    visibility: hidden;
                    width: 200px;
                    background-color: #555;
                    color: #fff;
                    text-align: center;
                    border-radius: 6px;
                    padding: 5px;
                    position: absolute;
                    z-index: 1;
                    bottom: 125%;
                    left: 50%;
                    margin-left: -100px;
                    opacity: 0;
                    transition: opacity 0.3s;
                }
                
                .tooltip:hover .tooltiptext {
                    visibility: visible;
                    opacity: 1;
                }
                
                /* Travel time progress */
                .progress-container {
                    background-color: #f0f0f0;
                    border-radius: 10px;
                    height: 4px;
                    width: 100%;
                    margin: 0 10px;
                    position: relative;
                }
                
                .progress-bar {
                    background-color: #1976d2;
                    height: 4px;
                    border-radius: 10px;
                    position: absolute;
                    left: 0;
                    width: 100%;
                }
            </style>
        """, unsafe_allow_html=True)

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

    def create_flight_card(self, flight, from_city, to_city, index, is_return=False):
        airline = flight["airline"]
        color = self.airlines[airline]["color"]
        logo = self.airlines[airline].get("logo", self.get_placeholder_image())
        
        # Calculate flight duration
        duration_mins = self.get_flight_time_in_minutes(flight["departure_time"], flight["arrival_time"])
        duration_text = self.format_duration(duration_mins)
        
        # Determine if this flight is selected
        flight_key = f"flight_{index}{'_return' if is_return else ''}"
        selected_class = ""
        
        if (is_return and st.session_state.selected_return_flight == index) or \
           (not is_return and st.session_state.selected_flight == index):
            selected_class = "flight-card-selected"
        
        # Convenience Fee
        convenience_fee = 350
        
        # Calculate total amount
        base_fare = flight['price']
        taxes = int(base_fare * 0.18)  # GST
        total_fare = base_fare + taxes + convenience_fee
        
        # Format for fare breakdown
        fare_breakdown = {
            "Base Fare": f"₹{base_fare:,}",
            "Taxes & Fees": f"₹{taxes:,}",
            "Convenience Fee": f"₹{convenience_fee}",
            "Total Amount": f"₹{total_fare:,}"
        }
        
        # Create card HTML
        card = f"""
            <div class="flight-card {selected_class}" id="{flight_key}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center;">
                        <img src="{logo}" class="airline-logo" alt="{airline}"/>
                        <div>
                            <div style="font-weight: bold">{airline}</div>
                            <div class="flight-details">{flight['flight_number']}</div>
                        </div>
                        <span class="badge badge-blue">{flight['class']}</span>
                    </div>
                    <div style="text-align: right">
                        <div class="price">₹{total_fare:,}</div>
                        <div class="flight-details">per passenger</div>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; margin: 15px 0;">
                    <div style="text-align: center">
                        <div style="font-weight: bold; font-size: 18px;">{flight['departure_time']}</div>
                        <div class="flight-details">{from_city.split('(')[0].strip()}</div>
                        <div class="flight-details">{from_city.split('(')[1].replace(')', '')}</div>
                    </div>
                    
                    <div style="position: relative; display: flex; align-items: center; flex-grow: 1; margin: 0 15px;">
                        <div class="duration-line">
                            <div class="duration-text">{duration_text}</div>
                        </div>
                    </div>
                    
                    <div style="text-align: center">
                        <div style="font-weight: bold; font-size: 18px;">{flight['arrival_time']}</div>
                        <div class="flight-details">{to_city.split('(')[0].strip()}</div>
                        <div class="flight-details">{to_city.split('(')[1].replace(')', '')}</div>
                    </div>
                </div>
        """
        
        # Add Fare Details and Rules accordions
        fare_id = f"fare_{index}{'_return' if is_return else ''}"
        rules_id = f"rules_{index}{'_return' if is_return else ''}"
        
        fare_details_open = st.session_state.fare_details_open.get(fare_id, False)
        fare_rules_open = st.session_state.fare_rules_open.get(rules_id, False)
        
        fare_details_button = "▼" if fare_details_open else "▶"
        fare_rules_button = "▼" if fare_rules_open else "▶"
        
        card += f"""
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <div class="fare-details-header" onclick="toggleSection('{fare_id}')">
                        <span style="font-weight: bold;">Fare Breakup</span>
                        <span id="fare_toggle_{fare_id}">{fare_details_button}</span>
                    </div>
                    <div class="fare-details-header" onclick="toggleSection('{rules_id}')">
                        <span style="font-weight: bold;">Fare Rules</span>
                        <span id="rules_toggle_{rules_id}">{fare_rules_button}</span>
                    </div>
                </div>
        """
        
        # Fare Details Section
        fare_display = "block" if fare_details_open else "none"
        card += f"""
                <div id="{fare_id}" class="fare-details" style="display: {fare_display};">
                    <table style="width: 100%;">
                        <tr>
                            <td style="padding: 5px; font-weight: bold;">Base Fare:</td>
                            <td style="padding: 5px; text-align: right;">{fare_breakdown['Base Fare']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; font-weight: bold;">Taxes & Fees:</td>
                            <td style="padding: 5px; text-align: right;">{fare_breakdown['Taxes & Fees']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; font-weight: bold;">
                                Convenience Fee
                                <div class="tooltip">ⓘ
                                    <span class="tooltiptext">This fee helps us provide you with a seamless booking experience.</span>
                                </div>
                            </td>
                            <td style="padding: 5px; text-align: right;">{fare_breakdown['Convenience Fee']}</td>
                        </tr>
                        <tr style="border-top: 1px solid #e0e0e0;">
                            <td style="padding: 5px; font-weight: bold;">Total Amount:</td>
                            <td style="padding: 5px; text-align: right; font-weight: bold;">{fare_breakdown['Total Amount']}</td>
                        </tr>
                    </table>
                </div>
        """
        
        # Fare Rules Section
        rules_display = "block" if fare_rules_open else "none"
        fare_class = flight['class']
        rules = self.fare_rules[fare_class]
        
        card += f"""
                <div id="{rules_id}" class="fare-rules" style="display: {rules_display};">
                    <table style="width: 100%;">
                        <tr>
                            <td style="padding: 5px; font-weight: bold;">Cancellation Fee:</td>
                            <td style="padding: 5px;">{rules['Cancellation Fee']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; font-weight: bold;">Date Change Fee:</td>
                            <td style="padding: 5px;">{rules['Date Change Fee']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; font-weight: bold;">Seat Selection:</td>
                            <td style="padding: 5px;">{rules['Seat Selection']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; font-weight: bold;">Baggage Allowance:</td>
                            <td style="padding: 5px;">{rules['Baggage Allowance']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; font-weight: bold;">Meal:</td>
                            <td style="padding: 5px;">{rules['Meal']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 5px; font-weight: bold;">Refundable:</td>
                            <td style="padding: 5px;">{rules['Refundable']}</td>
                        </tr>
                    </table>
                </div>
        """
        
        # Add select button and close card
        select_button_label = "SELECT FLIGHT"
        
        card += f"""
                <div style="display: flex; justify-content: center; margin-top: 15px;">
                    <button type="button" 
                        onclick="selectFlight({index}, {'true' if is_return else 'false'})" 
                        style="background-color: #1976d2; color: white; font-weight: bold; border: none; padding: 10px 20px; width: 80%; border-radius: 4px; cursor: pointer;">
                        {select_button_label}
                    </button>
                </div>
            </div>
        """
        
        return card

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

    def generate_flights(self, from_city, to_city, date, count=10):
        """Generate multiple flights between cities"""
        flights = []
