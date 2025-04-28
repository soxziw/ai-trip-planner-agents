import requests


# Define a function to search Airbnb
def search_airbnb(
    location,
    checkin,
    checkout,
    adults,
    pricemax,
    totalrecords,
    rapidapi_key=None
):
    url = "https://airbnb19.p.rapidapi.com/api/v1/searchPropertyByLocationV2"
    
    querystring = {
        "location": location,
        "checkin": checkin,
        "checkout": checkout,
        "adults": str(adults),
        "totalRecords": str(totalrecords),
        "currency": "USD",
        "priceMax": str(pricemax),
    }
    # print("rapidapi_key:",rapidapi_key)
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "airbnb19.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print(response.status_code)
    # print(response.json())
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    results = response.json()
    return results


def display_airbnb_results(response_json):
    results = ""
    listings = response_json.get('data', {}).get('list', [])
    
    if not listings:
        # print("No airbnb listings found.")
        results += "No airbnb listings found."
        return
    
    # print(f"Found {len(listings)} listings:\n" + "="*60)
    results += f"Found {len(listings)} listings:\n" + "="*60 + "\n"
    
    for idx, item in enumerate(listings, 1):
        listing_info = item.get('listing', {})
        pricing_info = item.get('pricingQuote', {})
        
        name = listing_info.get('name', 'Unknown')
        city = listing_info.get('city', 'Unknown')
        rating = listing_info.get('avgRatingLocalized', 'No Rating')
        room_type = listing_info.get('roomTypeCategory', 'Unknown')
        url = listing_info.get('webURL', '#')
        
        price_info = pricing_info.get('structuredStayDisplayPrice', {}).get('primaryLine', {})
        price = price_info.get('price', 'N/A')
        
        # Display nicely
        # print(f"{idx}. {name} ({city})")
        # print(f"   🛏️ Room Type: {room_type}")
        # print(f"   💵 Price: {price} per night")
        # print(f"   ⭐ Rating: {rating}")
        # print(f"   🔗 Link: {url}")
        # print("-" * 60)

        results += (f"{idx}. {name} ({city})\n")
        results += (f"   🛏️ Room Type: {room_type}\n")
        results += (f"   💵 Price: {price} per night\n")
        results += (f"   ⭐ Rating: {rating}\n")
        results += (f"   🔗 Link: {url}\n")
        results += ("-" * 60)
        results += "\n"
    return results
