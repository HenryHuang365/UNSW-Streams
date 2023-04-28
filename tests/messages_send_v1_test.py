import pytest
import requests
import json
from src import config

"""
Testing the message send function
"""

#Caspar Chan Pytest.fixture
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
    
def test_message_send_simple(clear_and_register):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    resp_2 = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token_2 = resp_2.json()['token'] 
    
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })
    
    channel_id = channel_id.json()['channel_id']    
    
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
    assert type(resp_send_1.json()['message_id']) == int
    assert resp_send_1.json()['message_id'] == 1
    assert resp_messages_1.json()['messages'][0]['message'] == 'Hello World'
    
    resp_join = requests.post(config.url + 'channel/join/v2', json = {
            "token": token_2,
            "channel_id": channel_id
    })
    
    assert resp_join.status_code == 200
    
    resp_send_1 = requests.post(config.url + 'message/send/v1', json = {
        "token": token_2,
        "channel_id": channel_id,
        "message": "Avengers"
            })
    
    resp_messages_1 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id,
        "start": 0
            })
    
    assert resp_send_1.status_code == 200
    assert type(resp_send_1.json()['message_id']) == int
    assert resp_send_1.json()['message_id'] == 2
    assert resp_messages_1.json()['messages'][0]['message'] == 'Avengers'

def test_invalid_channel_id(clear_and_register):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    resp_send = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": '1111',
        "message": "Hello World"
            })
    
    assert resp_send.status_code == 400
    
def test_invalid_message_length(clear_and_register):
    
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
    
    resp_send = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": ""
            })
    
    assert resp_send.status_code == 400
    
    resp_send = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "a"*1001
            })
    
    assert resp_send.status_code == 400
    
def test_not_channel_member(clear_and_register):
    
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
    
    resp_send = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    assert resp_send.status_code == 403
    
def test_invalid_token(clear_and_register):

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
    
    resp_send = requests.post(config.url + 'message/send/v1', json = {
        "token": 'abc123',
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    assert resp_send.status_code == 403
    