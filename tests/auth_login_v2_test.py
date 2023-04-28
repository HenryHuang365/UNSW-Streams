import pytest
import requests
import json
from src import config

def test_check_return_login():
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
    auth_user_id_1 = resp_reg_1.json()['auth_user_id']

    resp_login_1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!"
    })
    assert resp_login_1.json()['auth_user_id'] == auth_user_id_1
    assert resp_login_1.status_code == 200

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "dog@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    auth_user_id_2 = resp_reg_2.json()['auth_user_id']

    resp_login_2 = requests.post(config.url + 'auth/login/v2', json={
        "email": "dog@gmail.com",
        "password": "LetsGO!"
    })
    assert resp_login_2.json()['auth_user_id'] == auth_user_id_2
    assert resp_login_2.status_code == 200

def test_check_login_password():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    response = requests.post(config.url + 'auth/login/v2', json={
        "email": "cat@gmail.com",
        "password": "wrong_password"
    })
    assert response.status_code == 400

    response = requests.post(config.url + 'auth/login/v2', json={
        "email": "cat@gmail.com",
        "password": "also_wrong_password"
    })
    assert response.status_code == 400

    response = requests.post(config.url + 'auth/login/v2', json={
        "email": "cat@gmail.com",
        "password": "worst_password"
    })
    assert response.status_code == 400

    response = requests.post(config.url + 'auth/login/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!"
    })
    assert response.status_code == 200

def test_check_login_email():
    '''
    A simple test to check if the login endpoint
    will return an input error is the email 
    has not been previously registered
    '''
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/login/v2', json={
        "email": "apple@gmail.com",
        "password": "any_password"
    })
    assert response.status_code == 400

    response = requests.post(config.url + 'auth/login/v2', json={
        "email": "bat@gmail.com",
        "password": "any_password"
    })
    assert response.status_code == 400

    response = requests.post(config.url + 'auth/login/v2', json={
        "email": "cat@gmail.com",
        "password": "any_password"
    })
    assert response.status_code == 400

    requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "any_password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    
    response = requests.post(config.url + 'auth/login/v2', json={
        "email": "cat@gmail.com",
        "password": "any_password"
    })
    assert response.status_code == 200


def test_two_sessions():
    '''
    A simple test to check if the login endpoint
    will return an input error is the email 
    has not been previously registered
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "any_password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    token_1 = resp_reg.json()['token']

    response = requests.post(config.url + 'auth/login/v2', json={
        "email": "cat@gmail.com",
        "password": "any_password"
    })
    token_2 = response.json()['token']

    resp_session_1 = requests.get(config.url + '/channels/listall/v2', params = {
        'token': token_1
    })
    assert resp_session_1.status_code == 200

    resp_session_2 = requests.get(config.url + '/channels/listall/v2', params = {
        'token': token_2
    })
    assert resp_session_2.status_code == 200