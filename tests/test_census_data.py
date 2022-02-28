import logging
import os
from ast import Assert

from census_data import CensusData

logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)

def test_process():

    data_folder = os.path.join(os.path.join(os.getcwd(), 'tests'),'data')
    data = CensusData(os.path.join(data_folder,'census_data'))

    data.parse()

    N = 32

    #assert(len(parsed_data) == N)

    for item in data.good_data:
        assert(len(item) == 6)

    #assert(data.good_data[13][0] == "W Virginia")

    for item in data.good_data:  
        logger.debug(item)

    for item in data.bad_data:
        logger.debug(item)

    assert(False)
    