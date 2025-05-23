import requests
import json


def search_booking_destination(
    query,
    rapidapi_key=None
):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
    
    querystring = {
        "query": query,
    }
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print(response.status_code)
    # print(response.json())
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    results = response.json()
    return results


def search_booking_hotel(
    query,
    arrival_date,
    departure_date,
    adults,
    page_number,
    price_max,
    rapidapi_key=None
):
    url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
    response_json = search_booking_destination(query=query,rapidapi_key=rapidapi_key)
    # Extracting dest_id and search_type from the JSON response
    dest_info = [(item['dest_id'], item['search_type']) for item in response_json['data']]
    # print(dest_info)
    querystring = {
        "dest_id": dest_info[0][0],
        "search_type":dest_info[0][1],
        "arrival_date": arrival_date,
        "departure_date": departure_date,
        "adults": str(adults),
        "page_number": str(page_number),
        "price_max":str(price_max)
    }
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print(response.status_code)
    # print(response.json())
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    results = response.json()
    print(json.dumps(results, indent=4, sort_keys=True))
    return results



def display_booking_results(response_json):
    hotels = response_json.get('data', {}).get('hotels', [])
    results = ""
    if not hotels:
        # print("No booking hotels found.")
        results += "No booking hotels found."
        return
    
    # print(f"Found {len(hotels)} hotels:\n" + "="*60)
    results += f"Found {len(hotels)} hotels:\n" + "="*60 + "\n"
    
    for idx, item in enumerate(hotels, 1):
        accessibilityLabel = item.get('accessibilityLabel', {})
        # print(f"{idx}")
        # print(f"   🛏️Detail: {accessibilityLabel}")
        # print("-" * 60)
        results += (f"{idx}\n")
        results += (f"   🛏️Detail: {accessibilityLabel}\n")
        results += ("-" * 60)
        results += "\n"
    
    return results

if __name__ == "__main__":
    import os
    import json
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("RAPIDAPI_KEY")
    
    if not api_key:
        print("Error: RAPIDAPI_KEY not found in environment variables")
        exit(1)
    
    # Test search_booking_hotel function
    print("Testing search_booking_hotel function:")
    location = "Paris"
    checkin = "2025-08-01"
    checkout = "2025-08-05"
    adults = 2
    price_max = 300
    
    print(f"Searching for accommodations in {location} from {checkin} to {checkout}...")
    results = search_booking_hotel(
        query=location,
        arrival_date=checkin,
        departure_date=checkout,
        adults=adults,
        page_number=1,
        price_max=price_max,
        rapidapi_key=api_key
    )
    
    # Display the results
    if results:
        formatted_results = display_booking_results(results)
        print(formatted_results)
    else:
        print("No results found or an error occurred.")
    
    # Test with different parameters
    print("\nTesting with different parameters:")
    location = "Barcelona"
    checkin = "2025-09-10"
    checkout = "2025-09-15"
    adults = 3
    price_max = 400
    
    print(f"Searching for accommodations in {location} from {checkin} to {checkout}...")
    results = search_booking_hotel(
        query=location,
        arrival_date=checkin,
        departure_date=checkout,
        adults=adults,
        page_number=1,
        price_max=price_max,
        rapidapi_key=api_key
    )
    
    # Display the results
    if results:
        formatted_results = display_booking_results(results)
        print(formatted_results)
    else:
        print("No results found or an error occurred.")
