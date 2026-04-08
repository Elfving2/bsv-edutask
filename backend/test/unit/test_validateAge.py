import pytest
import unittest.mock


def test_validationAge():
    mock_usercontroller = mock.MagicMock()
    mock_usercontroller.get.return_value = {'age': 25}
    



