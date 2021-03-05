mapbox_access_token = 'pk.eyJ1IjoibWFub2ptYW5pdmFubmFuIiwiYSI6ImNrYW02YXVsZDBxcmUydXM5a3c1cWNxZDEifQ.lKTAI6NhJ-TfLxm6AziupQ'

import plotly.graph_objects as go
from mylogger.iss_logging import logger
import streamlit as st
from issTrack.issTracking import *
from time import sleep


# co_ordinate=iss.get_speed_iss_pos()
# latitude=co_ordinate[1][0]
# longitude=co_ordinate[1][1]

def PlotlyMap():
    mapbox_access_token = 'pk.eyJ1IjoibWFub2ptYW5pdmFubmFuIiwiYSI6ImNrYW02YXVsZDBxcmUydXM5a3c1cWNxZDEifQ.lKTAI6NhJ-TfLxm6AziupQ'
    iss = TrackerISS()
    location = iss.get_speed_iss_pos()
    latitude = location[1][0]
    longitude = location[1][1]
    fig = go.Figure(go.Scattermapbox(lat=[str(latitude)],lon=[str(longitude)],mode='markers',marker=go.scattermapbox.Marker(size=14)))
    fig.update_layout(hovermode='closest',mapbox=dict(accesstoken=mapbox_access_token,bearing=0,
                    center=go.layout.mapbox.Center(lat=latitude,lon=longitude),pitch=0,zoom=2))
    
    with st.empty():
        while True:
            sleep(5)
            location = iss.get_speed_iss_pos()
            latitude = location[1][0]
            longitude = location[1][1]
            # fig.update_geos({'lat':[latitude+1],'lon':[longitude+1]})
            fig.update({'data':[{'lat':[latitude],'lon':[longitude]}]},overwrite=False)
            fig.update_layout({'mapbox':{'center':go.layout.mapbox.Center(lat=latitude,lon=longitude)}},overwrite=False)

            # fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
            # fig.update_geos(projection_rotation=dict(lon=latitude, lat=latitude,roll=0),overwrite=False)
            # fig.update_geos(center=dict(lon=latitude, lat=latitude),overwrite=False)
            st.plotly_chart(fig, use_container_width=True)

def update_plotly(map_figure):
    iss = TrackerISS()
    location = iss.get_speed_iss_pos()
    latitude = location[1][0]
    longitude = location[1][1]
    map_figure.update({'data':[{'lat':[latitude],'lon':[longitude]}]},overwrite=False)
    map_figure.update_layout({'mapbox':{'center':go.layout.mapbox.Center(lat=latitude,lon=longitude)}},overwrite=False)
    return map_figure



