import pytest
import os
from src.util.dao import DAO
from src.util.validators import getValidator

import pymongo
from dotenv import dotenv_values


#
# Creating a new database connection for testing purposes. 
# This database is called 'testdb'
# Helper function
def create_db_connection(collection_name):
    LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
    MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)

    client = pymongo.MongoClient(MONGO_URL)
    database = client.testdb

    if collection_name not in database.list_collection_names():
        validator = getValidator(collection_name)
        database.create_collection(collection_name, validator=validator)

    # create DAO without running __init__
    dao = DAO.__new__(DAO)
    dao.collection = database[collection_name]

    return dao, database, client


@pytest.fixture
def dbConnection():
    dao, database, client = create_db_connection("user")
    yield dao
    database["user"].drop()
    client.close()


@pytest.fixture
def dbConnectionTask():
    dao, database, client = create_db_connection("task")
    yield dao
    database["task"].drop()
    client.close()


@pytest.fixture
def dbConnectionTodo():
    dao, database, client = create_db_connection("todo")
    yield dao
    database["todo"].drop()
    client.close()


@pytest.fixture
def dbConnectionVideo():
    dao, database, client = create_db_connection("video")
    yield dao
    database["video"].drop()
    client.close()
    
#
# USER Tests
#
# Tests the create function for users
# The test creates a new user with valid data and checks that the returned 
# object contains the expected data and an _id attribute.

@pytest.mark.integration
@pytest.mark.parametrize("data", [
    {"firstName": "Tuva", "lastName": "Rutberg", "email": "Tuva@example.com"},
    {"firstName": "Tuva", "lastName": "Rutberg", "email": "Tuva@example.com", "tags": ["Id1", "ID2"]},
    {"firstName": "Tuva", "lastName": "Rutberg", "email": "Tuva@example.com", "email":"Tuva@icloud.com"}
])
def test_create_valid_user(dbConnection, data):

    result = dbConnection.create(data)
    assert '_id' in result
    assert result['firstName'] == data['firstName']
    assert result['lastName'] == data['lastName']
    assert result['email'] == data['email']
    if 'tags' in data:
        assert result['tags'] == data['tags']


@pytest.mark.integration
@pytest.mark.parametrize("data", [
    {"firstName": "Tuva", "lastName": "Rutberg"},  # missing email
    {"firstName": "Tuva", "email": "Tuva@example.com"},  # missing lastName
    {"firstName": "Tuva"},  # missing email entirely
    {"firstName": "Tuva", "lastName": "Rutberg", "email": 123},  # invalid email
    {"firstName": 123, "lastName": "Rutberg", "email": "Tuva@example.com"},  # invalid first name
    {"firstName": "Tuva", "lastName": 123, "email": "Tuva@example.com"} # invalid last name
])
def test_faulty_create(dbConnection, data):   
    with pytest.raises(Exception):
        dbConnection.create(data)

#
# TASK TESTS
#
# Tests the create function for tasks
# The test creates a new task with valid data and checks that the returned 
# object contains the expected data and an _id attribute.
#

@pytest.mark.integration
@pytest.mark.parametrize("data", [
    {"title": "Learn Python", "description": "Complete Python basics course"},
    {"title": "Build API", "description": "Create REST API", "categories": ["Backend", "API"]},
    {"title": "Fix Bugs", "description": "Debug application issues", "categories": ["Testing"]}
])
def test_create_valid_task(dbConnectionTask, data):
    result = dbConnectionTask.create(data)
    assert '_id' in result
    assert result['title'] == data['title']
    assert result['description'] == data['description']
    if 'categories' in data:
        assert result['categories'] == data['categories']


@pytest.mark.integration
@pytest.mark.parametrize("data", [
    {"title": "Learn Python"},  # missing description
    {"description": "Complete course"},  # missing title
    {"title": 123, "description": "Invalid title type"},  # invalid title type
    {"title": "Valid Title", "description": 123},  # invalid description type
    {}  # missing both required fields
])
def test_faulty_create_task(dbConnectionTask, data):   
    with pytest.raises(Exception):
        dbConnectionTask.create(data)


#
# TODO TESTS
#
# Tests the create function for todos
# The test creates a new todo with valid data and checks that the returned 
# object contains the expected data and an _id attribute.
#

@pytest.mark.integration
@pytest.mark.parametrize("data", [
    {"description": "Buy groceries"},
    {"description": "Write documentation", "done": False},
    {"description": "Review pull requests", "done": True}
])
def test_create_valid_todo(dbConnectionTodo, data):
    result = dbConnectionTodo.create(data)
    assert '_id' in result
    assert result['description'] == data['description']
    if 'done' in data:
        assert result['done'] == data['done']


@pytest.mark.integration
@pytest.mark.parametrize("data", [
    {"done": True},  # missing description
    {"description": 123},  # invalid description type
    {"description": "Valid", "done": "invalid"},  # invalid done type
    {}  # missing required description
])
def test_faulty_create_todo(dbConnectionTodo, data):   
    with pytest.raises(Exception):
        dbConnectionTodo.create(data)


#
# VIDEO TESTS
#
# Tests the create function for videos
# The test creates a new video with valid data and checks that the returned 
# object contains the expected data and an _id attribute.
#

@pytest.mark.integration
@pytest.mark.parametrize("data", [
    {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
    {"url": "https://www.youtube.com/watch?v=abc123"}
])
def test_create_valid_video(dbConnectionVideo, data):
    result = dbConnectionVideo.create(data)
    assert '_id' in result
    assert result['url'] == data['url']


@pytest.mark.integration
@pytest.mark.parametrize("data", [
    {"url": 123},  # invalid url type
    {},  # missing url
])
def test_faulty_create_video(dbConnectionVideo, data):   
    with pytest.raises(Exception):
        dbConnectionVideo.create(data)
