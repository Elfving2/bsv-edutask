import pytest
import unittest.mock as mock
from src.util.helpers import ValidationHelper


@pytest.fixture
def get_age(current_age: int):
    mockController = mock.MagicMock()
    mockController.get.return_value = {'age': current_age}
    ValidationHelperMock = ValidationHelper(usercontroller=mockController)
    return ValidationHelperMock

@pytest.mark.unit
@pytest.mark.parametrize('current_age, expected', [(-1, 'invalid'), (0, 'underaged'), (1, 'underaged'), (17, 'underaged'), (18, 'underaged'), (19, 'valid'), (119, 'valid'), (120, 'valid'), (121, 'invalid')])
def test_validateAge_valid(get_age, expected):
    result = get_age.validateAge(userid=None)
    assert result == expected