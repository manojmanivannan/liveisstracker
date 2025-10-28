#!/bin/bash
# Simple launcher for the ISS Tracker application

echo "🛰️  Starting Live ISS Tracker..."
echo "📡 Open your browser at http://localhost:8050"
uvx --python 3.13 --with dash --with plotly --with geopy --with flask python main.py
