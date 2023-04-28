"""
Author: Shagun Panwar
zID: 5165416
"""
from requests.models import Response
import pytest
import requests
import json
from datetime import datetime
from src import config
import time

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

# valid token test
def test_invalid_token(clear_and_register):
    token = clear_and_register
    response_users_all = requests.get(BASE_URL + "/users/stats/v1",params ={
        "token": token + "1"
    })
    
    assert response_users_all.status_code == 403

# Fetches the required statistics about the use of UNSW Streams. - correct 
def test_correct_user_stats(clear_and_register):
    token = clear_and_register

    #Create 4 more users (in total 5)
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
        "email": "catsss@gmail.com",
        "password": "LetsGO!",
        "name_first": "cats",
        "name_last": "dogs"
    })
    
    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "catsssss@gmail.com",
        "password": "LetsGO!",
        "name_first": "cats",
        "name_last": "dogs"
    })
    resp_login1 = requests.post(config.url + '/auth/login/v2', json = {
        "email": "mike@gmail.com",
        "password": "LetsGO!"
        })    
    
    resp_login2 = requests.post(config.url + '/auth/login/v2', json = {
        "email": "cats@gmail.com",
        "password": "LetsGO!"
        })   
    
    token1 = resp_login1.json()['token']    
    token2 = resp_login2.json()['token']
    
    #token 1 create 3 dm -- 2 unique users in dm
    dm_1 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token1,
        'u_ids': []
        })
    
    requests.post(config.url + '/dm/create/v1', json = {
        'token':token1,
        'u_ids': [2]
        })
    
    requests.post(config.url + '/dm/create/v1', json = {
        'token':token1,
        'u_ids': [3]
        })    
    time_changed_2= int(datetime.now().timestamp())
    
    dm_1 = dm_1.json()['dm_id']
    #token 2 create 3 channels --> 2 unique users in channel (2,3 is previously in dm)
    # 4 ,5 invited into channel 3
    
    requests.post(BASE_URL + "channels/create/v2",json={
        "token": token2,
        "name": "channel1",
        "is_public": True
    })
    
    requests.post(BASE_URL + "channels/create/v2",json={
        "token": token2,
        "name": "channel2",
        "is_public": True
    })
    
    channel_id = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token2,
        "name": "channel3",
        "is_public": True
    })
    
    time_changed_1= int(datetime.now().timestamp())
    channel_id = channel_id.json()['channel_id']    
    
    requests.post(config.url + '/channel/invite/v2', json = {
        'token':token2,
        'channel_id': channel_id, 
        'u_id': 4,
    }) 
    
    requests.post(config.url + '/channel/invite/v2', json = {
        'token':token2,
        'channel_id': channel_id, 
        'u_id': 5,
    })             
    
    
    #3 msg send in dm 1 and 3 msg send in channel 3
    requests.post(config.url + 'message/send/v1', json = {
        "token": token2,
        "channel_id": channel_id,
        "message": "Hello World"
    })
    
    requests.post(config.url + 'message/send/v1', json = {
        "token": token2,
        "channel_id": channel_id,
        "message": "Hello World"
    })
    
    requests.post(config.url + 'message/send/v1', json = {
        "token": token2,
        "channel_id": channel_id,
        "message": "Hello World"
    })
    
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": token1,
        "dm_id": dm_1,
        "message": "Hello World"
    })
    
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": token1,
        "dm_id": dm_1,
        "message": "Hello World"
    })
    
    time.sleep(1)
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": token1,
        "dm_id": dm_1,
        "message": "Hello World"
    })
    time_changed_3= round(datetime.now().timestamp())
    
    
    response_users_stats = requests.get(BASE_URL + "/users/stats/v1", params={
        "token": token
    })
    
    time.sleep(1)
    workspace = response_users_stats.json()['workspace_stats']
    
    assert len(workspace['channels_exist']) == 4
    assert len(workspace['dms_exist']) == 4
    assert len(workspace['messages_exist']) == 7
    
    assert workspace['channels_exist'][-1]['time_stamp'] == time_changed_1
    assert workspace['dms_exist'][-1]['time_stamp'] == time_changed_2
    assert workspace['messages_exist'][-1]['time_stamp'] == time_changed_3
    
    assert workspace["utilization_rate"] == 4/5

    
    assert response_users_stats.status_code == 200

