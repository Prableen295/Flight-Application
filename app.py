import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd
import time
import base64
from PIL import Image
import io

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
        
        # Airline data with logos encoded as base64 to avoid external URL dependencies
        self.airlines = {
            "IndiGo": {
                "code": "6E", 
                "color": "#0052CC",
                "logo": self.get_indigo_logo()
            },
            "Air India": {
                "code": "AI", 
                "color": "#e31837",
                "logo": self.get_air_india_logo()
            },
            "SpiceJet": {
                "code": "SG", 
                "color": "#ff4e00",
                "logo": self.get_spicejet_logo()
            },
            "Vistara": {
                "code": "UK", 
                "color": "#4b286d",
                "logo": self.get_vistara_logo()
            },
            "Akasa Air": {
                "code": "QP", 
                "color": "#FF6D38",
                "logo": self.get_akasa_logo()
            },
            "Alliance Air": {
                "code": "9I", 
                "color": "#2B3990",
                "logo": self.get_alliance_logo()
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
    
    def get_indigo_logo(self):
        return "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAgNjAiPjxwYXRoIGZpbGw9IiMwMDUyQ0MiIGQ9Ik0yMCwxMGg2MHY0MEgyMFYxMHoiLz48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMzUsMjBoMzB2MjBIMzVWMjB6Ii8+PHBhdGggZmlsbD0iIzAwNTJDQyIgZD0iTTQ1LDI1aDEwdjEwSDQ1VjI1eiIvPjxwYXRoIGZpbGw9IiMwMDUyQ0MiIGQ9Ik0xMDUsMzBsLTUtMTBoMTBMMTA1LDMweiIvPjxwYXRoIGZpbGw9IiMwMDUyQ0MiIGQ9Ik0xMjUsMjBoLTE1djIwaDVWMzBoMTBjMywwLDUtMiw1LTV2MGMwLTMtMi01LTUtNVoiLz48cGF0aCBmaWxsPSIjMDA1MkNDIiBkPSJNMTQwLDIwaC01djIwaDVWMjBaIi8+PHBhdGggZmlsbD0iIzAwNTJDQyIgZD0iTTE2MCwyMGgtMTV2MjBoNVYzMGgxMGMzLDAsNS0yLDUtNXYwYzAtMy0yLTUtNS01WiIvPjwvc3ZnPg=="
    
    def get_air_india_logo(self):
        return "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAgNjAiPjxwYXRoIGZpbGw9IiNlMzE4MzciIGQ9Ik0xMDAsMTBjMjAsMCw0MCwxMCw0MCwzMGMwLDUtMTAsNS0xMCwwYzAtMTUtMTUtMjAtMzAtMjBzLTMwLDUtMzAsMjBjMCw1LTEwLDUtMTAsMEMxMCwyMCwzMCwxMCwxMDAsMTBaIi8+PHBhdGggZmlsbD0iI2UzMTgzNyIgZD0iTTUwLDQ1aDEwMHY1SDUwVjQ1WiIvPjxjaXJjbGUgZmlsbD0iI2UzMTgzNyIgY3g9IjEwMCIgY3k9IjMwIiByPSIxMCIvPjwvc3ZnPg=="
    
    def get_spicejet_logo(self):
        return "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAgNjAiPjxwYXRoIGZpbGw9IiNmZjRlMDAiIGQ9Ik0yMCwxMGg4MHY0MEgyMFYxMHoiLz48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMzUsMjVoNTB2MTBIMzVWMjV6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTExMCwzMGwtMTAtMjBoMjBMMTEwLDMweiIvPjxwYXRoIGZpbGw9IiNmZjRlMDAiIGQ9Ik0xMzAsMTBoNDB2NDBIMTMwVjEweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0xNDAsMjVoMjB2MTBoLTIwVjI1eiIvPjwvc3ZnPg=="
    
    def get_vistara_logo(self):
        return "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAgNjAiPjxwYXRoIGZpbGw9IiM0YjI4NmQiIGQ9Ik0yMCwxMGgxNjB2NDBIMjBWMTB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEwMCwxNWMxMCwwLDIwLDUsMjAsMTVjMCwxMC0xMCwxNS0yMCwxNXMtMjAtNS0yMC0xNUExNSwxNSwwLDAsMSwxMDAsMTVaIi8+PHBhdGggZmlsbD0iIzRiMjg2ZCIgZD0iTTEwMCwyNWM1LDAsNSw1LDAsNXMtNS01LDAtNVoiLz48cGF0aCBmaWxsPSIjZmZmIiBkPSJNNTAsMjBoMjB2MjBINTBWMjB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEzMCwyMGgyMHYyMGgtMjBWMjB6Ii8+PC9zdmc+"
    
    def get_akasa_logo(self):
        return "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAgNjAiPjxwYXRoIGZpbGw9IiNGRjZEMzgiIGQ9Ik0yMCwxMGgxNjB2NDBIMjBWMTB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTM1LDIwTDUwLDQwSDIwTDM1LDIweiIvPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik03MCwyMEw4NSw0MEg1NUw3MCwyMHoiLz48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMTA1LDIwTDEyMCw0MEg5MEwxMDUsMjB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTE0MCwyMEwxNTUsNDBIMTI1TDE0MCwyMHoiLz48L3N2Zz4="
    
    def get_alliance_logo(self):
        return "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAgNjAiPjxwYXRoIGZpbGw9IiMyQjM5OTAiIGQ9Ik0yMCwxMGgxNjB2NDBIMjBWMTB6Ii8+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTQwLDMwYzAtNSw1LTEwLDEwLTEwaDEwMGM1LDAsMTAsNSwxMCwxMHMtNSwxMC0xMCwxMEg1MEM0NSw0MCw0MCwzNSw0MCwzMFoiLz48cGF0aCBmaWxsPSIjMkIzOTkwIiBkPSJNNjAsMjVoMjB2MTBINjBWMjV6Ii8+PHBhdGggZmlsbD0iIzJCMzk5MCIgZD0iTTEwMCwyNWgyMHYxMGgtMjBWMjV6Ii8+PHBhdGggZmlsbD0iIzJCMzk5MCIgZD0iTTE0MCwyNWgyMHYxMGgtMjBWMjV6Ii8+PC9zdmc+"
    
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
        if 'show_fare_rules' not in st.session_state:
            st.session_state.show_fare_rules = {}
        if 'show_fare_breakup' not in st.session_state:
            st.session_state.show_fare_breakup = {}
        if 'progress_step' not in st.session_state:
            st.session_state.progress_step = 1
    
    def apply_custom_css(self):
        """Apply custom CSS styling for better UI"""
        st.markdown("""
        <style>
            .main {
                padding: 0 !important;
                margin: 0 !important;
            }
            
            .app-header {
                background: linear-gradient(135deg, #FF6D38, #FF4E00);
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
                border: 2px solid #FF6D38;
                background-color: #fff9f5;
            }
            
            .flight-time {
                font-size: 1.2rem;
                font-weight: bold;
            }
            
            .airline-name {
                font-weight: bold;
            }
            
            .flight-price {
                color: #FF4E00;
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
                background-color: #fff0eb;
                color: #FF4E00;
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
                width: 35px;
                height: 35px;
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
                background-color: #FF4E00;
                color: white;
            }
            
            .completed-step .step-circle {
                background-color: #4CAF50;
                color: white;
            }
            
            .step-title {
                font-size: 0.8rem;
                color: #616161;
                text-align: center;
            }
            
            .active-step .step-title {
                color: #FF4E00;
                font-weight: bold;
            }
            
            .completed-step .step-title {
                color: #4CAF50;
                font-weight: bold;
            }
            
            .progress-line {
                position: absolute;
                top: 17px;
                left: 15%;
                right: 15%;
                height: 2px;
                background-color: #e0e0e0;
                z-index: 1;
            }
            
            .progress-line-filled {
                position: absolute;
                top: 17px;
                left: 15%;
                height: 2px;
                background-color: #4CAF50;
                z-index: 1;
                transition: width 0.5s;
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
                background-color: #fff9f5;
                padding: 1rem;
                border-radius: 8px;
                margin-top: 1rem;
                border: 1px solid #ffe0d0;
            }
            
            .fare-rules {
                background-color: #f9f9f9;
                padding: 1rem;
                border-radius: 8px;
                margin-top: 1rem;
                border: 1px solid #e0e0e0;
            }
            
            .fare-breakup {
                background-color: #f9f9f9;
                padding: 1rem;
                border-radius: 8px;
                margin-top: 0.5rem;
                border: 1px solid #e0e0e0;
            }
            
            .fare-rule-item {
                display: flex;
                justify-content: space-between;
                padding: 0.5rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            
            .fare-rule-item:last-child {
                border-bottom: none;
            }
            
            .fare-breakup-item {
                display: flex;
                justify-content: space-between;
                padding: 0.5rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            
            .fare-breakup-item:last-child {
                border-bottom: none;
                font-weight: bold;
            }
            
            /* Button styling */
            .primary-button {
                background-color: #FF4E00;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                text-align: center;
                transition: background-color 0.3s;
            }
            
            .primary-button:hover {
                background-color: #E84600;
            }
            
            .secondary-button {
                background-color: #f0f0f0;
                color: #333;
                border: 1px solid #ddd;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            
            .secondary-button:hover {
                background-color: #e0e0e0;
            }
            
            .text-button {
                background: none;
                color: #FF4E00;
                border: none;
                padding: 0;
                font: inherit;
                cursor: pointer;
                outline: inherit;
                text-decoration: underline;
            }
            
            .link-button {
                color: #FF4E00;
                text-decoration: none;
                font-size: 0.9rem;
                cursor: pointer;
            }
            
            .link-button:hover {
                text-decoration: underline;
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
                border-left-color: #FF4E00;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            .logo-img {
                max-height: 30px;
                max-width: 80px;
            }
            
            .airline-logo-container {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            /* Booking summary styles */
            .booking-summary {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 1rem;
                margin-bottom: 1.5rem;
            }
            
            .booking-flight-info {
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid #f0f0f0;
            }
            
            .booking-flight-info:last-child {
                margin-bottom: 0;
                padding-bottom: 0;
                border-bottom: none;
            }
            
            .passenger-form {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
            }
            
            .passenger-section {
                margin-bottom: 1.5rem;
                padding-bottom: 1.5rem;
                border-bottom: 1px solid #f0f0f0;
            }
            
            .passenger-section:last-child {
                margin-bottom: 0;
                padding-bottom: 0;
                border-bottom: none;
            }
            
            .form-section-title {
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 1rem;
                color: #333;
            }
            
            .payment-method {
                padding: 1rem;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-bottom: 1rem;
                cursor: pointer;
                transition: border-color 0.3s;
            }
            
            .payment-method:hover {
                border-color: #FF4E00;
            }
            
            .payment-method.selected {
                border-color: #FF4E00;
                background-color: #fff9f5;
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
            
            /* Styling for the fare details toggle */
            .fare-details-toggle {
                display: flex;
                justify-content: space-between;
                padding: 0.5rem 0;
                cursor: pointer;
                font-size: 0.9rem;
                color: #FF4E00;
            }
            
            /* Arrival and departure styling */
            .date-info {
                font-size: 0.8rem;
                color: #616161;
                margin-top: 2px;
            }
            
            /* Tooltip styling */
            .tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
            }
            
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 200px;
                background-color: #333;
                color: white;
                text-align: center;
                border-radius: 4px;
                padding: 5px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -100px;
                opacity: 0;
                transition: opacity 0.3s;
                font-size: 0.8rem;
            }
            
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            
            /* Hide default Streamlit elements */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Improve form inputs */
            .stTextInput input, .stSelectbox select, .stDateInput input {
                padding: 0.5rem;
                border-radius: 4px;
                border: 1px solid #ddd;
            }
            
            .stTextInput input:focus, .stSelectbox select:focus, .stDateInput input:focus {
                border-color: #FF4E00;
                box-shadow: 0 0 0 2px rgba(255, 78, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)

    def generate_flights(self, from_city, to_city, date, count=10):
        """Generate random flight data"""
        flights = []
        
        # Get random times throughout the day
        departure_times = sorted([f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}" for _ in range(count)])
        
        for i in range(count):
            # Randomly select an airline
            airline = random.choice(list(self.airlines.keys()))
            airline_code = self.airlines[airline]["code"]
            
            # Generate random flight number
            flight_number = f"{airline_code} {random.randint(100, 999)}"
            
            # Assign departure time
            departure_time = departure_times[i]
            
            # Generate duration between 1h to 4h
            duration_mins = random.randint(60, 240)
            
            # Calculate arrival time
            departure_dt = datetime.strptime(departure_time, "%H:%M")
            arrival_dt = departure_dt + timedelta(minutes=duration_mins)
            arrival_time = arrival_dt.strftime("%H:%M")
            
            # Randomly select fare class
            fare_class = random.choice(self.fare_classes)
            
            # Assign price based on class
            if fare_class == "Economy":
                price = random.randint(2500, 5000)
            elif fare_class == "Premium Economy":
                price = random.randint(6000, 9000)
            else:  # Business
                price = random.randint(12000, 18000)
            
            # Create a flight
            flight = {
                "from_city": from_city,
                "to_city": to_city,
                "date": date,
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "airline": airline,
                "flight_number": flight_number,
                "price": price,
                "class": fare_class,
                "duration": self.format_duration(duration_mins),
                "duration_mins": duration_mins
            }
            
            flights.append(flight)
        
        return flights
    
    def filter_and_sort_flights(self, flights):
        """Filter and sort flight results based on user preferences"""
        # Filter by airline
        filtered = [f for f in flights if f["airline"] in st.session_state.filter_airlines]
        
        # Filter by class
        filtered = [f for f in filtered if f["class"] in st.session_state.filter_classes]
        
        # Sort flights
        if st.session_state.sort_by == "price":
            filtered.sort(key=lambda x: x["price"])
        elif st.session_state.sort_
