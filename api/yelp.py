import requests
import pprint


def search_yelp_business_restaurants(
        location,
    yelp_api_key=None
):
    url = "https://api.yelp.com/v3/businesses/search"
    querystring = {
        "location": location,
        "sorted_by": "best_match",
        "limit": 3
    }
    headers = {
        'Authorization': f'Bearer {yelp_api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, params=querystring)
    print(response.status_code)
    print(response.json())
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    results = response.json()
    return results



def search_yelp_fusion_restaurants(
        food_category, 
        location,
    yelp_api_key=None
):
    url = "https://api.yelp.com/ai/chat/v2"
    
    payload = {
        "query": "What's a good " + food_category + " place in " + location + "?",
    }
    headers = {
        'Authorization': f'Bearer {yelp_api_key}',
        'Content-Type': 'application/json'
    }
    json_payload = json.dumps(payload)
    response = requests.post(url, headers=headers, data=json_payload)
    # print(response.status_code)
    # print(response.json())
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    results = response.json()
    return results


def display_yelp_fusion_results(response_json):
    results = ""
    response_text = response_json.get('response', {}).get('text', 'No response text provided.')
    entities = response_json.get('entities', [])
    
    # print(f"\n{response_text}\n" + "="*60)
    results += f"\n{response_text}\n" + "="*60
    results += "\n"
    
    if not entities:
        # print("No businesses found.")
        results += "No businesses found."
        return

    businesses = entities[0].get('businesses', [])
    
    if not businesses:
        # print("No businesses listed.")
        results += "No businesses listed."
        return
    
    for idx, business in enumerate(businesses, 1):
        name = business.get('name', 'Unknown')
        url = business.get('url', '#')
        address = business.get('location', {}).get('formatted_address', 'Address not available')
        phone = business.get('phone', 'Phone not available')
        rating = business.get('rating', 'No rating')
        review_count = business.get('review_count', 'No reviews')
        price = business.get('price', 'Price not listed')
        categories = [cat.get('title') for cat in business.get('categories', [])]
        specialties = business.get('attributes', {}).get('AboutThisBizSpecialties', 'No specialties mentioned.')
        summary = business.get('summaries', {}).get('short', 'No summary available.')
        delivery = business.get('attributes', {}).get('RestaurantsDelivery', False)
        takeout = business.get('attributes', {}).get('RestaurantsTakeOut', False)
        wheelchair_accessible = business.get('attributes', {}).get('WheelchairAccessible', False)
        
        # print(f"{idx}. {name}")
        # print(f"   📍 Address: {address}")
        # print(f"   📞 Phone: {phone}")
        # print(f"   ⭐ Rating: {rating} ({review_count} reviews)")
        # print(f"   💵 Price Range: {price}")
        # print(f"   🍽️ Categories: {', '.join(categories) if categories else 'Not specified'}")
        # print(f"   🛵 Delivery Available: {'Yes' if delivery else 'No'}")
        # print(f"   🥡 Takeout Available: {'Yes' if takeout else 'No'}")
        # print(f"   ♿ Wheelchair Accessible: {'Yes' if wheelchair_accessible else 'No'}")
        # print(f"   🛠️ Specialties: {specialties}")
        # print(f"   📖 Summary: {summary}")
        # print(f"   🔗 URL: {url}")
        # print("-" * 60)

        results += (f"{idx}. {name}\n")
        results += (f"   📍 Address: {address}\n")
        results += (f"   📞 Phone: {phone}\n")
        results += (f"   ⭐ Rating: {rating} ({review_count} reviews)\n")
        results += (f"   💵 Price Range: {price}\n")
        results += (f"   🍽️ Categories: {', '.join(categories) if categories else 'Not specified'}\n")
        results += (f"   🛵 Delivery Available: {'Yes' if delivery else 'No'}\n")
        results += (f"   🥡 Takeout Available: {'Yes' if takeout else 'No'}\n")
        results += (f"   ♿ Wheelchair Accessible: {'Yes' if wheelchair_accessible else 'No'}\n")
        results += (f"   🛠️ Specialties: {specialties}\n")
        results += (f"   📖 Summary: {summary}\n")
        results += (f"   🔗 URL: {url}\n")
        results += ("-" * 60)
        results += ("\n")

    return results


def display_businesses(data):
    businesses = data.get('businesses', [])
    if not businesses:
        print("No businesses found.")
        return

    for idx, biz in enumerate(businesses, start=1):
        name = biz.get('name', 'N/A')
        categories = ', '.join([cat['title'] for cat in biz.get('categories', [])])
        rating = biz.get('rating', 'N/A')
        price = biz.get('price', 'N/A')
        address = ', '.join(biz['location'].get('display_address', []))
        phone = biz.get('display_phone', 'N/A')
        url = biz.get('url', 'N/A')
        menu_url = biz.get('attributes', {}).get('menu_url', 'N/A')
        image_url = biz.get('image_url', 'N/A')

        print(f"--- Business #{idx} ---")
        print(f"Name: {name}")
        print(f"Categories: {categories}")
        print(f"Rating: {rating} ⭐")
        print(f"Price: {price}")
        print(f"Address: {address}")
        print(f"Phone: {phone}")
        print(f"Website: {url}")
        print(f"Menu: {menu_url}")
        print(f"Image: {image_url}")
        print()

if __name__ == "__main__":
    import os
    import json
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("YELP_API_KEY")
    
    if not api_key:
        print("Error: YELP_API_KEY not found in environment variables")
        exit(1)
    
    # Test search_yelp_business_restaurants function
    print("Testing search_yelp_business_restaurants function:")
    location = "San Francisco"
    print(f"Searching for restaurants in {location}...")
    results = search_yelp_business_restaurants(location=location, yelp_api_key=api_key)
    if results:
        display_businesses(results)
    else:
        print("No results found or an error occurred.")
    
    # Test search_yelp_fusion_restaurants function
    print("\nTesting search_yelp_fusion_restaurants function:")
    cuisine = "Italian"
    location = "San Francisco"
    print(f"Searching for {cuisine} restaurants in {location}...")
    results = search_yelp_fusion_restaurants(food_category=cuisine, location=location, yelp_api_key=api_key)
    if results:
        formatted_results = display_yelp_fusion_results(results)
        print(formatted_results)
    else:
        print("No results found or an error occurred.")
    
    # Test with different parameters
    print("\nTesting with different parameters:")
    cuisine = "Japanese"
    location = "New York"
    print(f"Searching for {cuisine} restaurants in {location}...")
    results = search_yelp_fusion_restaurants(food_category=cuisine, location=location, yelp_api_key=api_key)
    if results:
        formatted_results = display_yelp_fusion_results(results)
        print(formatted_results)
    else:
        print("No results found or an error occurred.")
