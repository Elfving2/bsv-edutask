import pytest
from src.util.dao import DAO
from unittest.mock import patch


def temp_user():
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["firstName", "lastName", "email"],
            "properties": {
                "firstName": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "lastName": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "email": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                }
            }
        }
    }

#
# sets up Dao for user testing and drops the collection after the test is done
#

@pytest.fixture
def dao_setup():
    with patch('src.util.dao.getValidator', return_value=temp_user()):
        dao = DAO("name_dosent_matter")
        yield dao
        dao.drop()


#
# tests the create method of the Dao with correct data
#

@pytest.mark.integration
@pytest.mark.parametrize("user_data", [
{"firstName": "John", "lastName": "Doe", "email": "john.doe@example.com"},
{"firstName": "Jane", "lastName": "Smith", "email": "jane.smith@example.com"},
{"firstName": "Alice", "lastName": "Johnson", "email": "alice.johnson@example.com"}
])
def test_with_correct_data(dao_setup, user_data):
    dao = dao_setup
    result = dao.create(user_data)

    assert result["firstName"] == user_data["firstName"]
    assert result["lastName"] == user_data["lastName"]
    assert result["email"] == user_data["email"]


#
# tests the create method of the Dao with empty data
#
@pytest.mark.integration
def test_with_empty_data(dao_setup):
    dao = dao_setup
    with pytest.raises(Exception):
        dao.create({})

#
# tests the create method of the Dao with missing fields
#
@pytest.mark.integration
@pytest.mark.parametrize("user_data", [
{"firstName": "John", "lastName": "Doe"},
{"lastName": "John", "email": "john.doe@example.com"},
{"email": "john.doe@example.com"}
])
def test_with_missing_fields(dao_setup, user_data):
    dao = dao_setup
    with pytest.raises(Exception):
       dao.create(user_data)


#
# tests the create method of the Dao with incorrect data types
#
@pytest.mark.integration
@pytest.mark.parametrize("incorrect_user_data", [ 
{"firstName": 32, "lastName": "Doe", "email": "jhon.doe@example.com"},
{"firstName": "Jane", "lastName": "Smith", "email": {}},
{"firstName": "Alice", "lastName": 20, "email": "alice.johnson@example.com"}
])
def test_with_invalid_data(dao_setup, incorrect_user_data):
    dao = dao_setup
    with pytest.raises(Exception):
        dao.create(incorrect_user_data)

#
# tests the create method of the Dao with duplicate email
#

def test_with_duplicate_email(dao_setup):
    dao = dao_setup
    user_data = {"firstName": "sebastian", "lastName": "elfving", "email": "sebastian.elfving@example.com"}
    dao.create(user_data)

    with pytest.raises(Exception):
        dao.create(user_data)




