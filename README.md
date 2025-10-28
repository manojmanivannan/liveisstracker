![sample application](output-streamlit.gif)

# Live ISS Tracker

🛰️ A simple Python application that tracks and displays the real-time location of the International Space Station on an interactive 3D globe.

## Features

- **Interactive 3D Globe**: Orthographic projection centered on the ISS location
- **Flat Map View**: Traditional world map visualization
- **Real-time Data**: Fetches live ISS position from [Open Notify API](http://open-notify.org/)
- **Auto-refresh**: Optional automatic position updates every 5 seconds
- **No Docker Required**: Simple Python application with minimal dependencies

## Quick Start

### Method 1: Using the helper script (Easiest)

Simply run:

```bash
./run.sh
```

### Method 2: Using uvx directly

Run the application without installation:

```bash
uvx --python 3.13 --with dash --with plotly --with geopy --with flask python main.py
```

### Method 3: Using Python directly

1. Install dependencies:

```bash
pip install dash plotly geopy flask
```

2. Run the application:

```bash
python main.py
```

The application will open in your default web browser at `http://localhost:8050`

## Requirements

- Python 3.13 or higher
- Dependencies (automatically installed with uvx):
  - dash >= 2.14.0
  - plotly >= 5.17.0
  - geopy >= 2.4.0
  - flask >= 3.0.0

## Project Structure

```
liveisstracker/
├── main.py           # Main application file
├── pyproject.toml    # Project configuration
├── README.md         # This file
└── .gitignore        # Git ignore rules
```

## How It Works

1. **Data Source**: Fetches ISS coordinates from the Open Notify API
2. **Visualization**: Uses Plotly to render interactive globe and map views
3. **Web Framework**: Dash (built on Flask) provides truly async, non-blocking updates
4. **Auto-refresh**: Updates every 5 seconds without blocking user interactions

## About the ISS

The International Space Station:
- Orbits at ~408 km (254 miles) altitude
- Travels at ~27,600 km/h (17,100 mph)
- Completes one orbit every ~90 minutes
- Hosts international crew for scientific research

## Why Dash?

This version uses **Dash + Flask** instead of Streamlit for:
- ✅ **True async updates**: ISS position refreshes without blocking UI
- ✅ **Preserved interactions**: Your globe rotation/zoom stays intact during updates
- ✅ **Better performance**: No full page reloads, just data updates
- ✅ **Production ready**: Flask backend scales better for deployment

## License

MIT License - feel free to use and modify as needed.

## Links

- [Open Notify API](http://open-notify.org/)
- [GitHub Repository](https://github.com/manojmanivannan/liveisstracker)
