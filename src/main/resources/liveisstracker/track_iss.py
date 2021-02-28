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
import sys,os
from issTrack.page_information import information
from issTrack.issTracking import *
from PlotMap.MapBasePlot import *
import plotly.graph_objects as go
mapbox_access_token = open(os.getenv('MAPBOX_TOKEN')).read()

def main():
            
    try:
        st.title('International Space Station Tracker')
        st.markdown(information['header1'])
        st.markdown(information['what'])
        st.markdown(information['intro_source'],unsafe_allow_html=True)
        st.markdown(information['header2'])
        st.markdown(information['tech_spec'], unsafe_allow_html=True)
        st.markdown(information['intro_source'],unsafe_allow_html=True)
        iss = TrackerISS()
        live_show = st.radio("Show live tracking in orthographic",('Yes', 'No'), index=1)
        if live_show == 'Yes':
            home_name_st = st.text_input('Distance relative to (city)',value='')
            if home_name_st:
                home_name, home_lat, home_lon = get_home_location(home_name_st)
                
                earth = BasemapPlot(home_name,home_lat,home_lon)
        while live_show == 'Yes' and home_name_st:
            earth.plot_location(iss.get_speed_iss_pos())
            time.sleep(5)
        
        flat_show = st.radio("Show current poisition in flat view",('Yes', 'No'), index=0)
        if flat_show == 'Yes':
            
            location = iss.get_speed_iss_pos()

            latitude = location[1][0]
            longitude = location[1][1]
            fig = go.Figure(go.Scattermapbox(lat=[str(latitude)],lon=[str(longitude)],mode='markers',marker=go.scattermapbox.Marker(size=14)))
            if st.button('Refresh'):
                location = iss.get_speed_iss_pos()
                fig.update_layout(hovermode='closest',mapbox=dict(accesstoken=mapbox_access_token,bearing=0,
                                    center=go.layout.mapbox.Center(lat=location[1][0],lon=location[1][1]),pitch=0,zoom=1))
            st.plotly_chart(fig)
        

    except Exception as e:
        logger.error('Failed {}'.format(e))
        raise Exception(e)


if __name__ == '__main__':
    main()
