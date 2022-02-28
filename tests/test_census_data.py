from ast import Assert
import os
from census_data import CensusData

def test_process():

    data_folder = os.path.join(os.path.join(os.getcwd(), 'tests'),'data')
    data = CensusData(os.path.join(data_folder,'census_data'))

    parsed_data = data.process()

    assert(len(parsed_data) == 32)

    assert(len(parsed_data[0]) == 6)

    