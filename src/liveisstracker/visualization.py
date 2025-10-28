"""
Creates the 3D globe visualization for the ISS tracker.
"""

import plotly.graph_objects as go

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
        showlegend=False,
        uirevision='constant',  # Preserve UI state across updates
        paper_bgcolor='#f8f9fa',
        geo=dict(bgcolor='#f8f9fa')
    )
    
    return fig
