# GEMINI.md

## Project Overview

This project is a Python web application that displays the real-time location of the International Space Station (ISS) on an interactive 3D globe and a 2D map.

- **Frontend:** The application uses `Dash` and `Plotly` to create an interactive web interface.
- **Backend:** `Flask` serves as the web server.
- **Data Source:** The live ISS position is fetched from the [Open Notify API](http://open-notify.org/).
- **Main Logic:** The core application logic is contained in `main.py`.
- **Dependencies:** Project dependencies are listed in `pyproject.toml`.

## Building and Running

There are multiple ways to run the application:

### 1. Using the `run.sh` script (Recommended)

This script uses `uvx` to run the application in a temporary virtual environment.

```bash
./run.sh
```

### 2. Using `uvx` directly

```bash
uvx --python 3.13 --with dash --with plotly --with geopy --with flask python main.py
```

### 3. Using `pip`

First, install the dependencies:

```bash
pip install dash plotly geopy flask
```

Then, run the application:

```bash
python main.py
```

The application will be accessible at [http://localhost:8050](http://localhost:8050).

## Development Conventions

- The main application is a single file: `main.py`.
- The application uses `Dash` for the web framework and `Plotly` for visualizations.
- Asynchronous updates are used to refresh the ISS location without blocking the UI.
- The project follows standard Python coding conventions.
