"""
Tests for cligen.py
"""
import os
import sys
import pytest
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cligen

class TestCligen:

    @pytest.fixture
    def climate_file(self):
        return '../stations/ia/Ia130112.par'

    @pytest.fixture
    def num_years(self):
        return 20
    
    @pytest.fixture
    def begin_year(self):
        return 2000

    @pytest.fixture
    def cligen_result_columns(self):
        return ['da', 'mo', 'year', 'prcp', 'dur', 'tp', 'ip', 'tmax',
                'tmin', 'rad', 'w-vl', 'w-dir',  'tdew']

    def test_simulater_weather(self, climate_file, num_years, begin_year, cligen_result_columns):
        result = cligen.simulate_weather(climate_file, num_years, begin_year)
        assert isinstance(result, pd.DataFrame)
        assert (result.columns == cligen_result_columns).all()

    def test_load_station_information(self, climate_file):
        station_info = cligen.load_station_information(climate_file)

        assert (list(station_info.keys()) == ['lat', 'lon', 'elev'])

    def test_station_within_state_by_coordinates(self):
        des_moines_lat = 41.35
        des_moines_lon = -93.37
        state_code = 'IA'
        nearest_station_file = cligen.find_station_within_state_by_coordinates(state_code,
                                                        des_moines_lat,
                                                        des_moines_lon)
        station_info = cligen.load_station_information(nearest_station_file)
        assert station_info['lat'] == 41.37
        assert station_info['lon'] == -93.55
