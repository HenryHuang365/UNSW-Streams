"""
Author: Shagun Panwar
zID: 5165416
WIP NEED USER FILES
"""
import pytest
import requests
import json
from src import config
from src.token_funcs import decode_token, check_valid_token
from src.channel_add_remove_owners import channel_addowner_v1, channel_removeowner_v1


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

    # token = response_login.json()["token"]
    # auth_user_id = response_login.json()["auth_user_id"]
    
    return response_login.json()


# ----------------------------------------------------------------------------------------
'''
Channel owner add permissions
'''
# Test 1: Input error thrown when channel id does not refer to a valid channel - input error
def test_valid_channel_id_add(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })

    channel_id = response_create_channels.json()["channel_id"]

    response_addowner = requests.post(BASE_URL + "channel/addowner/v1",json={
        "token": token,
        "channel_id": channel_id + 100,
        "u_id": u_id
    })
    
    assert response_addowner.status_code == 400

# Test 2: U id does not refer to a valid user - input error
def test_valid_u_id_add(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]

    # test invalid user id
    response_addowner2 = requests.post(BASE_URL + "channel/addowner/v1",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id + 5
    })
    assert response_addowner2.status_code == 400

# Test 3: tests u_id refers to a user who is not already a channel member - input error
def test_not_channel_member_add(clear_and_register):
    token = clear_and_register["token"]

    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!",
        "name_first": "Boop",
        "name_last": "Loop"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!"
    })

    #new_user_token = response_login.json()["token"]
    new_user_u_id = response_login.json()["auth_user_id"]

    response_addowner = requests.post(BASE_URL + "channel/addowner/v1",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": new_user_u_id
    })

    assert response_addowner.status_code == 400

#Test 4: u id refers to a user who is already an owner of the channel
def test_user_already_channel_owner_add(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    
    channel_id = response_create_channels.json()["channel_id"]
    
    # response_channel_details = requests.get(BASE_URL + "channel/details/v2",params={
    #         "token": token,
    #         "channel_id": channel_id
    #     })
    
    # owner_members = response_channel_details.json()["owner_members"]

    # if u_id in owner_members:

    response_addowner = requests.post(BASE_URL + "channel/addowner/v1",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id
    })

    assert response_addowner.status_code == 400    

# Successfully add new owner - success case no error raised
def test_add_owner_sucessful(clear_and_register):
    token = clear_and_register["token"]
    #u_id = clear_and_register["auth_user_id"]
    
    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    
    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!",
        "name_first": "Boop",
        "name_last": "Loop"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!"
    })

    #new_user_token = response_login.json()["token"]
    new_user_u_id = response_login.json()["auth_user_id"]

    requests.post(BASE_URL + "channel/invite/v2",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": new_user_u_id
    })

    response_addowner = requests.post(BASE_URL + "channel/addowner/v1",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": new_user_u_id
    })

    assert response_addowner.status_code == 200

    # resp_details = requests.get(config.url + '/channel/details/v2', params={
    #     'token':token,
    #     'channel_id': channel_id, 
    #     })    

    
    # ownermembers = resp_details.json()['owner_members']

    # print(new_user_u_id)
    # print(ownermembers)

    # new_owner_added = False

    # for newowner in ownermembers:
    #     if newowner['u_id'] == new_user_u_id:
    #         new_owner_added = True

    # assert new_owner_added ==  True


# Test 5: channel id is valid and the authorised user does not have owner permission in the channel - access error
def test_auth_user_not_owner_add(clear_and_register):

    token = clear_and_register["token"]
   
    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    
    channel_id = response_create_channels.json()["channel_id"]
    
    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!",
        "name_first": "Boop",
        "name_last": "Loop"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!"
    })

    new_token = response_login.json()["token"]
    new_u_id = response_login.json()['auth_user_id']

    response_addowner = requests.post(BASE_URL + "channel/addowner/v1",json={
        "token": new_token,
        "channel_id": channel_id,
        "u_id": new_u_id
    })

    assert response_addowner.status_code == 403

# Testing for invalid token - access error
def test_invalid_token_add(clear_and_register):
    #token = clear_and_register
    u_id = clear_and_register["auth_user_id"]

    response_remove_owner = requests.post(BASE_URL + "channel/addowner/v1",json={
        "token": "InvalidToken",
        "channel_id": 15,
        "u_id": u_id
    })

    assert response_remove_owner.status_code == 403
# ----------------------------------------------------------------------------------------
'''
Channel owner remove permissions
'''
# Test 1: Input error thrown when channel id does not refer to a valid channel
def test_valid_channel_id_remove(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]

    response_removeowner = requests.post(BASE_URL + "channel/removeowner/v1",json={
        "token": token,
        "channel_id": channel_id + 100,
        "u_id": u_id
    })

    assert response_removeowner.status_code == 400

# Test 2: u id does not refer to a valid user 
def test_valid_u_id_remove(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]

    # test invalid user id
    response_removeowner2 = requests.post(BASE_URL + "channel/removeowner/v1",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id + 5
    })

    assert response_removeowner2.status_code == 400

# Test 3: u id refers to a user who is not an owner of the channel - input error
def test_not_channel_owner_remove(clear_and_register):
    token = clear_and_register["token"]

    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    
    channel_id = response_create_channels.json()["channel_id"]

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!",
        "name_first": "Boop",
        "name_last": "Loop"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!"
    })

    new_u_id = response_login.json()['auth_user_id']

    response_removeowner = requests.post(BASE_URL + "channel/removeowner/v1",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": new_u_id
    })

    assert response_removeowner.status_code == 400

# Test 4: u id refers to a user who is currently the only owner of the channel
def test_u_id_only_owner(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    
    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]
    
    response_removeowner = requests.post(BASE_URL + "channel/removeowner/v1",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id
    })

    response_channel_details = requests.get(BASE_URL + "channel/details/v2",params={
        "token": token,
        "channel_id": channel_id
    })
    
    owner_members = response_channel_details.json()["owner_members"]

    if len(owner_members) == 1:
        assert response_removeowner.status_code == 400    

# Test successful remove admin
def test_successful_remove_owner(clear_and_register):
    token = clear_and_register["token"]
    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    
    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!",
        "name_first": "Boop",
        "name_last": "Loop"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!"
    })

    #new_user_token = response_login.json()["token"]
    new_user_u_id = response_login.json()["auth_user_id"]

    requests.post(BASE_URL + "channel/invite/v2",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": new_user_u_id
    })

    requests.post(BASE_URL + "channel/addowner/v1",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": new_user_u_id
    })
    response_rmowner = requests.post(BASE_URL + "channel/removeowner/v1",json={
        "token": token,
        "channel_id": channel_id,
        "u_id": new_user_u_id
    })
    
    response_channel_details = requests.get(BASE_URL + "channel/details/v2",params={
        "token": token,
        "channel_id": channel_id
    })
    
    owner_members = response_channel_details.json()["owner_members"]

    assert len(owner_members) == 1
    assert response_rmowner.status_code == 200       
    
# Test 5: channel id is valid and the auth user does not have owner permissions in the channel - access error
def test_auth_user_not_owner_remove(clear_and_register):
    
    token = clear_and_register["token"]

    response_create_channels = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token,
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]
    
    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!",
        "name_first": "Boop",
        "name_last": "Loop"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "bluebottle@gmail.com",
        "password": "Jelly1fish!"
    })

    new_token = response_login.json()["token"]
    new_u_id = response_login.json()['auth_user_id']

    response_removeowner = requests.post(BASE_URL + "channel/removeowner/v1",json={
        "token": new_token,
        "channel_id": channel_id,
        "u_id": new_u_id
    })

    assert response_removeowner.status_code == 403

# Testing for invalid token - access error
def test_invalid_token_remove(clear_and_register):
    #token = clear_and_register
    u_id = clear_and_register["auth_user_id"]

    response_remove_owner = requests.post(BASE_URL + "channel/removeowner/v1",json={
        "token": "InvalidToken",
        "channel_id": 5,
        "u_id": u_id
    })

    
    assert response_remove_owner.status_code == 403