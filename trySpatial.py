from geopy.geocoders import Nominatim

# Create a geocoder object
geolocator = Nominatim(user_agent="my_app")

# Get the latitude and longitude of a location
location = geolocator.geocode("america")
latitude = location.latitude
longitude = location.longitude

print("Latitude:", latitude)
print("Longitude:", longitude)
