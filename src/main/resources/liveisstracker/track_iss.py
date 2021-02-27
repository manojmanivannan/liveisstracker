"""
Author: Manoj Manivannan
Date 13-Jun-2020

This script plots the ground position of international space station on a spherical map.
The location of ISS is obtained from 'http://api.open-notify.org/iss-now.json'
The resulting Geo coordinates are plot using matplotlib.
"""

from datetime import datetime
import streamlit as st
from mylogger.iss_logging import logger
import sys
from issTrack.page_information import information
from issTrack.issTracking import *
from PlotMap.MapBasePlot import *

def main():
            
    try:
        st.title('International Space Station Tracker')
        st.markdown(information['header1'])
        st.markdown(information['what'])
        st.markdown(information['intro_source'],unsafe_allow_html=True)
        st.markdown(information['header2'])
        st.markdown(information['tech_spec'], unsafe_allow_html=True)
        st.markdown(information['intro_source'],unsafe_allow_html=True)
        home_name_st = st.text_input('Show location relative to',value='Modena Italy')
        home_name, home_lat, home_lon = get_home_location(home_name_st)

        iss = TrackerISS()
        earth = BasemapPlot(home_name,home_lat,home_lon)
        live_stop = st.button('Stop live tracking')
        while True:
            earth.plot_location(iss.get_speed_iss_pos())
            if live_stop:
                break
            time.sleep(5)

    except Exception as e:
        # logger.error('Failed {}'.format(e), file=sys.stderr )
        raise Exception(e)








if __name__ == '__main__':
    main()
