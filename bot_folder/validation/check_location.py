import pytz
from datetime import datetime
from geopy.geocoders import Nominatim

def get_location(latitude, longitude ) -> list:
    geolocator = Nominatim(user_agent='NominatimApi', timeout=10000)
    location_name = geolocator.reverse(str(latitude) + "," + str(longitude), language='en')
    address = location_name.raw['address']
    country = address.get('country', '')
    country_tz = datetime.now(pytz.timezone(country))
    country_utc_offset = str(country_tz)[-6:]
    country_utc_time = datetime.now(pytz.timezone(country)).strftime("%H:%M")
    defined_location = [country, country_utc_offset, country_utc_time]
    return defined_location
