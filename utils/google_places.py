import googlemaps
import os
import json
import csv

from dotenv import load_dotenv

## Get places function, returns a list of places
load_dotenv(override=True)

gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))

def get_places(city, place_type="restaurant"):
    ## Get coordinates of city
    geocode_result = gmaps.geocode(city)
    if geocode_result:
        ## Get coordinates of the city
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        
        ## restaurants nearby
        places_results = gmaps.places_nearby((lat, lng), radius=10000, type=place_type)        
        
        ## Get the names
        places = []
        service_fields = [
            'serves_beer', 'serves_breakfast', 'serves_brunch', 
            'serves_dinner', 'serves_lunch', 'serves_vegetarian_food', 
            'serves_wine', 'takeout'
        ]
        
        for place in places_results.get('results',[]):
            name = place.get('name', 'N/A')
            rating = place.get('rating', 'N/A')
            price_level = place.get('price_level', 'N/A')
            #location = place['geometry']['location']
            description = place.get('vicinity', 'No description available')
            place_id = place.get('place_id', None)
            types = place.get('types',None)
            n_ratings = place.get("user_ratings_total", 'N/A')
            types = types[0]
            
            ## get website and opeining hours 
            website = None
            opening_hours = None
            phone_number = None
            wheelchair = None
            services = {field: "N/A" for field in service_fields}
            
            if place_id:
                place_details = gmaps.place(place_id=place_id)
                website = place_details.get('result', {}).get('website', None)
                # Extract opening hours if available
                opening_hours = place_details.get('result', {}).get('opening_hours', {}).get('weekday_text', None)
                phone_number = place_details.get('result', {}).get('international_phone_number', "N/A")
                ## Features of the place
                wheelchair = place_details.get('result', {}).get('wheelchair_accessible_entrance', 'N/A')
                result_details = place_details.get('result', {})
                for field in service_fields:
                    services[field] = result_details.get(field, "N/A")
                
            places.append({
                'FSQ_ID': None,
                'Name': name,
                'Category': types,
                'Icon': None,
                "Latitude": None,
                "Longitude": None,
                "Region": None,
                "Formatted Address": description,
                "Description": f"Opening Hours {opening_hours} - Accessibility {wheelchair}",
                "Phone Number": phone_number,
                'Rating': rating,
                'Price': price_level,
                "Tips": None
            })
            
        ## Save the places into csv
        with open("data/google_places.csv", "w", newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=places[0].keys())
            writer.writeheader()
            writer.writerows(places)
    
        return places
    else:
        print("place not found")
        
if __name__ == "__main__":
    get_places(city="Luxembourg")