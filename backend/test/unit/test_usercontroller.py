import pytest
import unittest.mock as mock
from src.controllers.usercontroller import UserController

@pytest.fixture
def usercontroller():
    DAOMock = mock.MagicMock(str="DAO")
    usercontrollerMock = UserController(dao=DAOMock)
    return usercontrollerMock


#
#   This test validates if email is invalid
#
@pytest.mark.unit
def test_get_user_by_email_invalid(usercontroller):
    email = "invalidemail"
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
#
@pytest.mark.unit
def test_get_user_by_email_multiple(usercontroller, capsys):
    email = "test@test.com"
    usercontroller.dao.find.return_value = [{'email': email}, {'email': email}]


    usercontroller.get_user_by_email(email)

    captured = capsys.readouterr()
    assert captured.out == f'Error: more than one user found with mail {email}\n'

#
# validate if method returns the first user when multiple users are found with the same 
# email address
#

@pytest.mark.unit
def test_get_return_user_by_email_multiple(usercontroller):
    email = "test@test.com"
    usercontroller.dao.find.return_value = [{'email': email}, {'email': email}]

    usercontroller.get_user_by_email(email)
    assert usercontroller.get_user_by_email(email) == {'email': email}


#
#  This test validates if email is valid but no user is found with that email
#  address will raise a value error because we return the first element of the list 
#  even if the user doesn't exist. So this is a bug 
#

@pytest.mark.unit
def test_get_user_by_email_no_user(usercontroller):
    email ="nonexisting@email.com"
    with pytest.raises(IndexError, match="list index out of range"):
        usercontroller.dao.find.return_value = []
        usercontroller.get_user_by_email(email)



#
# This test test the code when there is an error in the database operation doesn't  
#

@pytest.mark.unit
def test_get_user_by_email_db_error(usercontroller):
    email = "test@test.com"
    usercontroller.dao.find.side_effect = Exception("Database error")
    with pytest.raises(Exception):
        usercontroller.get_user_by_email(email)