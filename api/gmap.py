import os
import requests
from typing import Dict, Any, Optional, List, Tuple

def call_google_maps_api(
    endpoint: str,
    params: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Make a call to the Google Maps API.
    
    Args:
        endpoint: The Google Maps API endpoint (e.g., 'geocode/json', 'directions/json')
        params: Dictionary of parameters to send with the request
        api_key: Google Maps API key (defaults to environment variable)
        
    Returns:
        JSON response from the Google Maps API as a dictionary
    """
    base_url = "https://maps.googleapis.com/maps/api/"
    
    # Use provided API key or get from environment
    if api_key is None:
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        if not api_key:
            raise ValueError("Google Maps API key not provided and not found in environment variables")
    
    # Add API key to parameters
    params["key"] = api_key
    
    # Make the request
    response = requests.get(f"{base_url}{endpoint}", params=params)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Return the JSON response
    return response.json()

def geocode_address(address: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Geocode an address to get its coordinates.
    
    Args:
        address: The address to geocode
        api_key: Google Maps API key (optional)
        
    Returns:
        Geocoding results
    """
    params = {
        "address": address
    }
    
    return call_google_maps_api("geocode/json", params, api_key)

def get_directions(
    origin: str,
    destination: str,
    mode: str = "driving",
    waypoints: Optional[List[str]] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get directions between two locations.
    
    Args:
        origin: Starting location (address or lat,lng)
        destination: Ending location (address or lat,lng)
        mode: Transportation mode (driving, walking, bicycling, transit)
        waypoints: Optional list of waypoints
        api_key: Google Maps API key (optional)
        
    Returns:
        Directions results
    """
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode
    }
    
    if waypoints:
        params["waypoints"] = "|".join(waypoints)
    
    return call_google_maps_api("directions/json", params, api_key)
def search_nearby_places(
    location: str,
    radius: int = 1500,
    type: Optional[str] = None,
    keyword: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for nearby places around a location.
    
    Args:
        location: The location to search around (address or lat,lng)
        radius: Search radius in meters (default: 1500)
        type: Type of place (e.g., 'restaurant', 'hotel', 'tourist_attraction')
        keyword: Keyword to filter results
        api_key: Google Maps API key (optional)
        
    Returns:
        Nearby places search results
    """
    params = {
        "location": location,
        "radius": radius
    }
    
    if type:
        params["type"] = type
    
    if keyword:
        params["keyword"] = keyword
    
    return call_google_maps_api("place/nearbysearch/json", params, api_key)

def main():
    """
    Main function for testing the Google Maps API functionality.
    """
    print("Testing Google Maps API...")
    
    # Test geocoding
    try:
        print("\nTesting Geocoding:")
        geocode_result = geocode_address("1600 Amphitheatre Parkway, Mountain View, CA")
        
        if geocode_result.get("status") == "OK":
            location = geocode_result["results"][0]["geometry"]["location"]
            print(f"Coordinates: {location['lat']}, {location['lng']}")
        else:
            print(f"Geocoding error: {geocode_result.get('status')}")
    except Exception as e:
        print(f"Geocoding test failed: {e}")
    
    # Test directions
    try:
        print("\nTesting Directions:")
        directions_result = get_directions(
            "San Francisco, CA",
            "Los Angeles, CA"
        )
        
        if directions_result.get("status") == "OK":
            route = directions_result["routes"][0]
            distance = route["legs"][0]["distance"]["text"]
            duration = route["legs"][0]["duration"]["text"]
            print(f"Distance: {distance}")
            print(f"Duration: {duration}")
        else:
            print(f"Directions error: {directions_result.get('status')}")
    except Exception as e:
        print(f"Directions test failed: {e}")
        
    # Test nearby places
    try:
        print("\nTesting Nearby Places:")
        nearby_result = search_nearby_places(
            location="37.7749,-122.4194",  # San Francisco coordinates
            radius=1000,
            type="restaurant",
            keyword="pizza"
        )
        
        if nearby_result.get("status") == "OK":
            places = nearby_result.get("results", [])
            print(f"Found {len(places)} nearby places")
            if places:
                for i, place in enumerate(places[:3], 1):  # Show first 3 results
                    print(f"{i}. {place.get('name')} - {place.get('vicinity')}")
        else:
            print(f"Nearby places error: {nearby_result.get('status')}")
    except Exception as e:
        print(f"Nearby places test failed: {e}")

if __name__ == "__main__":
    main()
