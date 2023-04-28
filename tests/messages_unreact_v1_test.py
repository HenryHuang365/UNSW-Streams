import pytest
import requests
import json
from src import config

"""
Tests for unreact
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
    
def test_message_unreact_channel(clear_and_register):
    #Login First User
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    #Make a channel to send a message
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
    })
    
    channel_id = channel_id.json()['channel_id']
         
    #Have the first user send the message
    resp_send_1 = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    resp = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    resp = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    msg_id = resp_send_1.json()['message_id']
    
    assert msg_id == 1
    assert resp_send_1.status_code == 200
    
    #Have that same user react to it, as they have permission to
    #The first message (the bottom of the list) is reacted
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/channel/messages/v2', params = {
        'token':token,
        'channel_id':channel_id,
        'start': 0})
    
    assert resp_react.status_code == 200
    assert len(resp.json()['messages'][-1]['reacts']) == 1
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/channel/messages/v2', params = {
        'token':token,
        'channel_id':channel_id,
        'start': 0})
    
    assert resp_unreact.status_code == 200
    assert len(resp.json()['messages'][-1]['reacts']) == 0
    
def test_message_unreact_dm(clear_and_register):
    #Login First User
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    #Make another dm to send msg
    dm_id = requests.post(config.url + 'dm/create/v1', json = {
        "token": token,
        'u_ids':[]
    })
    
    dm_id = dm_id.json()['dm_id']
         
    #Have the first user send the message
    resp_send_1 = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    resp = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    resp = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    msg_id = resp_send_1.json()['message_id']
    
    assert msg_id == 1
    assert resp_send_1.status_code == 200
    
    #Have that same user edit it, as they have permission to
    #The first message (the bottom of the list) is reacted
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token,
        'dm_id':dm_id,
        'start': 0})
    
    assert resp_react.status_code == 200
    assert len(resp.json()['messages'][-1]['reacts']) == 1
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token,
        'dm_id':dm_id,
        'start': 0})
    
    assert resp_unreact.status_code == 200
    assert len(resp.json()['messages'][-1]['reacts']) == 0
    
def test_message_multiple_unreact_channel(clear_and_register):
    #Login First User
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    #Make a channel to send a message
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
    })
    
    channel_id = channel_id.json()['channel_id']
         
    #Have the first user send the message
    resp_send_1 = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    resp_send_2 = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    resp_send_3 = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    msg_id = resp_send_1.json()['message_id']
    msg_id_2 = resp_send_2.json()['message_id']
    msg_id_3 = resp_send_3.json()['message_id']
    
    resp = requests.get(config.url + '/channel/messages/v2', params = {
        'token':token,
        'channel_id':channel_id,
        'start': 0})
    
    assert msg_id == 1
    assert resp_send_1.status_code == 200
    assert resp.json()['messages'][0]['message_id'] == 3
    assert resp.json()['messages'][1]['message_id'] == 2
    assert resp.json()['messages'][2]['message_id'] == 1
    
    #Have that same user react to it, as they have permission to
    #The first message (the bottom of the list) is reacted
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    assert resp_react.status_code == 200
    
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id_2,
        "react_id": 1
            })
    
    assert resp_react.status_code == 200
    
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id_3,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/channel/messages/v2', params = {
        'token':token,
        'channel_id':channel_id,
        'start': 0})
    
    assert resp_react.status_code == 200
    assert len(resp.json()['messages'][0]['reacts']) == 1
    assert len(resp.json()['messages'][1]['reacts']) == 1
    assert len(resp.json()['messages'][2]['reacts']) == 1
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/channel/messages/v2', params = {
        'token':token,
        'channel_id':channel_id,
        'start': 0})

    assert resp_unreact.status_code == 200
    assert len(resp.json()['messages'][2]['reacts']) == 0
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id_2,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/channel/messages/v2', params = {
        'token':token,
        'channel_id':channel_id,
        'start': 0})
    
    assert resp_unreact.status_code == 200
    assert len(resp.json()['messages'][1]['reacts']) == 0
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id_3,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/channel/messages/v2', params = {
        'token':token,
        'channel_id':channel_id,
        'start': 0})
    
    assert resp_unreact.status_code == 200
    assert len(resp.json()['messages'][0]['reacts']) == 0
    
def test_message_multiple_unreact_dm(clear_and_register):
    #Login First User
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    #Make another dm to send msg
    dm_id = requests.post(config.url + 'dm/create/v1', json = {
        "token": token,
        'u_ids':[]
    })
    
    dm_id = dm_id.json()['dm_id']
         
    #Have the first user send the message
    resp_send_1 = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    resp_send_2 = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    resp_send_3 = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    msg_id = resp_send_1.json()['message_id']
    msg_id_2 = resp_send_2.json()['message_id']
    msg_id_3 = resp_send_3.json()['message_id']
    
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token,
        'dm_id':dm_id,
        'start': 0})
    
    assert msg_id == 1
    assert resp_send_1.status_code == 200
    assert resp.json()['messages'][0]['message_id'] == 3
    assert resp.json()['messages'][1]['message_id'] == 2
    assert resp.json()['messages'][2]['message_id'] == 1
       
    
    #Have that same user react to it, as they have permission to
    #The first message (the bottom of the list) is reacted
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    assert resp_react.status_code == 200
    
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id_2,
        "react_id": 1
            })
    
    assert resp_react.status_code == 200
    
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id_3,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token,
        'dm_id':dm_id,
        'start': 0})
    
    assert resp_react.status_code == 200
    assert len(resp.json()['messages'][0]['reacts']) == 1
    assert len(resp.json()['messages'][1]['reacts']) == 1
    assert len(resp.json()['messages'][2]['reacts']) == 1
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token,
        'dm_id':dm_id,
        'start': 0})

    assert resp_unreact.status_code == 200
    assert len(resp.json()['messages'][2]['reacts']) == 0
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id_2,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token,
        'dm_id':dm_id,
        'start': 0})
    
    assert resp_unreact.status_code == 200
    assert len(resp.json()['messages'][1]['reacts']) == 0
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id_3,
        "react_id": 1
            })
    
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token,
        'dm_id':dm_id,
        'start': 0})
    
    assert resp_unreact.status_code == 200
    assert len(resp.json()['messages'][0]['reacts']) == 0
   
def test_invalid_message_id(clear_and_register):
    
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
    
    assert channel_id.status_code == 200
    
    channel_id = channel_id.json()['channel_id']

    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
            "token": token,
            "message_id": 9999999999999,
            "react_id": 1
            })

    assert resp_unreact.status_code == 400

def test_invalid_react_id(clear_and_register):
    
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
    
    assert channel_id.status_code == 200
    
    channel_id = channel_id.json()['channel_id']
    
    resp_send = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    msg_id = resp_send.json()['message_id']
    
    assert msg_id == 1
    assert resp_send.status_code == 200
    
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    assert resp_react.status_code == 200
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
            "token": token,
            "message_id": msg_id,
            "react_id": 999999999999
            })

    assert resp_unreact.status_code == 400
    
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
    
    resp_send_1 = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    msg_id  = resp_send_1.json()['message_id']
    
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    assert resp_react.status_code == 200
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
            "token": 'abc123',
            "message_id": msg_id,
            "react_id": 1
            })
    
    assert resp_unreact.status_code == 403
    
def test_sender_left_channel(clear_and_register):
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token_1 = resp.json()['token']     
    
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token_1,
        "name": "channel1",
        "is_public": True
    })
    
    channel_id = channel_id.json()['channel_id']
    
    resp_send = requests.post(config.url + 'message/send/v1', json = {
        "token": token_1,
        "channel_id": channel_id,
        "message": "Hello World"
    })
    
    assert resp_send.status_code == 200
    
    msg_id = resp_send.json()['message_id']  
    
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token_1,
        "message_id": msg_id,
        "react_id": 1
    })
    
    assert resp_react.status_code == 200
     
    resp_send = requests.post(config.url + 'channel/leave/v1', json = {
        "token": token_1,
        "channel_id": channel_id,
    })   
    
    
    #Return an error as user is the sender of the message but left the channel
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token_1,
        "message_id": msg_id,
        "react_id": 1
            })

    assert resp_unreact.status_code == 400
    
    
def test_sender_left_dm(clear_and_register):
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token_1 = resp.json()['token']     
    
    dm_id = requests.post(config.url + 'dm/create/v1', json = {
        "token": token_1,
        'u_ids': [2]
    })
    
    dm_id = dm_id.json()['dm_id']
    #login as second user
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
    
    assert resp_send.status_code == 200
    
    msg_id = resp_send.json()['message_id']
    
    resp_react = requests.post(config.url + 'message/react/v1', json = {
        "token": token_2,
        "message_id": msg_id,
        "react_id": 1
    })
    
    assert resp_react.status_code == 200
    
    resp_send = requests.post(config.url + 'dm/leave/v1', json = {
        "token": token_2,
        "dm_id": dm_id,
    })   
    
    
    #Return an error as user is the sender of the message but left the DM
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token_2,
        "message_id": msg_id,
        "react_id": 1
            })

    assert resp_unreact.status_code == 400
    
def test_message_no_react_channel(clear_and_register):
    #Login First User
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    #Make a channel to send a message
    channel_id = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
    })
    
    channel_id = channel_id.json()['channel_id']
         
    #Have the first user send the message
    resp_send_1 = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    resp = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    resp = requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": channel_id,
        "message": "Hello World"
            })
    
    msg_id = resp_send_1.json()['message_id']
    
    assert msg_id == 1
    assert resp_send_1.status_code == 200
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
    
    assert resp_unreact.status_code == 400
    
def test_message_no_react_dm(clear_and_register):
    #Login First User
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    #Make another dm to send msg
    dm_id = requests.post(config.url + 'dm/create/v1', json = {
        "token": token,
        'u_ids':[]
    })
    
    dm_id = dm_id.json()['dm_id']
         
    #Have the first user send the message
    resp_send_1 = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    resp = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    resp = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
            })
    
    msg_id = resp_send_1.json()['message_id']
    
    assert msg_id == 1
    assert resp_send_1.status_code == 200
    
    resp_unreact = requests.post(config.url + 'message/unreact/v1', json = {
        "token": token,
        "message_id": msg_id,
        "react_id": 1
            })
   
    assert resp_unreact.status_code == 400