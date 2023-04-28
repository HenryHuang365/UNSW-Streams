#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 23:24:41 2021

@author: caspar
"""
import pytest
import requests
import json
from src import config



@pytest.fixture()
def clear_and_register_create_channel():
    '''
    Clear and create user for temporary database
    '''
    #Clear
    requests.delete(config.url + '/clear/v1')
    
    #Register User 1
    resp = requests.post(config.url + '/auth/register/v2', json ={
            'email': 'a@abc.com',
            'password': '123456',
            'name_first': 'Firstname',
            'name_last': 'Lastname'
        })
    token = resp.json()['token']
    
    #Create channel 1
    resp = requests.post(config.url + '/channels/create/v2', json = {
        'token': token,
        'name':'test_channel_1',
        'is_public': True
        })
    
    #Resgiter User 2
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'b@abc.com',
            'password': '123456',
            'name_first': 'Firstname2',
            'name_last': 'Lastname2'
        })
    token = resp.json()['token']    
    
    #Create channel 2
    resp = requests.post(config.url + '/channels/create/v2', json = {
        'token': token,
        'name':'test_channel_2',
        'is_public': True
        })
    
    #Logout User 2
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        })

    
def test_channels_list(clear_and_register_create_channel):
    '''
    Only shows the channel that User 1 is in (channel 1)
    '''
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']
    
    #Create one more channel
    resp = requests.post(config.url + '/channels/create/v2', json={
        'token': token,
        'name': "test_channel_3",
        'is_public': False
    })
    
    resp = requests.get(config.url + '/channels/list/v2', params = {
        'token': token
        })
    
    #correct_list = []
    assert resp.status_code == 200
    assert resp.json()['channels'] == [{
                    'channel_id': 1,
                    'name': 'test_channel_1'
                },
                {
                    'channel_id': 3,
                    'name': 'test_channel_3'
                }
            ]
    
def test_invalid_token():
    resp = requests.get(config.url + '/channels/list/v2', params = {
        'token': "InvalidToken"
        })
    assert resp.status_code == 403    
