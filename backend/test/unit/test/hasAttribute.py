import pytest
from src.util.helpers import hasAttribute

@pytest.mark.unit
def test_hasAttribute():
    result = hasAttribute({'name': 'Jane'}, 'name')
    assert result == True

@pytest.mark.unit
def test_hasAttribute_not_exists():
    result = hasAttribute({'name': 'Jane'}, 'age')
    assert result == False

@pytest.mark.unit
def test_hasAttribute_None():
    result = hasAttribute(None, 'name')
    assert result == False
