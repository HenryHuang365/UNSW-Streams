#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 17:34:41 2021

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
    
def test_user_in_1DM(clear_and_register):
    '''
    Only 1dm created by the user
    '''
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']
       
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': []
        })    
    
    resp = requests.get(config.url + '/dm/list/v1', params = {
        'token':token,
        })        
    assert resp.status_code == 200
    assert type(resp.json()['dms']) == list
    assert resp.json()['dms'] == [{
        "dm_id": 1,
        "name": 'basparlast2',
        }]
    
def test_user_in_3DM(clear_and_register):
    #Register two additional user
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'c@abc.com',
            'password': '123456',
            'name_first': 'caspar',
            'name_last': 'last3'
        })    

    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'd@abc.com',
            'password': '123456',
            'name_first': 'daspar',
            'name_last': 'last4'
        })
    
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']    
    #Create 2 DMs
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [3]
        })
 
    #logout then login and create 2DM as another user
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        })  
    
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'c@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']       
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1,2]
        })   

    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [4]
        })           
    
    resp = requests.get(config.url + '/dm/list/v1', params = {
        'token': token,
        })        
    assert resp.status_code == 200
    assert type(resp.json()['dms']) == list
    assert resp.json()['dms'] == [{
        "dm_id": 2,
        "name": 'basparlast2, casparlast3',
        },
        {
        "dm_id": 3,
        "name": 'aasparlast1, basparlast2, casparlast3',
        },
        {
        "dm_id": 4,
        "name": 'casparlast3, dasparlast4',
        }]
    
def test_invalid_token(clear_and_register):
    '''
    Return AccessError if token is invalid
    '''
    resp = requests.get(config.url + '/dm/list/v1', params = {
        'token': 'InvalidToken',
        'u_ids': []
        })       
    
    assert resp.status_code == 403