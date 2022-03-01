import logging
import os
from ast import Assert

from census_data import CensusData

logger = logging.getLogger("dev")
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)


def test_parsing():

    data_folder = os.path.join(os.path.join(os.getcwd(), "tests"), "data")
    data = CensusData(os.path.join(data_folder, "census_data"))

    data.parse()

    N = 32

    assert len(data.good_data) == N
    assert len(data.bad_data) == 0

    for item in data.good_data:
        assert len(item) == CensusData.NCOL

    assert len(data.dataframe.loc[:, "7_2009"]) == N


def test_counts():
    data_folder = os.path.join(os.path.join(os.getcwd(), "tests"), "data")
    data = CensusData(os.path.join(data_folder, "census_data"))
    data.parse()
    data.extractCounts()

    assert set(data.counts.values()).intersection([6, 9, 3, 4, 1, 0, 3, 4, 2])


def test_benford_law():
    data_folder = os.path.join(os.path.join(os.getcwd(), "tests"), "data")
    data = CensusData(os.path.join(data_folder, "census_data"))
    data.parse()
    data.extractCounts()
    is_valid, distances = data.is_following_bernofs_law()
    logger.debug(distances)
    assert is_valid is False
