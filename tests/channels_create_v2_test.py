"""
Author: Shagun Panwar
zID: 5165416

"""
import pytest
import requests
import json
from src import config
from src.token_funcs import decode_token, check_valid_token

BASE_URL = config.url

# fixture is clearing the data store and registering the user
@pytest.fixture
def clear_and_register():
    requests.delete(BASE_URL + "clear/v1")

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "cat@gmail.com",
        "password": "LetsGO!"
    })

    #print(response_login.json())
    token = response_login.json()["token"]
    # auth_user_id = response_login.json()["auth_user_id"]
    
    return token

# Test 1: tests to check that the name of the channel is within the defined length
def test_channel_name(clear_and_register):
    token = clear_and_register
    # correct length for name
    response = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    assert response.status_code == 200

    # name length too short
    response2 = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "",
        "is_public": True
    })
    assert response2.status_code == 400

    # name length is too long i.e. >20
    response3 = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "Fundamentals of Software Engineering",
        "is_public": True
    })
    assert response3.status_code == 400

# Test 2: tests to check that the channel creator is the channel owner
def test_channel_creator(clear_and_register):
    token = clear_and_register
    auth_id = decode_token(token)["u_id"]
    
    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]

    response_channel_details = requests.get(BASE_URL + "channel/details/v2",params={
        "token": token,
        "channel_id": channel_id
    })

    # print(response_create_channels.json())
    # print(response_channel_details.json())
    owner_members = response_channel_details.json()["owner_members"]
    user_is_owner = False

    for user in owner_members:
        if auth_id == user["u_id"]:
            user_is_owner = True
            break

    assert user_is_owner == True

# Test 3: test a valid token
def test_invalid_token(clear_and_register):
    token = clear_and_register
    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token + "1",
        "name": "COMP1531",
        "is_public": True
    })
    
    assert response_create_channels.status_code == 403


    