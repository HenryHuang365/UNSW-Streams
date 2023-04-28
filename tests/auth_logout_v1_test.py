import pytest
import requests
import json
from src import config

def test_check_return_logout():
    '''
    A simple test to check if the 
    auth_user_id returned when logging in is correct
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']

    resp_logout_1 = requests.post(config.url + 'auth/logout/v1', json={
        "token": token_1
    })
    assert resp_logout_1.status_code == 200
    assert len(resp_logout_1.json()) == 0

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "dog@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 200
    token_2 = resp_reg_2.json()['token']

    resp_logout_2 = requests.post(config.url + 'auth/logout/v1', json={
        "token": token_2
    })
    assert resp_logout_2.status_code == 200
    resp = requests.get(config.url + '/channels/listall/v2', params = {
        'token': token_2
    })
    assert resp.status_code == 403
    

def test_check_logout_invalid_token():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']

    resp_logout_1 = requests.post(config.url + 'auth/logout/v1', json={
        "token": token_1 +'1'
    })
    assert resp_logout_1.status_code == 403

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "dog@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 200
    token_2 = resp_reg_2.json()['token']

    resp_logout_2 = requests.post(config.url + 'auth/logout/v1', json={
        "token": token_2 + 'm'
    })
    assert resp_logout_2.status_code == 403