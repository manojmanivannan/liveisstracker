# import ${python_package}
from ${python_package}.issTrack.issTracking import TrackerISS, get_city_location
import click
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from time import sleep


@click.command()
@click.option('--get-iss-location','-i', is_flag=True, help="Get the current location of International Space Station")
@click.option('--get-iss-speed','-s',is_flag=True, help="Get the current ground speed of International Space Station")
@click.option('--get-country','-c',is_flag=True, help="Get the country above which the ISS is current passing over")
def main(get_iss_location,get_iss_speed,get_country):

    location = TrackerISS(silent=True).gps_location

    if get_iss_location:
        location = TrackerISS(silent=True).gps_location
        print(f'Timestamp (UTC): {datetime.utcfromtimestamp(int(location["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")} ISS is at Lat:{location["latitude"]} Lon:{location["longitude"]}')

    if get_iss_speed:
        location_0 = location
        sleep(2)
        location_1 = TrackerISS(silent=True).gps_location
        time_diff = location_1['timestamp'] - location_0['timestamp']
        distance = geodesic((location_0['latitude'],location_0['longitude']),
                            (location_1['latitude'],location_1['longitude'])).km

        try:
            speed = distance/time_diff*3600 # km/h
        except ZeroDivisionError:
            speed = 0
        except  Exception as e:
            speed = 99999999999

        print(f'Ground Speed of International Space Station is ~ {round(speed,2)} Km/h')

    if get_country:

        geolocator = Nominatim(user_agent="my-application",timeout=3).reverse(f'{location["latitude"]},{location["longitude"]}',language='en')
        
        try:
            country = geolocator.raw['address']['country']
        except KeyError:
            country = 'the ocean'

        print(f'Internaionl Space Station is currently above {country}')

