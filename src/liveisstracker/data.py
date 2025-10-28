"""
Handles fetching and parsing of ISS location data.
"""

import json
import urllib.request as url

# Constants
ISS_API_URL = 'http://api.open-notify.org/iss-now.json'

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
