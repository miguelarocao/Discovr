import googlemaps
from datetime import datetime

# Fetch Gmaps server key from local file
with open('gmaps_server_api_key.txt', 'r') as f:
    key = f.read()

# Initialise Gmaps API
gmaps = googlemaps.Client(key = key)

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

# Query for a place with various parameters
query = 'museum'
# Catalina Grad Housing
location = (34.139974, -118.128759)
min_price = 1
max_price = 3
open_now = True
lang = 'en_US'
radius = 100

# type doesn't really work for a lot of cases
type = 'restaurant'

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