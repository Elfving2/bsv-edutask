import pytest
import unittest.mock as mock
from src.util.dao import DAO


@pytest.fixture
def mockDao():
    daoMock = DAO(collection_name="DAO")
    return daoMock

