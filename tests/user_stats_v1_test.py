
"""
Author: Shagun Panwar
zID: 5165416
"""
from requests.models import Response
import pytest
import requests
import json
from src import config
from datetime import datetime
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
    response_users_all = requests.get(BASE_URL + "/user/stats/v1",params ={
        "token": token + "1"
    })
    
    assert response_users_all.status_code == 403

# # Fetches the required statistics about this user's use of UNSW Streams - correct
def test_correct_user_stats_token1_does_all(clear_and_register):
    #Create 2 more users (in total 3)
    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "mike@gmail.com",
        "password": "LetsGO!",
        "name_first": "Mike",
        "name_last": "hannigan"
    })
    resp_login2 = requests.post(BASE_URL + "auth/register/v2",json={
        "email": "mikasde@gmail.com",
        "password": "LetsGO!",
        "name_first": "Mike",
        "name_last": "hannigan"
    })
    
    resp_login1 = requests.post(config.url + '/auth/login/v2', json = {
        "email": "mike@gmail.com",
        "password": "LetsGO!"
        })    
    
    
    token1 = resp_login1.json()['token']    
    token2 = resp_login2.json()['token']  
    #token 1 create 3 dm -- in dm_3 , uid 1 is invited
    dm_1 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token1,
        'u_ids': []
        })
    
    requests.post(config.url + '/dm/create/v1', json = {
        'token':token1,
        'u_ids': []
        })
    
    requests.post(config.url + '/dm/create/v1', json = {
        'token':token1,
        'u_ids': [1]
        })    
    time_changed_2= int(datetime.now().timestamp())
    
    dm_1 = dm_1.json()['dm_id']
    #token 1 create 3 channels , in ch_3, uid 1 is invited
    # 4 ,5 invited into channel 3
    
    requests.post(BASE_URL + "channels/create/v2",json={
        "token": token1,
        "name": "channel1",
        "is_public": True
    })
    
    requests.post(BASE_URL + "channels/create/v2",json={
        "token": token1,
        "name": "channel2",
        "is_public": True
    })
    
    channel_id = requests.post(BASE_URL + "channels/create/v2",json={
        "token": token1,
        "name": "channel3",
        "is_public": True
    })
    
    time_changed_1= int(datetime.now().timestamp())
    channel_id = channel_id.json()['channel_id']    
    
    requests.post(config.url + '/channel/invite/v2', json = {
        'token':token1,
        'channel_id': channel_id, 
        'u_id': 1,
    }) 
    
    
    #token 1 send 3 msgs to dm 1 and 3 msg in channel 3
    requests.post(config.url + 'message/send/v1', json = {
        "token": token1,
        "channel_id": channel_id,
        "message": "Hello World"
    })
    
    requests.post(config.url + 'message/send/v1', json = {
        "token": token1,
        "channel_id": channel_id,
        "message": "Hello World"
    })
    
    requests.post(config.url + 'message/send/v1', json = {
        "token": token1,
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
    
    
    response_users_stats = requests.get(BASE_URL + "/user/stats/v1", params={
        "token": token1
    })
    
    requests.delete(config.url + 'message/remove/v1', json = {
        "token": token1,
        "message_id": 1
    })    

    resp_1 = requests.get(BASE_URL + "/user/stats/v1", params={
        "token": token1
    })
    
    resp_0 = requests.get(BASE_URL + "/user/stats/v1", params={
        "token": token2
    })
    
    time.sleep(1)
    stat = response_users_stats.json()['user_stats']
    stat1 = resp_0.json()['user_stats']
    stat2 = resp_1.json()['user_stats']
    assert len(stat['channels_joined']) == 4
    assert len(stat['dms_joined']) == 4
    assert len(stat['messages_sent']) == 7
    
    assert stat['channels_joined'][-1]['time_stamp'] == time_changed_1
    assert stat['dms_joined'][-1]['time_stamp'] == time_changed_2
    assert stat['messages_sent'][-1]['time_stamp'] == time_changed_3
    
    assert stat["involvement_rate"] == 1
    assert stat1["involvement_rate"] == 0
    assert stat2["involvement_rate"] == 1
    
    assert response_users_stats.status_code == 200

def test_denom_0(clear_and_register):   
    token = clear_and_register
    resp_0 = requests.get(BASE_URL + "/user/stats/v1", params={
        "token": token
    })
    stat1 = resp_0.json()['user_stats']
    assert stat1["involvement_rate"] == 0


