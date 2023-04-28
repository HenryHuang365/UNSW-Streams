import pytest
import requests
import json
from src import config

"""
Testing the message edit function
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

def test_message_edit_channel(clear_and_register):
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
    
    #Have that same user edit it, as they have permission to
    #The first message (the bottom of the list) is edited
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token,
        "message_id": msg_id,
        "message": "World Hello"
    })
    
    resp = requests.get(config.url + '/channel/messages/v2', params = {
        'token':token,
        'channel_id':channel_id,
        'start': 0})
    
    assert resp_edit.status_code == 200
    assert len(resp.json()['messages']) == 3
    assert resp.json()['messages'][2]['message'] == 'World Hello'
    
def test_message_edit_dm(clear_and_register):
    #Login First User
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    #Make a channel and send a msg to that channel (Test for unique msg id)
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
    
    assert msg_id == 2
    assert resp_send_1.status_code == 200
    
    #Have that same user edit it, as they have permission to
    #The first message (the bottom of the list) is edited
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token,
        "message_id": msg_id,
        "message": "World Hello"
    })
    
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token,
        'dm_id':dm_id,
        'start': 0})
    
    assert resp_edit.status_code == 200
    assert len(resp.json()['messages']) == 3
    assert resp.json()['messages'][2]['message'] == 'World Hello'

    
def test_invalid_character_length(clear_and_register):
    
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
        "message": "Hello World"
    })
    
    #Return an input error as message cannot be greater than 1000 charaters
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token,
        "message_id": resp_send.json(),
        "message": "a"*1001
    })
    
    assert resp_edit.status_code == 400
    
def test_invalid_message_id(clear_and_register):
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    #Return an input error if the message being edited doesn't exist
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token,
        "message_id": '7968576676786',
        "message": "Hello World"
    })
    
    assert resp_edit.status_code == 400
    
def test_edit_different_user_channel(clear_and_register):
    
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
    
    msg = resp_send.json()['message_id']
    
    resp_2 = requests.post(config.url + 'auth/login/v2', json = {
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token_2 = resp_2.json()['token']
    
    #Return an error as user is not in the channel or the sender of the message
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token_2,
        "message_id": msg,
        "message": "World Hello"
    })
    
    assert resp_edit.status_code == 403
     
    resp_join = requests.post(config.url + 'channel/join/v2', json = {
            "token": token_2,
            "channel_id": channel_id
    })
    
    assert resp_join.status_code == 200
    
    msg = resp_send.json()['message_id']
    
    #Return an error as user is not the sender of the message
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token_2,
        "message_id": msg,
        "message": "World Hello"
    })
    
    assert resp_edit.status_code == 403
    
def test_edit_different_user_dm(clear_and_register):    
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token_1 = resp.json()['token']     
        
    dm_id = requests.post(config.url + 'dm/create/v1', json = {
        "token": token_1,
        "u_ids": [2]
            })
    
    assert dm_id.status_code == 200
    
    dm_id = dm_id.json()['dm_id']
    
    resp_send_1 = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token_1,
        "dm_id": dm_id,
        "message": "Hello World"
        })
    
    msg_id = resp_send_1.json()['message_id']
    
    resp_dms = requests.get(config.url + 'dm/messages/v1', params = {
            "token": token_1,
            "dm_id": dm_id,
            "start": 0
            })
    
    assert resp_dms.status_code == 200
    assert resp_dms.json()['messages'][0]['message'] == 'Hello World'
    assert len(resp_dms.json()['messages']) == 1
    
    #Register as the third user (not in dm)
    resp = requests.post(config.url + '/auth/register/v2', json={
        "email": "third.person@email.com",
        "password": "password",
        "name_first": "Biggie",
        "name_last": "Smalls"
        })
    token_3 = resp.json()['token']
    
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token_3,
        "message_id": msg_id,
        "message": "World Hello"
    })
    
    assert resp_edit.status_code == 403
    
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
    
    resp_send = requests.post(config.url + 'channel/leave/v1', json = {
        "token": token_1,
        "channel_id": channel_id,
    })   
    
    #Return an error as user is the sender of the message but left the channel
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token_1,
        "message_id": msg_id,
        "message": "World Hello"
    })    
    
    assert resp_edit.status_code == 403
    
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
    
    resp_send = requests.post(config.url + 'dm/leave/v1', json = {
        "token": token_2,
        "dm_id": dm_id,
    })   
    
    #Return an error as user is the sender of the message but left the channel
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token_2,
        "message_id": msg_id,
        "message": "World Hello"
    })    
    
    assert resp_edit.status_code == 403    

def test_msg_longer_than_1000(clear_and_register):
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
    
    resp_send = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token_1,
        "dm_id": dm_id,
        "message": "Hello World"
    })  
    msg_id = resp_send.json()['message_id']       
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token_1,
        'dm_id':dm_id,
        'start': 0})
    
    assert len(resp.json()['messages']) == 1    
    #Remove a message if input is ""
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token_1,
        "message_id": msg_id,
        "message": "a"*1001
    })       
    
    assert resp_edit.status_code == 400
    
def test_empty_message_channnel(clear_and_register):  
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
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token_1,
        "message_id": msg_id,
        "message": ""
    })
    
    resp = requests.get(config.url + '/channel/messages/v2', params = {
        'token':token_1,
        'channel_id':channel_id,
        'start': 0})
    
    assert resp_edit.status_code == 200
    assert len(resp.json()['messages']) == 0    
    
def test_empty_message_dm(clear_and_register):  
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
    
    resp_send = requests.post(config.url + 'message/senddm/v1', json = {
        "token": token_1,
        "dm_id": dm_id,
        "message": "Hello World"
    })  
    msg_id = resp_send.json()['message_id']       
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token_1,
        'dm_id':dm_id,
        'start': 0})
    
    assert len(resp.json()['messages']) == 1    
    #Remove a message if input is ""
    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
        "token": token_1,
        "message_id": msg_id,
        "message": ""
    })   
    
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token':token_1,
        'dm_id':dm_id,
        'start': 0})
    
    assert resp_edit.status_code == 200
    assert len(resp.json()['messages']) == 0
  
    
def test_invalid_token(clear_and_register):

    resp_edit = requests.put(config.url + 'message/edit/v1', json = {
            "token": 'abc123',
            "message_id": 99999999999999,
            "message": "World Hello"
            })
    
    assert resp_edit.status_code == 403