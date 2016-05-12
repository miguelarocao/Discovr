import googlemaps
import sys
from google import search
from datetime import datetime

# Fetch Gmaps server key from local file
with open('gmaps_server_api_key.txt', 'r') as f:
    key = f.read()

# Initialise Gmaps API
gmaps = googlemaps.Client(key = key)

# Geocoding an address
geocode_result = gmaps.geocode('Mountain View, CA')


# Query for a place with various parameters

ip = sys.argv[1:]
if len(ip) == 0:
    query = 'Billiards'
else:
    query = ip[0]    
# Catalina Grad Housing
lat = geocode_result[0]["geometry"]['location']['lat']
lng = geocode_result[0]["geometry"]['location']['lng']
location = (lat, lng)
min_price = 1
max_price = 3
open_now = False
lang = 'en_US'
radius = 1000

# Run query
places = gmaps.places(query, 
                      location = location,
                      radius = radius,
                      language = lang,
                      min_price= min_price,
                      max_price = max_price,
                      open_now = open_now,
                      #type = type
                      )

# Look up an address with reverse geocoding
size = len(places["results"])
results = []
for i in range (0, min(size,5)):
    results.append(places["results"][i]["name"])
    print places["results"][i]["name"] +  ":  " +  places["results"][i]["formatted_address"] 

#for result in results:

    #for url in search(result, stop=1):
#           print(url)
    
    
    # Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",)    

