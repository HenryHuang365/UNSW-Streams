"""
Author: Shagun Panwar
zID: 5165416
"""
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

    token = response_login.json()["token"]
    # auth_user_id = response_login.json()["auth_user_id"]
    
    return token

#provide a list of all users and their associated details. return type is a list of users with no errors raised
def test_users_all(clear_and_register):
    token = clear_and_register

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "mike@gmail.com",
        "password": "LetsGO!",
        "name_first": "Mike",
        "name_last": "hannigan"
    })

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "cats@gmail.com",
        "password": "LetsGO!",
        "name_first": "cats",
        "name_last": "dogs"
    })

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "testuser@gmail.com",
        "password": "LetsGO!",
        "name_first": "Test",
        "name_last": "user"
    })

    
    response_users_all = requests.get(BASE_URL + "/users/all/v1", params={
        "token": token
    })
    
    # users = response_users_all.json()
    # for emails in users:
    #     if emails["email"] != "":
    assert response_users_all.json() == {
        'users':[
            {   
                "u_id": 1,
                "email": "cat@gmail.com",
                "name_first": "name_first",
                "name_last": "name_last", 
                "handle_str": "namefirstnamelast",  
                "profile_img_url": "http://localhost:8080/static/default.jpeg"
                
            },
            {
                "u_id": 2,
                "email": "mike@gmail.com",
                "name_first": "Mike",
                "name_last": "hannigan",
                "handle_str": "mikehannigan",
                "profile_img_url": "http://localhost:8080/static/default.jpeg"
            },
            {
                "u_id": 3,
                "email": "cats@gmail.com",
                "name_first": "cats",
                "name_last": "dogs",
                "handle_str": "catsdogs",
                "profile_img_url": "http://localhost:8080/static/default.jpeg"
            },
            {
                "u_id": 4,
                "email": "testuser@gmail.com",
                "name_first": "Test",
                "name_last": "user",
                "handle_str": "testuser",
                "profile_img_url": "http://localhost:8080/static/default.jpeg"
            }
        ]
    }
    
    #assert response_users_all.status_code == 200

def test_removed_user_not_included():

    requests.delete(BASE_URL + "clear/v1")
    # this will be the global owner
    resp_reg_1 = requests.post(BASE_URL + "auth/register/v2",json={
        "email": "mike@gmail.com",
        "password": "LetsGO!",
        "name_first": "Mike",
        "name_last": "hannigan"
    })
    u_id_1 = resp_reg_1.json()['auth_user_id']
    token_1 = resp_reg_1.json()['token']

    resp_reg_2 = requests.post(BASE_URL + "auth/register/v2",json={
        "email": "cats@gmail.com",
        "password": "LetsGO!",
        "name_first": "cats",
        "name_last": "dogs"
    })
    u_id_2 = resp_reg_2.json()['auth_user_id']

    admin_resp = requests.delete(BASE_URL + "admin/user/remove/v1",json={
        "token": token_1,
        "u_id": u_id_2
    })
    assert admin_resp.status_code == 200
    response_users_all = requests.get(BASE_URL + "/users/all/v1", params={
        "token": token_1
    })
    
 
    assert response_users_all.json() == {
        'users':[
            {   
                "u_id": u_id_1,
                 "email": "mike@gmail.com",
                "name_first": "Mike",
                "name_last": "hannigan",
                "handle_str": "mikehannigan"  ,
                "profile_img_url": "http://localhost:8080/static/default.jpeg"
            }
        ]
    }


def test_invalid_token(clear_and_register):
    token = clear_and_register
    response_users_all = requests.get(BASE_URL + "/users/all/v1",params ={
        "token": token + "1"
    })
    
    assert response_users_all.status_code == 403