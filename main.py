"""
Live ISS Tracker - Interactive 3D globe showing the International Space Station's location

Author: Manoj Manivannan
Dash + Flask implementation for truly async updates
"""

import json
import urllib.request as url
from datetime import datetime
from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as go
from geopy.geocoders import Nominatim

# Constants
ISS_API_URL = 'http://api.open-notify.org/iss-now.json'

# Initialize geocoder
geolocator = Nominatim(user_agent="liveisstracker", timeout=3)


def get_iss_location():
    """Fetch current ISS location from API"""
    try:
        response = url.urlopen(ISS_API_URL)
        data = json.loads(response.read())
        return {
            'latitude': float(data['iss_position']['latitude']),
            'longitude': float(data['iss_position']['longitude']),
            'timestamp': data['timestamp']
        }
    except Exception as e:
        print(f"Error fetching ISS location: {e}")
        return None




def create_3d_globe(iss_lat, iss_lon):
    """Create 3D globe visualization with ISS marker"""
    
    fig = go.Figure()

    # Add shadow/glow effect
    fig.add_trace(go.Scattergeo(
        lon=[iss_lon],
        lat=[iss_lat],
        mode='markers',
        marker=dict(
            size=30,  # Larger than the main marker
            color='rgba(255, 0, 0, 0.3)',  # Semi-transparent red
            symbol='circle',
        ),
        name='ISS Shadow',
        hoverinfo='none' # Don't show hover info for the shadow
    ))
    
    # Add ISS marker
    fig.add_trace(go.Scattergeo(
        lon=[iss_lon],
        lat=[iss_lat],
        mode='markers+text',
        marker=dict(
            size=15,
            color='red',
            symbol='circle',
            line=dict(width=2, color='white')
        ),
        text=['🛰️ ISS'],
        textposition='top center',
        textfont=dict(size=16, color='red'),
        name='ISS Location',
        hovertemplate='<b>International Space Station</b><br>' +
                      'Latitude: %{lat:.2f}°<br>' +
                      'Longitude: %{lon:.2f}°<br>' +
                      '<extra></extra>'
    ))
    
    # Configure the globe projection centered on ISS initially
    fig.update_geos(
        projection_type='orthographic',
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor='rgb(243, 243, 243)',
        coastlinecolor='rgb(204, 204, 204)',
        countrycolor='rgb(204, 204, 204)',
        showocean=True,
        oceancolor='rgb(230, 245, 255)',
        showlakes=True,
        lakecolor='rgb(230, 245, 255)',
        projection_rotation=dict(
            lon=iss_lon,
            lat=iss_lat,
            roll=0
        )
    )
    
    # Update layout with uirevision to preserve user interactions
    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=40, b=0),
        title=dict(
            text='🛰️ International Space Station - Live Location',
            x=0.5,
            xanchor='center',
            font=dict(size=20)
        ),
        showlegend=False,
        uirevision='constant',  # Preserve UI state across updates
        paper_bgcolor='#f8f9fa',
        geo=dict(bgcolor='#f8f9fa')
    )
    
    return fig





# Initialize Dash app
app = Dash(__name__)
app.title = "Live ISS Tracker"

# App layout
app.layout = html.Div([
    html.Div([
        html.H1('🛰️ International Space Station Tracker', 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
        
        html.Div([
            html.H3('About the International Space Station', style={'color': '#34495e'}),
            html.P([
                'The ', html.B('International Space Station (ISS)'), 
                ' is a modular space station in low Earth orbit. '
                "It's a multinational collaborative project involving NASA, Roscosmos, JAXA, ESA, and CSA."
            ]),
            html.Ul([
                html.Li('Orbit altitude: ~408 km (254 miles)'),
                html.Li('Orbital speed: ~27,600 km/h (17,100 mph)'),
                html.Li('Completes one orbit: Every ~90 minutes'),
            ]),
            html.P([
                'This application shows the ', html.B('real-time location'), 
                ' of the ISS using data from ',
                html.A('Open Notify API', href='http://open-notify.org/', target='_blank'),
                '.'
            ]),
        ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),
        
        # Stats cards
        html.Div([
            html.Div([
                html.Div([
                    html.H4('Latitude', style={'color': '#7f8c8d', 'fontSize': '14px', 'marginBottom': '5px'}),
                    html.H2(id='latitude-display', style={'color': '#2c3e50', 'margin': '0'}),
                ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            ], style={'flex': '1', 'marginRight': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4('Longitude', style={'color': '#7f8c8d', 'fontSize': '14px', 'marginBottom': '5px'}),
                    html.H2(id='longitude-display', style={'color': '#2c3e50', 'margin': '0'}),
                ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            ], style={'flex': '1', 'marginRight': '10px'}),
            
            html.Div([
                html.Div([
                    html.H4('Last Updated', style={'color': '#7f8c8d', 'fontSize': '14px', 'marginBottom': '5px'}),
                    html.H2(id='timestamp-display', style={'color': '#2c3e50', 'margin': '0', 'fontSize': '18px'}),
                ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
            ], style={'flex': '1'}),
        ], style={'display': 'flex', 'marginBottom': '30px'}),
        
        # Globe visualization
        dcc.Graph(id='iss-globe', config={'displayModeBar': True, 'scrollZoom': True}),
        
        
        
        # Footer
        html.Div([
            html.P([
                'Built with ', html.B('Dash'), ' + ', html.B('Plotly'), ' + ', html.B('Flask'), ' | ',
                html.A('View on GitHub', href='https://github.com/manojmanivannan/liveisstracker', target='_blank'),
            ], style={'textAlign': 'center', 'color': '#7f8c8d', 'marginTop': '30px'}),
        ]),
        
        # Interval component for auto-refresh (every 5 seconds)
        dcc.Interval(
            id='interval-component',
            interval=5*1000,  # in milliseconds
            n_intervals=0
        )
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px', 'fontFamily': 'Arial, sans-serif'})
])


# Callback to update all displays
@app.callback(
    [
        Output('latitude-display', 'children'),
        Output('longitude-display', 'children'),
        Output('timestamp-display', 'children'),
        Output('iss-globe', 'figure')
    ],
    [Input('interval-component', 'n_intervals')],
    [State('iss-globe', 'figure')]
)
def update_iss_location(n, globe_fig_dict):
    """Update ISS location every interval - fully async, non-blocking"""
    iss_data = get_iss_location()
    
    if iss_data:
        lat = iss_data['latitude']
        lon = iss_data['longitude']
        timestamp = datetime.fromtimestamp(iss_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S UTC')
        
        if globe_fig_dict:
            globe_fig = go.Figure(globe_fig_dict)
            globe_fig.update_traces(lon=[lon], lat=[lat])
        else:
            globe_fig = create_3d_globe(lat, lon)
        
        return (
            f"{lat:.4f}°",
            f"{lon:.4f}°",
            timestamp,
            globe_fig
        )
    else:
        # Return default values on error
        return "Error", "Error", "Error", go.Figure()


if __name__ == '__main__':
    print("🛰️  Starting Live ISS Tracker...")
    print("📡 Open your browser at http://localhost:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
