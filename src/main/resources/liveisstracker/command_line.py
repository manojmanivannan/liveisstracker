# import ${python_package}
from ${python_package}.issTrack.issTracking import TrackerISS
import click
from datetime import datetime


@click.command()
@click.option('--get-iss-location','-i', is_flag=True, help="Print the current location of International Space Station")
def main(get_iss_location):
    if get_iss_location:
        location = TrackerISS(silent=True).gps_location
        print(f'Timestamp (UTC): {datetime.utcfromtimestamp(int(location["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")} ISS is at Lat:{location["latitude"]} Lon:{location["longitude"]}')