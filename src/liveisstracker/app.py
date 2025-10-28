"""
Defines the Dash application, its layout, and callbacks.
"""

from datetime import datetime
from dash import Dash, html, dcc, Input, Output, State, no_update
import plotly.graph_objects as go

from .data import get_iss_location
from .visualization import create_3d_globe

# Initialize Dash app
app = Dash(__name__)
app.title = "Live ISS Tracker"

# Initial figure to display while loading
initial_figure = go.Figure()
initial_figure.update_layout(
    xaxis={"visible": False},
    yaxis={"visible": False},
    annotations=[{
        "text": "Loading...",
        "xref": "paper",
        "yref": "paper",
        "showarrow": False,
        "font": {"size": 28}
    }]
)

# App layout
app.layout = html.Div([
    html.Button(
        'Close',
        id='close-button',
        style={'position': 'absolute', 'top': '10px', 'right': '10px', 'zIndex': '1000'}
    ),
    html.Div([
        html.H1('🛰️ International Space Station Tracker', 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
        
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
        dcc.Graph(
            id='iss-globe',
            figure=initial_figure,
            config={'displayModeBar': True, 'scrollZoom': True}
        ),
        
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

app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            window.pywebview.api.close_window();
        }
        return "";
    }
    """,
    Output('close-button', 'n_clicks'), # Dummy output
    Input('close-button', 'n_clicks'),
    prevent_initial_call=True
)


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
        
        # Check if the figure has data traces. If not, it's the initial load.
        if globe_fig_dict and globe_fig_dict.get('data'):
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
        # On error, return no_update to keep the current figure
        return no_update, no_update, no_update, no_update
