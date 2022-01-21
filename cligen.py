"""
Python wrapper for the CLIGEN simulator.

See: https://www.ars.usda.gov/midwest-area/
        west-lafayette-in/national-soil-erosion-research/docs/wepp/cligen/
"""
import subprocess
import pandas as pd
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Point
from shapely.ops import nearest_points

cligen_location = str(Path(__file__).parent.resolve() / 'cligen/cligen')
stations_location = Path(__file__).parent.resolve() / 'stations'

def simulate_weather(climate_file, num_years, begin_year):
    """
    Simulate weather using CLIGEN.
    See: https://www.ars.usda.gov/midwest-area/
            west-lafayette-in/national-soil-erosion-research/docs/wepp/cligen/

    Parameters
    ----------
    climate_file : str
        Path to climate/station file.

    num_years : int
        Number of years to simulate

    begin_year : int
        Year number to start at

    Returns
    -------
    pandas.DataFrame
        Columns are
        da mo year  prcp  dur   tp     ip  tmax  tmin  rad  w-vl w-dir  tdew
                    (mm)  (h)               (C)   (C) (l/d) (m/s)(Deg)   (C)
    """
    subprocess.call([cligen_location, f'-i{climate_file}', '-oOUT.TXT',
                     f'-y{num_years}', '-t5', '-F', f'-b{begin_year}'],
                     stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    output = pd.read_csv('OUT.TXT',
                         skiprows=13, sep='\s+')
    # remove units rows
    output =  output.drop(0)

    return output


def load_station_information(station_file):
    """Load the station information for a given station file."""

    with open(station_file, 'r') as sf:
        station_string = sf.read()

    lat = float(station_string.split('LATT')[1].split('LONG')[0][2:])
    lon = float(station_string.split('LONG')[1].split('YEARS')[0][2:])
    elev = float(station_string.split('ELEVATION')[1].split('TP5')[0][2:])

    station_info = {
        'lat': lat,
        'lon': lon,
        'elev': elev
    }

    return station_info


def find_station_within_state_by_coordinates(state_code, lat, lon):
    """Load the climate file for the nearest station within a state.

    Parameters
    ----------
    state_code : str
        Two letter state abbreviation in ANSI standard.

    lat : float

    lon : float

    Returns
    -------
    str
        Full path to nearest station's climate file
    """
    state_files = stations_location / state_code.lower()

    
    station_list = []
    for station_file in state_files.glob('*.par'):
        station_info = load_station_information(station_file)
        station_list.append({'geometry': Point(station_info['lon'], station_info['lat']),
                             'location': station_file})
    station_df = gpd.GeoDataFrame(station_list)

    station_df['dist'] = station_df.apply(lambda row: Point(lon, lat).distance(row.geometry), axis=1)
    return station_df.iloc[station_df['dist'].argmin()]['location']




          
# Quick test
if __name__ == '__main__':
    simulate_weather('stations/ia/Ia130112.par', 5)

