#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:18:22 2021

@author: caspar
"""
import pytest
import requests
import json
from src import config

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
    
def test_search_caspar(clear_and_register):    
    '''
    Search for Caspar in msg 
    '''
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })    
    token = resp.json()['token']    
    #create dm and send msg in dms
    resp_dm_1 = requests.post(config.url + 'dm/create/v1', json = {
        'token':token,
        'u_ids':[]})
    
    resp_dm_2 = requests.post(config.url + 'dm/create/v1', json = {
        'token':token,
        'u_ids':[2]})    

    dm_id_1 = resp_dm_1.json()['dm_id']
    dm_id_2 = resp_dm_2.json()['dm_id']
    
    #DM 1 -> 2 Caspar
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id_1,
        "message": "Hello World"
        })    
    
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id_1,
        "message": "Hello Caspar"
        })    
    
    #DM 2 -> 1 Caspar
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id_2,
        "message": "No one"
        })   
    
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id_2,
        "message": "asdCasparadasd one"
        })   
    
    #Create channels and send msg in channels
    ch_id_1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })   
    ch_id_2 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })    
    
    ch_id_1 = ch_id_1.json()['channel_id']
    ch_id_2 = ch_id_2.json()['channel_id']   
    
    requests.post(config.url + '/channel/invite/v2', json = {
        'token':token,
        'channel_id': ch_id_2, 
        'u_id': 2,
        })       
    
    #CH1 -> 1 Caspar
    requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": ch_id_1,
        "message": "Bye Caspar"
            })    
    
    requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": ch_id_1,
        "message": "See you"
            })       
    #logout user 1
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        }) 
    
    #login user 2
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })        
    token = resp.json()['token']
    
    #CH2 -> 3 Caspar
    requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": ch_id_2,
        "message": "See you Caspar"
            })        
    
    requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": ch_id_2,
        "message": "Bye Caspar"
            })

    requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": ch_id_2,
        "message": "Yo Caspar"
            })
    
    requests.post(config.url + 'message/send/v1', json = {
        "token": token,
        "channel_id": ch_id_2,
        "message": "Yo"
            })
    
    resp = requests.get(config.url + '/search/v1', params = {
        'token': token,
        'query_str': 'Caspar',
        })       
    
    assert resp.status_code == 200
    assert len(resp.json()['messages']) == 4
    
def test_string_too_short(clear_and_register):
    '''
    Return InputError for empty string
    '''
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    resp = requests.get(config.url + '/search/v1', params = {
        'token': token,
        'query_str': ''
        })       
    
    assert resp.status_code == 400        
    
def test_string_too_long(clear_and_register):
    '''
    Return InputError for string over 1000 chrarcters
    '''
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    resp = requests.get(config.url + '/search/v1', params = {
        'token': token,
        'query_str': 'a'*1001
        })       
    
    assert resp.status_code == 400    
    
    
def test_invalid_token(clear_and_register):
    '''
    Return AccessError if token is invalid
    '''
    resp = requests.get(config.url + '/search/v1', params = {
        'token': 'InvalidToken',
        'query_str': 'abc'
        })       
    
    assert resp.status_code == 403
    