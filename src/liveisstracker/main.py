"""
Entry point for the windowed ISS Tracker application.

This script starts the Dash/Flask server in a separate thread
and then creates a pywebview window to display the application.
"""

import threading
import webview
import typer
from .app import app
from .data import get_iss_location

cli = typer.Typer()

def run_server():
    """Run the Dash/Flask server."""
    app.run(host='127.0.0.1', port=8050)

@cli.command()
def run():
    """Runs the ISS Tracker GUI application."""
    # Run the server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    class Api:
        def close_window(self):
            webview.windows[0].destroy()

    api = Api()

    # Create and start the webview window
    webview.create_window(
        'Live ISS Tracker',
        'http://127.0.0.1:8050',
        js_api=api,
        width=1400,
        height=900
    )
    webview.start()

@cli.command()
def location():
    """Prints the current ISS location and exits."""
    iss_data = get_iss_location()
    if iss_data:
        print(f"Latitude: {iss_data['latitude']}")
        print(f"Longitude: {iss_data['longitude']}")
    else:
        print("Could not retrieve ISS location.")

def main():
    cli()

if __name__ == '__main__':
    main()
