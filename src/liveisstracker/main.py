"""
Entry point for the windowed ISS Tracker application.

This script starts the Dash/Flask server in a separate thread
and then creates a pywebview window to display the application.
"""

import multiprocessing
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
    server_process = multiprocessing.Process(target=run_server)
    server_process.daemon = True
    server_process.start()

    class Api:
        def __init__(self, server_process):
            self.server_process = server_process

        def close_window(self):
            if self.server_process:
                self.server_process.terminate()
            webview.windows[0].destroy()

    api = Api(server_process)

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
