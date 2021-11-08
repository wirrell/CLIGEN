"""
Python wrapper for the CLIGEN simulator.

See: https://www.ars.usda.gov/midwest-area/
        west-lafayette-in/national-soil-erosion-research/docs/wepp/cligen/
"""
import subprocess
import pandas as pd
from pathlib import Path

cligen_location = str(Path(__file__).parent.resolve() / 'cligen/cligen')

def simulate_weather(climate_file, num_years):
    """
    Simulate weather using CLIGEN.
    See: https://www.ars.usda.gov/midwest-area/
            west-lafayette-in/national-soil-erosion-research/docs/wepp/cligen/

    Parameters
    ----------
    climate_file : str
        Path to climate file.

    num_years : int
        Number of years to simulate

    Returns
    -------
    pandas.DataFrame
        Columns are
        da mo year  prcp  dur   tp     ip  tmax  tmin  rad  w-vl w-dir  tdew
                    (mm)  (h)               (C)   (C) (l/d) (m/s)(Deg)   (C)
    """
    subprocess.call([cligen_location, f'-i{climate_file}', '-oOUT.TXT',
                     f'-y{num_years}', '-t5', '-F', '-b1'],
                     stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    output = pd.read_csv(Path(__file__).parent / 'OUT.TXT',
                         skiprows=13, sep='\s+')
    # remove units rows
    output =  output.drop(0)

    return output
          
# Quick test
if __name__ == '__main__':
    simulate_weather('stations/ia/Ia130112.par', 5)

