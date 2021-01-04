"""
Author: Manoj Manivannan
Date 13-Jun-2020

This script plots the ground position of international space station on a spherical map.
The location of ISS is obtained from 'http://api.open-notify.org/iss-now.json'
The resulting Geo coordinates are plot using matplotlib.
"""
from time import sleep
import urllib.request as url
from urllib.error import URLError
import json, os
try:
    from dbsql.dbconnections import *
except ModuleNotFoundError:
    from liveisstracker.dbsql.dbconnections import *

from mpl_toolkits.basemap import Basemap # pip does not include this package, install by downloading the binary from web
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg' # point to the extracted exe file of ffmpeg
import matplotlib.animation as animate
import numpy as np
from geopy.distance import geodesic
from datetime import datetime
from geopy.geocoders import Nominatim
import streamlit as st
import sys
from streamlit.ReportThread import add_report_ctx
from threading import currentThread
from LoopClass import LoopTh
import pickle
import logging
#FORMAT = '%(asctime)s - %(levelname)s %(message)s'
#logging.basicConfig(format=FORMAT)
logger = logging.getLogger('LiveISStracker')
logger.propagate = False
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

geolocator = Nominatim(user_agent="my-application",timeout=3)

###### MODENA #######################
#home_name="MODENA"
home_lat=44.6501557
home_lon=10.8516923
#####################################
count = 0
#####################################

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
            self.db_cnx = MySql()
        except Exception:
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
            print(e)
            speed = 99999999999

        return [speed, iss]

class BasemapPlot:

    def __init__(self, home_name,home_latitude, home_longitude, map_type):

        self.home_name = home_name
        self.home_latitude = home_latitude
        self.home_longitude = home_longitude
        self.map_type = map_type

        # self.gps_location = gps_location

        figure, ax = plt.subplots(num="ISS Tracker",figsize=(14,8))
        self.the_plot = st.pyplot(plt,clear_figure=True)

    def create_plot(self,projection_type):
        self.gps_location = TrackerISS.get_iss_lat_lon()

        try:
            if projection_type == 'mill':
                logger.info('Projection type = mill')
                if os.path.isfile('millmap.pickle'):
                    self.m = pickle.load(open('millmap.pickle','rb'))
                else:
                    self.m = Basemap(projection=projection_type,resolution='c')
                    self.m.fillcontinents(color='coral',lake_color='aqua')
                    # draw parallels and meridians
                    #self.m.drawparallels(np.arange(-90.,91.,30.))
                    #self.m.drawmeridians(np.arange(-180.,181.,60.))
                    self.m.drawcountries()
                    self.m.drawmapboundary(fill_color='aqua')
                    pickle.dump(self.m,open('millmap.pickle','wb'),-1)
            else:
                self.m = Basemap(projection=projection_type,
                        lat_0=self.gps_location['latitude'],
                        lon_0=self.gps_location['longitude'],
                        resolution='c')

                self.m.fillcontinents(color='coral',lake_color='aqua')
                # draw parallels and meridians
                self.m.drawparallels(np.arange(-90.,91.,30.))
                self.m.drawmeridians(np.arange(-180.,181.,60.))
                self.m.drawcountries()
                self.m.drawmapboundary(fill_color='aqua')
            return self
        except Exception as e:
            print('Failure in basemap',e)

    def plot_location(self, speed_iss_pos):

        speed = speed_iss_pos[0]
        iss = speed_iss_pos[1]
        if self.map_type == 'Orthogonal':
            self.create_plot(projection_type='ortho')
            # pickle.dump(self.m,open('map.pickle','wb'),-1)
        else:
            self.create_plot(projection_type='mill')
            #self.m = pickle.load(open('map.pickle','rb'))
            #self.gps_location = TrackerISS.get_iss_lat_lon()
        x_pt, y_pt = self.m(self.gps_location['longitude'],self.gps_location['latitude'])
        self.point = self.m.plot(x_pt, y_pt,'bo')[0]
        self.point.set_data(x_pt,y_pt)
        plt.text(x_pt, y_pt, 'Lat:{} Lon:{}'.\
            format(\
                round(self.gps_location['latitude'],2),\
                round(self.gps_location['longitude'],2)))

        distance_to_home = TrackerISS.get_distance_btwn_locations(location_1 = (self.home_latitude, self.home_longitude),\
                                                                    location_2 = iss)
         
        location = Nominatim(user_agent="my-application",timeout=3)\
        .reverse('{},{}'.format(self.gps_location['latitude'],\
            self.gps_location['longitude']), language='en')
        try:
            country = location.raw['address']['country']
        except KeyError:
            country = 'the ocean'

        plt.title('ISS is currently above {} \n \
            Ground distance between {} and ISS is {}km.\n \
            Ground speed {} km/h' \
            .format(country,self.home_name,round(distance_to_home,2),round(speed,2)))
        self.the_plot.pyplot(plt,clear_figure=True)

def main():
    logger.info('Starting thread')
            
    try:
        st.title('International Space Station Tracker')
        map_type = st.selectbox('Map type',('Flat','Orthogonal'))
        home_name_st = st.text_input('Home')
        home_name = home_name_st if home_name_st else 'Modena'
        a = TrackerISS()
        b = BasemapPlot(home_name,home_lat,home_lon,map_type)
        while True:
            sleep(5)
            b.plot_location(speed_iss_pos = a.get_speed_iss_pos())

    except Exception as e:
        print('Failed {}'.format(e), file=sys.stderr )





map_type = ''


if __name__ == '__main__':
    thread = LoopTh(target=main,)
    add_report_ctx(thread)
    thread.start()
    # Sleep few seconds for the thread to initialize before proceeding
    sleep(3)
    thread.join()
    