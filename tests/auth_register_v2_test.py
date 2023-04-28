import pytest
import requests
import json
from src import config

def test_check_return_register():
    '''
    A simple test to check if the 
    auth_user_id returned when logging in is correct
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "correct@gmail.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    assert type(resp_reg_1.json()['auth_user_id']) == int

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "correct1@gmail.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    assert type(resp_reg_2.json()['auth_user_id']) == int

def test_password_length_register():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "a@a.com",
        "password": "",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 400

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "a@a.com",
        "password": "apple",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 400

    resp_reg_3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "a@a.com",
        "password": "a"*500,
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_3.status_code == 200

    
def test_firstname_length_register():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "b@b.com",
        "password": "password",
        "name_first": "",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 400

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "b@b.com",
        "password": "password",
        "name_first": "a"*51,
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 400

    resp_reg_3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "b@b.com",
        "password": "password",
        "name_first": "a"*49,
        "name_last": "name_last"
    })
    assert resp_reg_3.status_code == 200

def test_lastname_length_register():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "c@c.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": ""
    })
    assert resp_reg_1.status_code == 400

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "c@c.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "a"*51
    })
    assert resp_reg_2.status_code == 400

    resp_reg_3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "c@c.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "a"*49
    })
    assert resp_reg_3.status_code == 200

def test_email_regex_register():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "@a.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 400

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "apple@.co",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 400

    resp_reg_3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "applegmail.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_3.status_code == 400

    resp_reg_4 = requests.post(config.url + 'auth/register/v2', json={
        "email": "apple@gmail.c",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_4.status_code == 400

    resp_reg_5 = requests.post(config.url + 'auth/register/v2', json={
        "email": "apple@gmail.com3",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_5.status_code == 400

    resp_reg_6 = requests.post(config.url + 'auth/register/v2', json={
        "email": "apple@gmail.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_6.status_code == 200

def test_email_valid_register():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "peach@gmail.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "peach@gmail.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 400

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "different@gmail.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "different@gmail.com",
        "password": "password",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 400

# check handle
def test_handle_same_handle_register():
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "a@abc.com",
        "password": "password",
        "name_first": "caspar1234567890",
        "name_last": "Chan"
    })
    assert resp_reg_1.status_code == 200
    auth_user_id_1 = resp_reg_1.json()['auth_user_id']
    token_1 = resp_reg_1.json()['token']

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "b@abc.com",
        "password": "password",
        "name_first": "caspar1234567890",
        "name_last": "Chan"
    })
    assert resp_reg_2.status_code == 200
    auth_user_id_2 = resp_reg_2.json()['auth_user_id']
    token_2 = resp_reg_2.json()['token']

    resp_reg_3 = requests.post(config.url + 'auth/register/v2', json={
        "email": "c@abc.com",
        "password": "password",
        "name_first": "caspar1234567890",
        "name_last": "Chan"
    })
    assert resp_reg_3.status_code == 200
    auth_user_id_3 = resp_reg_3.json()['auth_user_id']
    token_3 = resp_reg_3.json()['token']

    resp_reg_4 = requests.post(config.url + 'auth/register/v2', json={
        "email": "d@abc.com",
        "password": "password",
        "name_first": "Mahek",
        "name_last": "Mohammadi"
    })
    assert resp_reg_4.status_code == 200
    auth_user_id_4 = resp_reg_4.json()['auth_user_id']
    token_4 = resp_reg_4.json()['token']

    resp_user_1 = requests.get(config.url + '/user/profile/v1', params ={
        "token": token_1,
        "u_id": auth_user_id_1,
    })
    assert resp_user_1.json()['user']['handle_str'] == 'caspar1234567890chan'

    resp_user_2 = requests.get(config.url + '/user/profile/v1', params ={
        "token": token_2,
        "u_id": auth_user_id_2,
    })
    assert resp_user_2.json()['user']['handle_str'] == 'caspar1234567890chan0'

    resp_user_3 = requests.get(config.url + '/user/profile/v1', params ={
        "token": token_3,
        "u_id": auth_user_id_3,
    })
    assert resp_user_3.json()['user']['handle_str'] == 'caspar1234567890chan1'

    resp_user_4 = requests.get(config.url + '/user/profile/v1', params ={
        "token": token_4,
        "u_id": auth_user_id_4,
    })
    assert resp_user_4.json()['user']['handle_str'] == 'mahekmohammadi'
