#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13

@author: mahek
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
            'email': 'a@abc.com',
            'password': '123456',
            'name_first': 'Firstname',
            'name_last': 'Lastname'
        })
    a_token = resp.json()['token']
    a_id = resp.json()['auth_user_id']

    #Resgiter User 2
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'b@abc.com',
            'password': '123456',
            'name_first': 'Firstname2',
            'name_last': 'Lastname2'
        })
    b_token = resp.json()['token']
    b_id = resp.json()['auth_user_id']

    #Resgiter User 3
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'c@abc.com',
            'password': '123456',
            'name_first': 'caspar',
            'name_last': 'last3'
        })
    c_token = resp.json()['token']   
    c_id = resp.json()['auth_user_id']

    #Resgiter User 4
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'd@abc.com',
            'password': '123456',
            'name_first': 'daspar',
            'name_last': 'last4'
        })
    d_token = resp.json()['token']
    d_id = resp.json()['auth_user_id']

    return {
        "a_token": a_token,
        "a_id": a_id,
        "b_token": b_token,
        "b_id": b_id,
        "c_token": c_token,
        "c_id": c_id,
        "d_token": d_token,
        "d_id": d_id,
    }
        
# test to see if when user in channel they get notified when they
# enter channel
def test_add_to_channel(clear_and_register):    

    tokens = clear_and_register

    response_create_channels = requests.post(config.url + "channels/create/v2",json={
        "token": tokens["a_token"],
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]
    requests.post(config.url + '/channel/invite/v2', json = {
        'token': tokens["a_token"],
        'channel_id': channel_id, 
        'u_id': tokens["b_id"],
        })
    resp_notifications = requests.get(config.url + 'notifications/get/v1', params = {
        'token': tokens["b_token"]
        })
    assert resp_notifications.status_code == 200
    assert resp_notifications.json()["notifications"] == [{
        "channel_id": channel_id,
        "dm_id": -1,
        "notification_message": "firstnamelastname added you to COMP1531"
    }]

# tag user in channel and see the response
def test_tag_user_in_channel(clear_and_register):    

    tokens = clear_and_register

    response_create_channels = requests.post(config.url + "channels/create/v2",json={
        "token": tokens["a_token"],
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]
    requests.post(config.url + '/channel/invite/v2', json = {
        'token': tokens["a_token"],
        'channel_id': channel_id, 
        'u_id': tokens["b_id"],
        })
    requests.post(config.url + 'message/send/v1', json = {
        "token": tokens["a_token"],
        "channel_id": channel_id,
        "message": "Hello World @firstname2lastname2"
            })
    resp_notifications = requests.get(config.url + 'notifications/get/v1', params = {
        'token': tokens["b_token"]
        })
    assert resp_notifications.status_code == 200
    assert resp_notifications.json()["notifications"] == [
        {
        "channel_id": channel_id,
        "dm_id": -1,
        "notification_message": "firstnamelastname tagged you in COMP1531: Hello World @firstna"
        },
        {
        "channel_id": channel_id,
        "dm_id": -1,
        "notification_message": "firstnamelastname added you to COMP1531"
    }]

def test_wrong_token(clear_and_register):    

    tokens = clear_and_register

    response_create_channels = requests.post(config.url + "channels/create/v2",json={
        "token": tokens["a_token"],
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]
    requests.post(config.url + '/channel/invite/v2', json = {
        'token': tokens["a_token"],
        'channel_id': channel_id, 
        'u_id': tokens["b_id"],
        })
    resp_notifications = requests.get(config.url + 'notifications/get/v1', params = {
        'token': "random"
        })
    assert resp_notifications.status_code == 403

def test_add_to_dm(clear_and_register):    

    tokens = clear_and_register

    create_dm = requests.post(config.url + '/dm/create/v1', json = {
        'token':tokens["a_token"],
        'u_ids': [tokens["b_id"]]
        })
    dm_id = create_dm.json()["dm_id"]
    
    resp_notifications = requests.get(config.url + 'notifications/get/v1', params = {
        'token': tokens["b_token"]
        })
    assert resp_notifications.status_code == 200
    assert resp_notifications.json()["notifications"] == [{
        "channel_id": -1,
        "dm_id": dm_id,
        "notification_message": "firstnamelastname added you to firstname2lastname2, firstnamelastname"
    }]

def test_tag_user_in_dm(clear_and_register):    

    tokens = clear_and_register

    create_dm = requests.post(config.url + '/dm/create/v1', json = {
        'token':tokens["a_token"],
        'u_ids': [tokens["b_id"]]
        })
    dm_id = create_dm.json()["dm_id"]
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": tokens["a_token"],
        "dm_id": dm_id,
        "message": "Hello World @firstname2lastname2"
        })
    requests.post(config.url + 'message/senddm/v1', json = {
        "token": tokens["a_token"],
        "dm_id": dm_id,
        "message": "Hello World @casparlast3"
        })
    resp_notifications = requests.get(config.url + 'notifications/get/v1', params = {
        'token': tokens["b_token"]
        })
    assert resp_notifications.status_code == 200
    assert resp_notifications.json()["notifications"] == [
        {
        "channel_id": -1,
        "dm_id": dm_id,
        "notification_message": "firstnamelastname tagged you in firstname2lastname2, firstnamelastname: Hello World @firstna"
        },
        {
        "channel_id": -1,
        "dm_id": dm_id,
        "notification_message": "firstnamelastname added you to firstname2lastname2, firstnamelastname"
    }]
    resp_notifications = requests.get(config.url + 'notifications/get/v1', params = {
        'token': tokens["c_token"]
        })
    assert resp_notifications.status_code == 200
    assert resp_notifications.json()["notifications"] == []

def test_react_in_channel(clear_and_register):    

    tokens = clear_and_register

    response_create_channels = requests.post(config.url + "channels/create/v2",json={
        "token": tokens["a_token"],
        "name": "COMP1531",
        "is_public": True
    })
    channel_id = response_create_channels.json()["channel_id"]
    requests.post(config.url + '/channel/invite/v2', json = {
        'token': tokens["a_token"],
        'channel_id': channel_id, 
        'u_id': tokens["b_id"],
        })
    send_message = requests.post(config.url + 'message/send/v1', json = {
        "token": tokens["a_token"],
        "channel_id": channel_id,
        "message": "Hello World @firstname2lastname2"
            })
    msg_id = send_message.json()['message_id']
    requests.post(config.url + 'message/react/v1', json = {
        "token": tokens["b_token"],
        "message_id": msg_id,
        "react_id": 1
            })
    notifications_a = requests.get(config.url + 'notifications/get/v1', params = {
        'token': tokens["a_token"]
        })
    assert notifications_a.status_code == 200
    assert notifications_a.json()["notifications"] == [{
        "channel_id": channel_id,
        "dm_id": -1,
        "notification_message": "firstname2lastname2 reacted to your message in COMP1531"
        }]

    notifications_b = requests.get(config.url + 'notifications/get/v1', params = {
        'token': tokens["b_token"]
        })
    assert notifications_b.status_code == 200
    assert notifications_b.json()["notifications"] == [
        {
        "channel_id": channel_id,
        "dm_id": -1,
        "notification_message": "firstnamelastname tagged you in COMP1531: Hello World @firstna"
        },
        {
        "channel_id": channel_id,
        "dm_id": -1,
        "notification_message": "firstnamelastname added you to COMP1531"
    }]

# needed: test to see that there are only 20 notifications