import pytest
from src.util.helpers import hasAttribute

#
#   We can use fixtiures to mock database
#

@pytest.fixture
def obj():
    return {'name': 'Jane'}

@pytest.fixture
def obj_empty():
    return {}

@pytest.mark.unit
def test_hasAttribute(obj):
    result = hasAttribute(obj, 'name')
    assert result == True

@pytest.mark.unit
def test_hasAttribute_not_exists(obj):
    result = hasAttribute(obj, 'age')
    assert result == False

@pytest.mark.unit
def test_hasAttribute_empty(obj_empty):
    result = hasAttribute(obj_empty, 'name')
    assert result == False








#
# lecture purpose dosent work becuase we have to change code 
#

# @pytest.mark.unit
# def test_hasAttribute_None():
#     result = hasAttribute(None, 'name')
#     assert result == False
