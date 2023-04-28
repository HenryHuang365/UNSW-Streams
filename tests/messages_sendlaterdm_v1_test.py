#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 02:34:08 2021

@author: caspar
"""

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
def test_send_later_msg_id_correct(clear_and_register):
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': []
        })
    
    dm_id = dm_id.json()['dm_id']
    
    
    curr_time = datetime.now()        
    curr_timestamp = int(curr_time.timestamp())
    
    time_sent = datetime.now() + timedelta(seconds = 10)
    time_sent = int(time_sent.timestamp())
    
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
        })    

    requests.post(config.url + 'message/senddm/v1', json = {
        "token": token,
        "dm_id": dm_id,
        "message": "Hello World"
        })
    
    resp = requests.post(config.url + '/message/sendlaterdm/v1', json = {
        "token": token,
        'dm_id': dm_id,
        "message": "asd",
        "time_sent": time_sent
            })
    
    msg_id = resp.json()['message_id']
    assert resp.status_code == 200
    
    time_diff = time_sent - curr_timestamp
    time.sleep(time_diff + 1)
    resp_messages = requests.get(config.url + '/dm/messages/v1', params = {
        'token' : token,
        'dm_id' : dm_id,
        'start' : 0})
    
    assert resp_messages.json()['messages'][0]['message_id'] == msg_id
    assert msg_id == 3
    assert resp_messages.json()['messages'][0]['time_created'] == time_sent
    
def test_send_later_1_msg(clear_and_register):
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': []
        })
    
    dm_id = dm_id.json()['dm_id']
    
    
    curr_time = datetime.now()        
    curr_timestamp = int(curr_time.timestamp())
    
    time_sent = datetime.now() + timedelta(seconds = 10)
    time_sent = int(time_sent.timestamp())

    resp = requests.post(config.url + '/message/sendlaterdm/v1', json = {
        "token": token,
        'dm_id': dm_id,
        "message": "asd",
        "time_sent": time_sent
            })
    
    msg_id = resp.json()['message_id']
    assert resp.status_code == 200
    
    time_diff = time_sent - curr_timestamp
    time.sleep(time_diff + 1)
    
    resp_messages = requests.get(config.url + '/dm/messages/v1', params = {
        'token' : token,
        'dm_id' : dm_id,
        'start' : 0})
    
    assert resp_messages.json()['messages'][0]['message_id'] == msg_id
    assert resp_messages.json()['messages'][0]['time_created'] == time_sent
    
def test_invalid_chaneel(clear_and_register):
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': []
        })
    
    dm_id = dm_id.json()['dm_id']
    
    
    time_sent = datetime.now() + timedelta(seconds = 10)
    time_sent = int(time_sent.timestamp())
    
    resp = requests.post(config.url + '/message/sendlaterdm/v1', json = {
        "token": token,
        'dm_id': '565654646465',
        "message": "asd",
        "time_sent": time_sent
            })
    
    assert resp.status_code == 400          
    
    
def test_message_empty(clear_and_register):
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': []
        })
    
    dm_id = dm_id.json()['dm_id']
    
    
    time_sent = datetime.now() + timedelta(seconds = 10)
    time_sent = int(time_sent.timestamp())
    
    resp = requests.post(config.url + '/message/sendlaterdm/v1', json = {
        "token": token,
        'dm_id': dm_id,
        "message": "",
        "time_sent": time_sent
            })
    
    assert resp.status_code == 400       
    
    
def test_message_length_over_1000(clear_and_register):
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': []
        })
    
    dm_id = dm_id.json()['dm_id']
    

    
    time_sent = datetime.now() + timedelta(seconds = 10)
    time_sent = int(time_sent.timestamp())
    
    resp = requests.post(config.url + '/message/sendlaterdm/v1', json = {
        "token": token,
        'dm_id': dm_id,
        "message": "a"*1001,
        "time_sent": time_sent
            })
    
    
    assert resp.status_code == 400    
    
def test_time_sent_past(clear_and_register):
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': []
        })
    
    dm_id = dm_id.json()['dm_id']
    
    token = resp.json()['token'] 
    
    time_sent = datetime.now() - timedelta(seconds = 10)
    time_sent = int(time_sent.timestamp())
    
    resp = requests.post(config.url + '/message/sendlaterdm/v1', json = {
        "token": token,
        'dm_id': dm_id,
        "message": "asd",
        "time_sent": time_sent
            })
    
    assert resp.status_code == 400    
    
def test_valid_ch_not_member(clear_and_register):
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': []
        })
    
    dm_id = dm_id.json()['dm_id']
    
    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    time_sent = datetime.now() + timedelta(seconds = 10)
    time_sent = int(time_sent.timestamp())
    
    resp = requests.post(config.url + '/message/sendlaterdm/v1', json = {
        "token": token,
        'dm_id': dm_id,
        "message": "asd",
        "time_sent": time_sent
            })
    
    
    assert resp.status_code == 403    
    
def test_invalid_token(clear_and_register):

    resp = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp.json()['token'] 
    
    dm_id = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': []
        })
    
    dm_id = dm_id.json()['dm_id']

    
    time_sent = datetime.now() + timedelta(seconds = 10)
    time_sent = int(time_sent.timestamp())
    
    resp = requests.post(config.url + '/message/sendlaterdm/v1', json = {
        "token": 'asdasd',
        'dm_id': dm_id,
        "message": "asd",
        "time_sent": time_sent
            })
    
    assert resp.status_code == 403
    