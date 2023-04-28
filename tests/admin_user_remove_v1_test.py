"""
Author: Shagun Panwar
zID: 5165416
"""
from requests.models import Response
import pytest
import requests
import json
from src import config
from src.server import clear

BASE_URL = config.url

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

    # token = response_login.json()["token"]
    # auth_user_id = response_login.json()["auth_user_id"]
    
    return response_login.json()

# Test: user succesfully removed
def test_user_remove_success(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]
    
    response_1 = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP153asd1",
        "is_public": True
    })
    
    ch_id = response_1.json()["channel_id"]
    # create a new channel
    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]

    # register a new user
    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "mike@gmail.com",
        "password": "LetsGO!",
        "name_first": "mike",
        "name_last": "hannigan"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "mike@gmail.com",
        "password": "LetsGO!"
    })
    new_token = response_login.json()["token"]
    new_u_id = response_login.json()["auth_user_id"]

    #invite the new user to the channel
    requests.post(BASE_URL + "channel/invite/v2",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": new_u_id
    })
    
    requests.post(BASE_URL + "channel/invite/v2",json={
        "token": token,
        "channel_id": ch_id,
        "u_id": new_u_id
    })    
    requests.post(BASE_URL + "channel/addowner/v1",json={
        "token": token,
        "channel_id": ch_id,
        "u_id": new_u_id
    })

    # response_channel_details = requests.get(BASE_URL + "channel/details/v2",params={
    #     "token": token,
    #     "channel_id": channel_id
    # })

    # all_members = response_channel_details.json()['all_members']
    # owner_members = response_channel_details.json()['owner_members']
    # print(response_channel_details.json())
    requests.post(BASE_URL + "message/send/v1",json={
        "token": token,
        "channel_id": channel_id,
        "message": "hellowoasdrld"
    })
    
    requests.post(BASE_URL + "message/send/v1",json={
        "token": new_token,
        "channel_id": channel_id,
        "message": "hellowoasdrld"
    })   
    
    requests.post(BASE_URL + "message/send/v1",json={
        "token": new_token,
        "channel_id": channel_id,
        "message": "helloworld"
    })

    response_create_dm = requests.post(BASE_URL + "dm/create/v1",json={
        "token": new_token,
        "u_ids": [u_id]
    })

    response_create_dm = requests.post(BASE_URL + "dm/create/v1",json={
        "token": new_token,
        "u_ids": [u_id]
    })

    dm_id = response_create_dm.json()["dm_id"]

    requests.post(BASE_URL + "messages/senddm/v1",json={
        "token": new_token,
        "dm_id": dm_id,
        "message": "itsabluemoon"
    })

    requests.post(BASE_URL + "messages/senddm/v1",json={
        "token": new_token,
        "dm_id": dm_id,
    })

    response_admin_user_remove = requests.delete(BASE_URL + "admin/user/remove/v1",json={
        "token": token,
        "u_id": new_u_id
    })
    
    # user_removed = False

    # if new_u_id not in owner_members:
    #     user_removed = True
        
    # for user in all_members:
    #     if user["u_id"] != new_u_id:
    #         user_removed = True
    #         break
    
    # for index,message in enumerate(messages):
    #     if message["u_id"] == new_u_id:
    #         messages[index]["message"] = "Removed user"

    assert response_admin_user_remove.status_code == 200

# Test: u id does not refer to a valid user - Input error 
def test_valid_u_id(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_admin_user_remove2 = requests.delete(BASE_URL + "admin/user/remove/v1",json={
        "token": token,
        "u_id": u_id + 5
    })

    assert response_admin_user_remove2.status_code == 400

# Test: the authorised user is not a global owner - access error
def test_not_global_owner(clear_and_register):
    u_id = clear_and_register["auth_user_id"]

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "mike@gmail.com",
        "password": "LetsGO!",
        "name_first": "mike",
        "name_last": "hannigan"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "mike@gmail.com",
        "password": "LetsGO!"
    })

    new_token = response_login.json()["token"]

    response_admin_user_remove = requests.delete(BASE_URL + "admin/user/remove/v1",json={
        "token": new_token,
        "u_id": u_id
    })
    print(response_admin_user_remove.json())
    assert response_admin_user_remove.status_code == 403

# Test: u_id refers to a user who is the only global owner - Input error
def test_only_global_owner(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_admin_user_remove = requests.delete(BASE_URL + "admin/user/remove/v1",json={
        "token": token,
        "u_id": u_id
    })
    print(response_admin_user_remove.json())
    assert response_admin_user_remove.status_code == 400  

def test_invalid_token(clear_and_register):
    
    u_id = clear_and_register["auth_user_id"]
    
    response_admin_user_remove = requests.delete(BASE_URL + "admin/user/remove/v1",json={
        "token": "InvalidToken1",
        "u_id": u_id
    })
    
    assert response_admin_user_remove.status_code == 403




