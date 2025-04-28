import os
import requests
from typing import Dict, Any, Optional, List

def call_tripadvisor_api(
    endpoint: str,
    params: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Make a call to the TripAdvisor API.
    
    Args:
        endpoint: The TripAdvisor API endpoint
        params: Dictionary of parameters to send with the request
        api_key: TripAdvisor API key (defaults to environment variable)
        
    Returns:
        JSON response from the TripAdvisor API as a dictionary
    """
    base_url = "https://api.content.tripadvisor.com/api/v1/"
    
    # Use provided API key or get from environment
    if api_key is None:
        api_key = os.environ.get("TRIPADVISOR_API_KEY")
        if not api_key:
            raise ValueError("TripAdvisor API key not provided and not found in environment variables")
    
    # Add API key to headers
    headers = {
        "accept": "application/json"
    }
    
    params['key'] = api_key
    
    # Make the request
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    # Check if the request was successful
    response.raise_for_status()
    
    # Return the JSON response
    return response.json()

def search_attractions(
    location: str,
    category: Optional[str] = None,
    limit: int = 10,
    language: str = "en",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for attractions in a given location.
    
    Args:
        location: The location to search (e.g., "Paris, France")
        category: Optional category filter (e.g., "attractions", "restaurants")
        limit: Maximum number of results to return (default: 10)
        language: Language code for results (default: "en")
        api_key: TripAdvisor API key (optional)
        
    Returns:
        Search results for attractions
    """
    params = {
        "searchQuery": location,
        "language": language,
        "limit": limit
    }
    
    if category:
        params["category"] = category
    
    return call_tripadvisor_api("location/search", params, api_key)

def get_location_details(
    location_id: str,
    language: str = "en",
    currency: str = "USD",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific location.
    
    Args:
        location_id: TripAdvisor location ID
        language: Language code for results (default: "en")
        currency: Currency code for pricing (default: "USD")
        api_key: TripAdvisor API key (optional)
        
    Returns:
        Detailed information about the location
    """
    params = {
        "language": language,
        "currency": currency
    }
    
    return call_tripadvisor_api(f"location/{location_id}/details", params, api_key)

def search_tours(
    location_id: str,
    limit: int = 10,
    language: str = "en",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for tours and activities in a specific location.
    
    Args:
        location_id: TripAdvisor location ID
        limit: Maximum number of results to return (default: 10)
        language: Language code for results (default: "en")
        api_key: TripAdvisor API key (optional)
        
    Returns:
        Search results for tours and activities
    """
    params = {
        "language": language,
        "limit": limit
    }
    
    return call_tripadvisor_api(f"location/{location_id}/attractions", params, api_key)

def main():
    """
    Main function for testing the TripAdvisor API functionality.
    """
    print("Testing TripAdvisor API...")
    
    # Test location search
    try:
        print("\nTesting Location Search:")
        location_result = search_attractions("Seattle", limit=5)
        
        if location_result.get("data"):
            locations = location_result.get("data", [])
            print(f"Found {len(locations)} locations")
            if locations:
                for i, location in enumerate(locations, 1):
                    print(f"{i}. {location.get('name')} - {location.get('location_id')}")
                
                # Save first location ID for next tests
                first_location_id = locations[0].get('location_id')
        else:
            print("Location search error or no results")
    except Exception as e:
        print(f"Location search test failed: {e}")
        first_location_id = None
    
    # Test location details if we have a location ID
    if first_location_id:
        try:
            print("\nTesting Location Details:")
            details_result = get_location_details(first_location_id)
            
            if details_result:
                print(f"Name: {details_result.get('name')}")
                print(f"Address: {details_result.get('address_obj', {}).get('address_string')}")
                print(f"Rating: {details_result.get('rating')}/5.0 ({details_result.get('num_reviews')} reviews)")
                print(f"Description: {details_result.get('description', 'No description available')[:100]}...")
            else:
                print("Location details error or no results")
        except Exception as e:
            print(f"Location details test failed: {e}")
        
        # Test tours search
        try:
            print("\nTesting Tours Search:")
            tours_result = search_tours(first_location_id, limit=3)
            
            if tours_result.get("data"):
                tours = tours_result.get("data", [])
                print(f"Found {len(tours)} tours/attractions")
                if tours:
                    for i, tour in enumerate(tours, 1):
                        print(f"{i}. {tour.get('name')}")
                        print(f"   Rating: {tour.get('rating', 'N/A')}/5.0")
                        print(f"   Category: {tour.get('category', {}).get('name', 'N/A')}")
            else:
                print("Tours search error or no results")
        except Exception as e:
            print(f"Tours search test failed: {e}")

if __name__ == "__main__":
    main()