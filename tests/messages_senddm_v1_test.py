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
    
def test_dm_send_simple(clear_and_register):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    resp_2 = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    u_id_2 = resp_2.json()['auth_user_id']
    token_2 = resp_2.json()['token'] 
    
    dm_id = requests.post(config.url + 'dm/create/v1', json = {
        "token": token,
        "u_ids": [u_id_2]
            })
    
    resp = requests.post(config.url + 'dm/create/v1', json = {
        'token':token,
        'u_id':[]})
    
    resp = requests.post(config.url + 'dm/create/v1', json = {
        'token':token,
        'u_id':[]})    
    
    assert dm_id.status_code == 200
    
    dm_id = dm_id.json()['dm_id']
    
    resp_send_1 = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
        })

    resp_dms = requests.get(config.url + 'dm/messages/v1', params = {
            "token": token,
            "dm_id": dm_id,
            "start": 0
            })
    
    assert resp_send_1.status_code == 200
    assert type(resp_send_1.json()['message_id']) == int
    assert resp_send_1.json()['message_id'] == 1
    assert resp_dms.json()['messages'][0]['message'] == 'Hello World'
    
    resp_send_1 = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token_2,
        "dm_id": dm_id,
        "message": "Hawkeye best"
        })

    resp_dms = requests.get(config.url + 'dm/messages/v1', params = {
            "token": token,
            "dm_id": dm_id,
            "start": 0
            })
    
    assert resp_send_1.status_code == 200
    assert type(resp_send_1.json()['message_id']) == int
    assert resp_send_1.json()['message_id'] == 2
    assert resp_dms.json()['messages'][0]['message'] == 'Hawkeye best'
    
def test_invalid_dm_id(clear_and_register):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
       
    resp_send = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": '1111',
        "message": "Hello World"
            })
    
    assert resp_send.status_code == 400
    
def test_invalid_message_length(clear_and_register):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + 'dm/create/v1', json = {
        "token": token,
        "u_ids": []
            })
    dm_id = dm_id.json()['dm_id']
    
    resp_send = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": ""
            })
    
    assert resp_send.status_code == 400
    
    resp_send = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": 'a'*1001
            })
    
    assert resp_send.status_code == 400
    
def test_not_dm_member(clear_and_register):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token_1 = resp.json()['token'] 
    
    dm_id = requests.post(config.url + 'dm/create/v1', json = {
        "token": token_1,
        "u_ids": []   
            })
    dm_id = dm_id.json()['dm_id']
    
    resp = requests.post(config.url + 'dm/create/v1', json = {
        "token": token_1,
        "u_ids": []   
            })
    
    resp = requests.post(config.url + 'dm/create/v1', json = {
        "token": token_1,
        "u_ids": []   
            })
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token_2 = resp.json()['token'] 
    
    resp_send = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token_2,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    assert resp_send.status_code == 403
    
    resp_leave = requests.post(config.url + 'dm/leave/v1', json = {
            'token': token_1,
            'dm_id': dm_id
            })
    
    resp_leave.status_code == 200
    
    resp_send = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token_1,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    assert resp_send.status_code == 403
    
def test_invalid_token(clear_and_register):

    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + 'dm/create/v1', json = {
        "token": token,
        "u_ids": []   
            })
    dm_id = dm_id.json()['dm_id']
    
    resp_send = requests.post(config.url + 'message/senddm/v1', json = {
        "token": 'abc123',
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    assert resp_send.status_code == 403
