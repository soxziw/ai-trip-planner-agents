# ai-trip-planner-agents/api_integration.py

import os
import json
from api.airbnb import search_airbnb, display_airbnb_results
from api.booking import search_booking_hotel, display_booking_results
from api.yelp import search_yelp_fusion_restaurants, display_yelp_fusion_results
from api.tripadvisor import search_attractions, get_location_details, search_tours
from api.gmap import search_places, get_place_details, get_directions

class ApiManager:
    """Manages API calls and formats results for agent consumption"""
    
    def __init__(self):
        # Load API keys from environment variables
        self.yelp_api_key = os.environ.get("YELP_API_KEY")
        self.rapidapi_key = os.environ.get("RAPIDAPI_KEY")
        self.tripadvisor_api_key = os.environ.get("TRIPADVISOR_API_KEY")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
    
    def search_hotels_airbnb(self, location, checkin, checkout, adults=2, price_max=300, total_records=5):
        """Search for Airbnb accommodations"""
        try:
            results = search_airbnb(
                location=location,
                checkin=checkin,
                checkout=checkout,
                adults=adults,
                pricemax=price_max,
                totalrecords=total_records,
                rapidapi_key=self.rapidapi_key
            )
            
            if results:
                return display_airbnb_results(results)
            return "No Airbnb results found."
        except Exception as e:
            return f"Error retrieving Airbnb data: {str(e)}"
    
    def search_hotels_booking(self, location, checkin, checkout, adults=2, price_max=300, page_number=1):
        """Search for hotels on Booking.com"""
        try:
            results = search_booking_hotel(
                query=location,
                arrival_date=checkin,
                departure_date=checkout,
                adults=adults,
                page_number=page_number,
                price_max=price_max,
                rapidapi_key=self.rapidapi_key
            )
            
            if results:
                return display_booking_results(results)
            return "No Booking.com results found."
        except Exception as e:
            return f"Error retrieving Booking.com data: {str(e)}"
    
    def search_restaurants(self, cuisine, location):
        """Search for restaurants using Yelp Fusion API"""
        try:
            results = search_yelp_fusion_restaurants(
                food_category=cuisine,
                location=location,
                yelp_api_key=self.yelp_api_key
            )
            
            if results:
                return display_yelp_fusion_results(results)
            return "No restaurant results found."
        except Exception as e:
            return f"Error retrieving restaurant data: {str(e)}"
    
    def search_attractions(self, location, category=None, limit=10):
        """Search for attractions using TripAdvisor API"""
        try:
            results = search_attractions(
                location=location,
                category=category,
                limit=limit,
                api_key=self.tripadvisor_api_key
            )
            
            attractions = []
            if results and 'data' in results:
                for attraction in results['data']:
                    attractions.append({
                        'name': attraction.get('name', 'Unknown'),
                        'location_id': attraction.get('location_id', ''),
                        'location_string': attraction.get('location_string', ''),
                        'category': attraction.get('category', {}).get('name', 'Unknown')
                    })
                
                return json.dumps(attractions, indent=2)
            return "No attraction results found."
        except Exception as e:
            return f"Error retrieving attraction data: {str(e)}"
    
    def get_location_details(self, location_id):
        """Get TripAdvisor location details"""
        try:
            results = get_location_details(
                location_id=location_id,
                api_key=self.tripadvisor_api_key
            )
            
            if results:
                details = {
                    'name': results.get('name', 'Unknown'),
                    'description': results.get('description', 'No description available'),
                    'web_url': results.get('web_url', ''),
                    'address': results.get('address_obj', {}).get('address_string', 'Unknown'),
                    'rating': results.get('rating', 'No rating'),
                    'num_reviews': results.get('num_reviews', '0'),
                    'price_level': results.get('price_level', 'Unknown'),
                    'hours': results.get('hours', {}).get('weekday_text', [])
                }
                
                return json.dumps(details, indent=2)
            return "No location details found."
        except Exception as e:
            return f"Error retrieving location details: {str(e)}"
    
    def get_directions(self, origin, destination, mode="driving"):
        """Get directions using Google Maps API"""
        try:
            results = get_directions(
                origin=origin,
                destination=destination,
                mode=mode,
                api_key=self.google_api_key
            )
            
            if results and 'routes' in results and results['routes']:
                route = results['routes'][0]
                directions = {
                    'distance': route['legs'][0]['distance']['text'],
                    'duration': route['legs'][0]['duration']['text'],
                    'steps': []
                }
                
                for step in route['legs'][0]['steps']:
                    directions['steps'].append({
                        'instruction': step['html_instructions'],
                        'distance': step['distance']['text'],
                        'duration': step['duration']['text']
                    })
                
                return json.dumps(directions, indent=2)
            return "No directions found."
        except Exception as e:
            return f"Error retrieving directions: {str(e)}"