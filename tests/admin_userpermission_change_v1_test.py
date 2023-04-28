"""
Author: Shagun Panwar
zID: 5165416
"""
from requests.models import Response
import pytest
import requests
import json
from src import config

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

# Test 1: u id does not refer to a valid user - Input error 
def test_valid_u_id(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_admin_user_permission_change = requests.post(BASE_URL + "/admin/userpermission/change/v1",json={
        "token": token,
        "u_id": u_id + 5,
        "permission_id": 2
    })
    
    assert response_admin_user_permission_change.status_code == 400

# Test 2: u_id refers to a user who is the only global owner and they are being demoted to a user - input error
def test_demote_only_global_owner(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_admin_user_permission_change = requests.post(BASE_URL + "/admin/userpermission/change/v1",json={
        "token": token,
        "u_id": u_id,
        "permission_id": 2
    })

    assert response_admin_user_permission_change.status_code == 400  


# Test 3: permission id is invalid - input error
def test_invalid_permission_id(clear_and_register):
    token = clear_and_register["token"]
    u_id = clear_and_register["auth_user_id"]

    response_admin_user_permission_change = requests.post(BASE_URL + "/admin/userpermission/change/v1",json={
        "token": token,
        "u_id": u_id,
        "permission_id": 3
    })

    assert response_admin_user_permission_change.status_code == 400  

# Test 4: the authorised user is not a global owner - access error
def test_auth_user_not_global_owner(clear_and_register):
    
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

    response_admin_user_permission_change = requests.post(BASE_URL + "/admin/userpermission/change/v1",json={
        "token": new_token,
        "u_id": u_id,
        "permission_id": 2
    })

    assert response_admin_user_permission_change.status_code == 403  

def test_userpermission_success(clear_and_register):
    token = clear_and_register['token']

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "miasdaske@gmail.com",
        "password": "LetsGO!",
        "name_first": "mikase",
        "name_last": "hannigsaan"
    })    
    
    new_user = requests.post(BASE_URL + "auth/register/v2",json={
        "email": "mike@gmail.com",
        "password": "LetsGO!",
        "name_first": "mike",
        "name_last": "hannigan"
    })
 
    new_id = new_user.json()["auth_user_id"]    
    
    response_admin_user_permission_change = requests.post(BASE_URL + "/admin/userpermission/change/v1",json={
        "token": token,
        "u_id": new_id,
        "permission_id": 1
    })    
    
    assert response_admin_user_permission_change.status_code == 200

def test_invalid_token(clear_and_register):
    
    u_id = clear_and_register["auth_user_id"]

    response_admin_user_permission_change = requests.post(BASE_URL + "/admin/userpermission/change/v1",json={
        "token": "InvalidToken1",
        "u_id": u_id,
        "permission_id": 1
    }) 
    
    assert response_admin_user_permission_change.status_code == 403

