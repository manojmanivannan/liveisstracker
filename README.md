# Live ISS Tracker

🛰️ A simple desktop application that tracks and displays the real-time location of the International Space Station on an interactive 3D globe.

![sample application](output-streamlit.gif)

## Quick Start

To run the application, make sure you have a modern version of Python and `uv` installed, then simply run:

```bash
uvx liveisstracker
```

This command will download, install, and run the application in a temporary virtual environment.

## Other Ways to Run

### Using `pipx`

If you have `pipx` installed, you can use it to run the application in an isolated environment:

```bash
pipx run liveisstracker
```

### Using `pip`

You can also install the package directly into your Python environment using `pip`:

```bash
# Install the package
pip install liveisstracker

# Run the application
liveisstracker
```

## Development

To contribute to the development of this project, you can set it up locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/manojmanivannan/liveisstracker.git
    cd liveisstracker
    ```

2.  **Run the application:**
    The included `run.sh` script uses `uv` to install dependencies and run the app in a local virtual environment.
    ```bash
    ./run.sh
    ```
