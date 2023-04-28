import pytest
import requests
import json
from src import config

"""
Testing the message remove function
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

def test_join_simple(clear_and_register):
    
    resp = requests.post(config.url + '/auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token_1 = resp.json()['token'] 
    
    resp = requests.post(config.url + '/channels/create/v2', json = {
        "token": token_1,
        "name": "channel1",
        "is_public": True
    })
    ch_id = resp.json()['channel_id']
    
    resp_2 = requests.post(config.url + '/auth/login/v2', json = {
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token_2 = resp_2.json()['token']
    
    resp = requests.post(config.url + 'channel/join/v2', json = {
        'token': token_2,
        'channel_id': ch_id
        })       
    
    assert resp.status_code == 200

def test_invalid_channel_id(clear_and_register):
    
    resp = requests.post(config.url + '/auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token_1 = resp.json()['token'] 
    
    resp_join = requests.post(config.url + '/channel/join/v2', json = {
        "token": token_1,
        "channel_id": '111111'
        })
    
    assert resp_join.status_code == 400
    
def test_user_already_in_channel(clear_and_register):
    
    resp = requests.post(config.url + '/auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token_1 = resp.json()['token'] 
    
    resp = requests.post(config.url + '/channels/create/v2', json = {
        "token": token_1,
        "name": "channel1",
        "is_public": True
    })
    ch_id = resp.json()['channel_id']
    
    
    resp_join = requests.post(config.url + '/channel/join/v2', json = {
        "token": token_1,
        "channel_id": ch_id
    })
    
    assert resp_join.status_code == 400
    
def test_join_private_channel(clear_and_register):
    #First user created is global owner
    resp = requests.post(config.url + '/auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token_1 = resp.json()['token'] 
    
    resp_2 = requests.post(config.url + '/auth/login/v2', json = {
        "email": "second.person@email.com",
        "password": "password"
    })
    token_2 = resp_2.json()['token']
    
    resp = requests.post(config.url + '/channels/create/v2', json = {
        "token": token_2,
        "name": "channel1",
        "is_public": False
    })
    
    resp = requests.post(config.url + '/channels/create/v2', json = {
        "token": token_2,
        "name": "channel1",
        "is_public": False
    })
    channel_id = resp.json()['channel_id']
    
    #Global owner has permission to join private channels
    resp_join = requests.post(config.url + '/channel/join/v2', json = {
            "token": token_1,
            "channel_id": channel_id
    })
    
    requests.get(config.url + '/channel/details/v2', json = {
        "token": token_1,
        "channel_id": channel_id
        })
    
    assert resp_join.status_code == 200
    
    resp_3 = requests.post(config.url + '/auth/register/v2', json={
        "email": "third.person@email.com",
        "password": "password",
        "name_first": "Bey",
        "name_last": "Blade"
        })
    
    token_3 = resp_3.json()['token']
    
    #User is a general member and does not have permission to join
    resp_join = requests.post(config.url + '/channel/join/v2', json = {
        "token": token_3,
        "channel_id": channel_id
        })
    
    assert resp_join.status_code == 403
    
def test_invalid_token(clear_and_register):
    '''
    Return AccessError if token is invalid
    '''
    resp = requests.post(config.url + 'channel/join/v2', json = {
        'token': 'InvalidToken',
        'channel_id': 5464564
        })       
    
    assert resp.status_code == 403