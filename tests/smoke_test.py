"""
Smoke test to verify that the package is installed correctly and is importable.
"""

try:
    from liveisstracker.main import main
    print("Successfully imported main function from liveisstracker.main")
except ImportError as e:
    print(f"Failed to import main function: {e}")
    exit(1)
