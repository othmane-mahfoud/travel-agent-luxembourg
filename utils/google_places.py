import googlemaps
import os
import json
import csv

## Get places function, returns a list of places

gmaps = googlemaps.Client(key=os.getenv("MAPS_API"))

def get_places(city, place_type="restaurant"):
    ## Get coordinates of city
    geocode_result = gmaps.geocode(city)
    if geocode_result:
        ## Get coordinates of the city
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        
        ## restaurants nearby
        places_results = gmaps.places_nearby((lat, lng), radius=1000, type=place_type)
        # Guardar los resultados en un archivo JSON
        with open("places_results.json", "w") as json_file:
            json.dump(places_results, json_file, indent=4)  # Save the places_results as a JSON file
        
        
        ## Get the names
        places = []
        
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
            if place_id:
                place_details = gmaps.place(place_id=place_id)
                website = place_details.get('result', {}).get('website', None)
                # Extract opening hours if available
                opening_hours = place_details.get('result', {}).get('opening_hours', {}).get('weekday_text', None)
                phone_number = place_details.get('result', {}).get('formatted_phone_number', "N/A")

            
            places.append({
                'name': name,
                'rating': rating,
                'n_ratings' : n_ratings,
                'price_level': price_level,
                'type': types,
                'location': description,
                'website': website,
                'opening_hours': opening_hours,
                'phone_number': phone_number
            })
            
        ## Save the places into csv
        with open("places.csv", "w", newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=places[0].keys())
            writer.writeheader()
            writer.writerows(places)
        
        
        return places
    else:
        print("place not found")
    



