"""
Created on Sun Oct 17 18:38:00 2021

@author: caspar
"""

import pytest
import requests
import json
from src import config

@pytest.fixture 
def clear_and_register():
    '''
    Clear and create user for temporary database
    '''
    #Clear
    requests.delete(config.url + '/clear/v1')
    
    #Register User 1
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'a@abc.com',
            'password': '123456',
            'name_first': 'aaspar',
            'name_last': 'last1'
        })
    token = resp.json()['token']
    
    #Logout User 1
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        })
    
    #Resgiter User 2
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'b@abc.com',
            'password': '123456',
            'name_first': 'baspar',
            'name_last': 'last2'
        })
    token = resp.json()['token']    
        
    #Logout User 2
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        }) 
    
def test_invalid_token(clear_and_register):
    '''
    Return AccessError if token is invalid
    '''
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token': 'InvalidToken',
        'dm_id': 0,
        'start': 1,
        })       
    
    assert resp.status_code == 403
    
    
def test_50_msgs(clear_and_register):
    '''
    Test if total of 50 msgs are returned from start to end
    '''
    resp_auth_login = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp_auth_login.json()['token']
    
    resp_dm_create = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })   
    dm_id = resp_dm_create.json()['dm_id']
    for _ in range(51):
        requests.post(config.url + '/message/senddm/v1', json = {
            'token':token,
            'dm_id': dm_id,
            'message':'ABDEFG'})
    
    resp_dm_messages = requests.get(config.url + '/dm/messages/v1', params = {
        'token' : token,
        'dm_id' : dm_id,
        'start' : 0})
    
    assert resp_dm_messages.status_code == 200
    assert resp_dm_messages.json()['end'] == 50
    assert len(resp_dm_messages.json()['messages']) == 50 
    
def test_no_msgs(clear_and_register):
    '''
    Test if msg is empty
    '''
    resp_auth_login = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp_auth_login.json()['token']
    
    resp_dm_create = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })   
    dm_id = resp_dm_create.json()['dm_id']

    resp_dm_messages = requests.get(config.url + '/dm/messages/v1', params = {
        'token' : token,
        'dm_id' : dm_id,
        'start' : 0})
    
    assert resp_dm_messages.status_code == 200
    assert resp_dm_messages.json()['end'] == -1
    assert resp_dm_messages.json()['messages'] == []
    
def test_less_than_50_msgs(clear_and_register):
    '''
    Test if there are less than 50 msgs from start to end
    '''
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })    
    dm_id = resp.json()['dm_id']
    for _ in range(20):
        requests.post(config.url + '/message/senddm/v1', json = {
            'token':token,
            'dm_id': dm_id,
            'message':'ABDEFG'})
        
    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token' : token,
        'dm_id' : dm_id,
        'start' : 0})
    
    assert resp.status_code == 200
    assert resp.json()['end'] == -1
    assert len(resp.json()['messages']) == 20 
    
def test_start_greater_msg(clear_and_register):
    '''
    Test if it returns a input error if start is > len of totoal msgs
    '''
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })    
    dm_id = resp.json()['dm_id']

    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token' : token,
        'dm_id' : dm_id,
        'start' : 2000000})   
    
    assert resp.status_code == 400
    
def test_dm_id_not_valid(clear_and_register):
    '''
    Test if it return input error if the dm_id is not existing
    '''
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })    

    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token' : token,
        'dm_id' : 4345343434,
        'start' : 2000000})   
    
    assert resp.status_code == 400

def test_not_member_in_dm(clear_and_register):
    '''
    Test if it returns access error if the auth user is not a member in the dm
    '''
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']  
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })    
    dm_id = resp.json()['dm_id']
    
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        }) 

    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']      

    resp = requests.get(config.url + '/dm/messages/v1', params = {
        'token' : token,
        'dm_id' : dm_id,
        'start' : 0})   
    
    assert resp.status_code == 403