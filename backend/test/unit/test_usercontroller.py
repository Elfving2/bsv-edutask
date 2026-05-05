import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

@pytest.fixture
def usercontroller():
    DAOMock = mock.MagicMock(str="DAO")
    usercontrollerMock = UserController(dao=DAOMock)
    return usercontrollerMock


#
#   This test validates if email is invalid or empty
#
@pytest.mark.unit
@pytest.mark.parametrize("email", ["invalidemail", ""])
def test_get_user_by_email_invalid(usercontroller, email):
    with pytest.raises(ValueError, match='Error: invalid email address'):
        usercontroller.get_user_by_email(email)

#   
#   This test validates if email is valid
#
@pytest.mark.unit
def test_get_user_by_email_valid(usercontroller):
    email = "test@test.com"
    usercontroller.dao.find.return_value = [{'email': email}]
    assert usercontroller.get_user_by_email(email) == {'email': email}

#
# Test if print statement is correctly printed when multiple users are found with the same email address
# and return the first user in the list
#
@pytest.mark.unit
def test_get_user_by_email_multiple(usercontroller, capsys):
    email = "test@test.com"
    usercontroller.dao.find.return_value = [{'email': email}, {'email': email}]

    result = usercontroller.get_user_by_email(email)

    captured = capsys.readouterr()
    assert captured.out == f'Error: more than one user found with mail {email}\n'
    assert result == {'email': email} 


 #
 # This test test the code when there is an error in the database operation doesn't  
 #

@pytest.mark.unit
def test_get_user_by_email_db_error(usercontroller):
    email = "test@test.com"
    usercontroller.dao.find.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        usercontroller.get_user_by_email(email)


#
# This test validates if no user is found 
# with the given email address
#
@pytest.mark.unit
def test_get_user_by_email_no_user_returns_none(usercontroller):
    email = "nonexisting@email.com"
    usercontroller.dao.find.return_value = []
    assert usercontroller.get_user_by_email(email) is None