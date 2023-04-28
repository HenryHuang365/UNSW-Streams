import pytest
import requests
import json
from src import config

#Caspar Chan Pytest.fixture
@pytest.fixture()
def clear_and_register_create_channel():
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
    
def test_channel_messages_simple(clear_and_register_create_channel):

    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token']
    
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })   
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })
    
    channel_id = channel_id.json()['channel_id']
    
    resp_messages_1 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id,
        "start": 0
            })
    
    assert resp_messages_1.status_code == 200
    assert type(resp_messages_1.json()['messages']) == list
    assert len(resp_messages_1.json()['messages']) == 0
    assert type(resp_messages_1.json()['start']) == int
    assert type(resp_messages_1.json()['end']) == int
    
    requests.post(config.url + 'message/send/v1', json = {
        'token': token,
        'channel_id': channel_id,
        'message': "Hello World"
        })
    
    resp_messages_2 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id,
        "start": 0
            })
    
    assert resp_messages_2.status_code == 200
    assert type(resp_messages_2.json()['messages']) == list
    assert len(resp_messages_2.json()['messages']) == 1
    assert resp_messages_2.json()['messages'][0]['message_id'] == 1
    assert resp_messages_2.json()['messages'][0]['message'] == "Hello World"
    assert type(resp_messages_2.json()['start']) == int
    assert type(resp_messages_2.json()['end']) == int
    assert resp_messages_2.json()['end'] == -1
   
    for _ in range(55):
        resp_send_1 = requests.post(config.url + 'message/send/v1', json = {
            "token": token,
            "channel_id": channel_id,
            "message": "Hello World"
                })
    
    resp_messages_1 = requests.get(config.url + 'channel/messages/v2', params = {
    "token": token,
    "channel_id": channel_id,
    "start": 0
        })
    
    assert resp_send_1.status_code == 200
    assert len(resp_messages_1.json()['messages']) == 50
    assert resp_messages_1.json()['end'] == 50
    
def test_invalid_channel_id(clear_and_register_create_channel):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    resp_messages = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": '1111',
        "start": 0
            })
    assert resp_messages.status_code == 400
     
def test_start_greater_than_messages(clear_and_register_create_channel):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    resp = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
        })
    ch_id = resp.json()['channel_id']
    resp_messages = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": ch_id,
        "start": 10
        })
    
    assert resp_messages.status_code == 400
    
def test_not_in_channel(clear_and_register_create_channel):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })
    channel_id = channel_id.json()['channel_id']
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    resp_messages = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id,
        "start": 10
            })
    
    assert resp_messages.status_code == 403
    
def test_invalid_token(clear_and_register_create_channel):

    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })
    
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })
    channel_id = channel_id.json()['channel_id']
    
    resp_messages = requests.get(config.url + 'channel/messages/v2', params = {
        "token": 'abc123',
        "channel_id": channel_id,
        "start": 0
            })
    
    assert resp_messages.status_code == 403
        