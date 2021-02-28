from time import sleep, ctime
import urllib.request as url
from urllib.error import URLError
import json, time
from geopy.distance import geodesic
try:
    from dbsql.dbconnections import *
except ModuleNotFoundError:
    from liveisstracker.dbsql.dbconnections import *
from geopy.geocoders import Nominatim
from mylogger.iss_logging import logger

geolocator = Nominatim(user_agent="my-application",timeout=3)


def get_home_location(home_name):
    location = geolocator.geocode(home_name)

    if not location:
        logger.error(f'"{home_name}" is not a valid city name')
        st.write('Not a valid location')
        raise Exception(': Streamlit not RUNNING')
    
    logger.info(location.address)
    logger.info("Latitude: "+location.raw['lat'])
    logger.info("Longitude: "+location.raw['lon'])

    return location.address, location.raw['lat'], location.raw['lon']

class TrackerISS:

    lat_pre = 0
    lon_pre = 0
    timestamp_pre = 0
    iss_link = 'http://api.open-notify.org/iss-now.json'

    def __init__(self):

        gps_location = self.get_iss_lat_lon()
        self.timestamp = gps_location['timestamp']
        self.latitude = gps_location['latitude']
        self.longitude = gps_location['longitude']

        try:
            logger.info('Establishing connection to DB')
            self.db_cnx = MySql()
        except Exception:
            logger.error('DB connection failed')
            self.db_cnx = None

    def insert_record_in_db(self, lat, lon, timestamp):

        if self.db_cnx is not None:
            self.db_cnx.insert_record('location',key_values={'lat':lat,'lon':lon,'datetime_id':timestamp})
    
    @staticmethod
    def get_distance_btwn_locations(location_1=None, location_2=None,testing_mode=None):
        
        if testing_mode:
            location_1 = testing_mode['location_1']
            location_2 = testing_mode['location_2']

        return geodesic(location_1,location_2).km

    @staticmethod
    def get_iss_lat_lon(testing_mode=None):

        try:
            if testing_mode:
                response = url.urlopen(testing_mode['iss_link'])
            else:
                response = url.urlopen(TrackerISS.iss_link)
            json_res = json.loads(response.read())
            geo_location = json_res['iss_position']
            timestamp = json_res['timestamp']
            lon, lat = float(geo_location['longitude']), float(geo_location['latitude'])
            logger.debug(f"Current ISS location at {ctime(int(timestamp))}: latitude: {lat}, longitude: {lon}")
            return {'timestamp':timestamp, 'latitude': lat,'longitude': lon}
        except URLError as e:
            raise e

    def get_speed_iss_pos(self,testing_mode=None):

        if testing_mode:
            self.timestamp = testing_mode['timestamp']
            self.latitude = testing_mode['latitude']
            self.longitude = testing_mode['longitude']
        else:

            gps_location = self.get_iss_lat_lon()
            self.timestamp = gps_location['timestamp']
            self.latitude = gps_location['latitude']
            self.longitude = gps_location['longitude']

            # Write location stats to DB
            self.insert_record_in_db(self.latitude, self.longitude, self.timestamp)

        # global lat_pre,lon_pre, self.timestamp_pre

        iss = (self.latitude, self.longitude)
        time_diff = self.timestamp - self.timestamp_pre
        distance = geodesic((self.lat_pre,self.lon_pre),iss).km
        self.lat_pre,self.lon_pre = iss
        self.timestamp_pre = self.timestamp

        try:
            speed = distance/time_diff*3600 # km/h
        except ZeroDivisionError:
            speed = 0
        except  Exception as e:
            logger.error(e)
            speed = 99999999999

        return [speed, iss]