import googlemaps
import sys
#from google import search
from datetime import datetime

# Fetch Gmaps server key from local file
with open('gmaps_server_api_key.txt', 'r') as f:
    key = f.read()

# Initialise Gmaps API
gmaps = googlemaps.Client(key = key)


# Geocoding an address

Map = {}
for line in open('../wiki_to_gmap.txt'):
    listWords = line.split("\t")
    Map[listWords[0]] = listWords[1][:-1]


# Query for a place with various parameters

ip = sys.argv[1:]

if len(ip) == 0:
    query = 'Karaoke'
    radius = 1000
    address = 'Mountain View, CA'
elif len(ip) == 1:
    query = ip[0] 
    radius = 1000
    address = 'Mountain View, CA'
elif len(ip) == 2:
    query = ip[0]     
    address = ip[1]
    radius = 1000
else:    
    query = ip[0]     
    address = ip[1]
    radius = ip[2]

if query == "":
    query = 'Karaoke'    
if radius == "":
    query = 1000
if address == "":
    address = 'Mountain View, CA'         
    
geocode_result = gmaps.geocode(address)    
# Catalina Grad Housing
lat = geocode_result[0]["geometry"]['location']['lat']
lng = geocode_result[0]["geometry"]['location']['lng']
location = (lat, lng)
min_price = 1
max_price = 3
open_now = False
lang = 'en_US'

# Run query
places = gmaps.places(Map[query], 
                      location = location,
                      radius = radius,
                      language = lang,
                      min_price= min_price,
                      max_price = max_price,
                      open_now = open_now,
                  #    type = "restaurant"
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

