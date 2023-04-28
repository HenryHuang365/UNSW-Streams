#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 08:00:36 2021

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
            'name_first': 'Firstname',
            'name_last': 'Lastname'
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
            'name_first': 'Firstname2',
            'name_last': 'Lastname2'
        })
    token = resp.json()['token']    
        
    #Logout User 2
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        }) 
    
def test_create_one_DM(clear_and_register):
    '''
    A simple test to check if the dm returns correct dm_id and create a DM
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
    
    assert resp.status_code == 200
    assert type(resp.json()['dm_id']) == int    
    assert resp.json()['dm_id'] == 1

def test_create_mulitple_DMs(clear_and_register):
    '''
    A simple test to check if the dm returns correct dm_id and create 3DMs
    '''    
  
    #Register two additional user
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'hj@abc.com',
            'password': '123456',
            'name_first': 'Firstname123',
            'name_last': 'Lastname123'
        })    

    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'bk@abc.com',
            'password': '123456',
            'name_first': 'Firstname123',
            'name_last': 'Lastname123'
        })
    
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']    
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1,3]
        })
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1,4]
        })    
    
    assert resp.status_code == 200
    assert type(resp.json()['dm_id']) == int    
    assert resp.json()['dm_id'] == 3
    
    
def test_empty_uids(clear_and_register):
    '''
    If empty u_id list is given, the DM shd be create with the user himself
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
    assert resp.status_code == 200
    assert type(resp.json()['dm_id']) == int    
    assert resp.json()['dm_id'] == 1    
    
    
def test_invalid_token(clear_and_register):
    '''
    Return AccessError if token is invalid
    '''
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token': 'InvalidToken',
        'u_ids': []
        })       
    
    assert resp.status_code == 403
    
def test_u_id_not_valid(clear_and_register):
    '''
    Return InputError if u_id is invalid
    '''
    resp = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token = resp.json()['token']
    
    resp = requests.post(config.url + '/dm/create/v1', json = {
        'token': token,
        'u_ids': [1,2,12314124512312312]
        })       
    
    assert resp.status_code == 400