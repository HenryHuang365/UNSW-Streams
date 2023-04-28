import pytest
import requests
import json
from src import config
from datetime import datetime, timedelta, timezone
import time

@pytest.fixture()
def clear_and_register():
    '''
    Clear and create user for temporary database
    '''
    #Clear
    requests.delete(config.url + '/clear/v1')
    
    #Register User 1
    resp = requests.post(config.url + '/auth/register/v2', json={
        "email": "first.person@email.com",
        "password": "password",
        "name_first": "Biggie",
        "name_last": "Smalls"
        })
    token = resp.json()['token']
    
    #Logout User 1
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        })
    
    #Resgiter User 2
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'second.person@email.com',
            'password': 'password',
            'name_first': 'Homer',
            'name_last': 'Simpson'
        })
    token = resp.json()['token']    
        
    #Logout User 2
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        }) 

def test_standup_start(clear_and_register):
    resp_regiester1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regiester1.json()['token'] 

    resp_regiester2 = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token2 = resp_regiester2.json()['token'] 
    
    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })

    resp_channel_id2 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token2,
        "name": "channel2",
        "is_public": True
            })
    
    channel_id = resp_channel_id1.json()['channel_id']
    assert resp_channel_id2.status_code == 200
    
    curr_time = datetime.now()        
    curr_timestamp = int(curr_time.timestamp())

    time_finish = datetime.now() + timedelta(seconds = 10)
    time_finish = int(time_finish.timestamp())
    
    resp_time_finish = requests.post(config.url + 'standup/start/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "length": 10
        })    
    time_diff = time_finish - curr_timestamp
    time.sleep(time_diff)
    assert resp_time_finish.status_code == 200
    assert resp_time_finish.json()["time_finish"] == time_finish

def test_standup_start_invalid_channel(clear_and_register):
    resp_regiester1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regiester1.json()['token'] 
    
    resp_time_finish = requests.post(config.url + 'standup/start/v1', json = {
        "token": token,
        "channel_id": -100,
        "length": 10
        })    
    assert resp_time_finish.status_code == 400

def test_standup_start_negative_length(clear_and_register):
    resp_regiester1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regiester1.json()['token'] 

    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })
    
    channel_id = resp_channel_id1.json()['channel_id']
    
    time_finish = datetime.now() + timedelta(seconds = 10)
    time_finish = int(time_finish.timestamp())
    
    resp_time_finish = requests.post(config.url + 'standup/start/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "length": -1,
        })    
    assert resp_time_finish.status_code == 400

def test_standup_start_running_standup_existing(clear_and_register):
    resp_regiester1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token1 = resp_regiester1.json()['token'] 

    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token1,
        "name": "channel1",
        "is_public": True
            })
    
    channel_id = resp_channel_id1.json()['channel_id']
    curr_time = datetime.now()        
    curr_timestamp = int(curr_time.timestamp())

    time_finish = datetime.now() + timedelta(seconds = 5)
    time_finish = int(time_finish.timestamp())
    
    requests.post(config.url + 'standup/start/v1', json = {
        "token": token1,
        "channel_id": channel_id,
        "length": 10,
        })   
    time_diff = time_finish - curr_timestamp
    time.sleep(time_diff)
    resp_time_finish2 = requests.post(config.url + 'standup/start/v1', json = {
        "token": token1,
        "channel_id": channel_id,
        "length": 10,
        })  
    assert resp_time_finish2.status_code == 400

def test_standup_start_invalid_token(clear_and_register):
    resp_regiester1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token1 = resp_regiester1.json()['token'] 

    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token1,
        "name": "channel1",
        "is_public": True
            })
    
    channel_id = resp_channel_id1.json()['channel_id']
    
    time_finish = datetime.now() + timedelta(seconds = 10)
    time_finish = int(time_finish.timestamp())
    
    resp_time_finish = requests.post(config.url + 'standup/start/v1', json = {
        "token": "invalid token",
        "channel_id": channel_id,
        "length": 10,
        })    
    assert resp_time_finish.status_code == 403

def test_standup_start_auth_user_not_in_channel(clear_and_register):
    resp_regiester1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token1 = resp_regiester1.json()['token'] 

    resp_regiester2 = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token2 = resp_regiester2.json()['token'] 

    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token1,
        "name": "channel1",
        "is_public": True
            })
    
    channel_id = resp_channel_id1.json()['channel_id']
    
    time_finish = datetime.now() + timedelta(seconds = 10)
    time_finish = int(time_finish.timestamp())
    
    resp_time_finish = requests.post(config.url + 'standup/start/v1', json = {
        "token": token2,
        "channel_id": channel_id,
        "length": 10,
        })    
    assert resp_time_finish.status_code == 403

