import pytest
import requests
import json
from src import config

def test_check_base_case():
    '''
    A simple test to check if the 
    auth_user_id returned when logging in is correct
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "mahekshayeq@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200

    resp_change_request = requests.post(config.url + 'auth/passwordreset/request/v1', json={
        "email": "mahekshayeq@gmail.com",
    })
    assert resp_change_request.status_code == 200

def test_mutliple_users():
    '''
    A simple test to check if the 
    auth_user_id returned when logging in is correct
    '''
    requests.delete(config.url + 'clear/v1')

    requests.post(config.url + 'auth/register/v2', json={
        "email": "mahekshayeq@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })

    requests.post(config.url + 'auth/register/v2', json={
        "email": "abq@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    requests.post(config.url + 'auth/register/v2', json={
        "email": "cd@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })

    resp_change_request = requests.post(config.url + 'auth/passwordreset/request/v1', json={
        "email": "mahekshayeq@gmail.com",
    })
    assert resp_change_request.status_code == 200

def test_check_invalid_email():
    '''
    A simple test to check if the 
    auth_user_id returned when logging in is correct
    '''
    requests.delete(config.url + 'clear/v1')

    resp_change_request = requests.post(config.url + 'auth/passwordreset/request/v1', json={
        "email": "mahekshayeq@gmail.com",
    })
    assert resp_change_request.status_code == 200

def test_sessions_logged_out():
    '''
    A simple test to check if the 
    auth_user_id returned when logging in is correct
    '''
    requests.delete(config.url + 'clear/v1')
    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "mahekshayeq@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']

    resp_login_1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "mahekshayeq@gmail.com",
        "password": "LetsGO!"
    })
    assert resp_login_1.status_code == 200
    token_2 = resp_login_1.json()['token']

    resp_change_request = requests.post(config.url + 'auth/passwordreset/request/v1', json={
        "email": "mahekshayeq@gmail.com",
    })
    assert resp_change_request.status_code == 200

    resp = requests.get(config.url + '/channels/listall/v2', params = {
        'token': token_1
        })
    assert resp.status_code == 403

    resp_logout_2 = requests.post(config.url + 'auth/logout/v1', json={
        "token": token_2
    })
    assert resp_logout_2.status_code == 403

def test_inccorrect_code():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + "auth/register/v2",json={
        "email": "a@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    resp_reset_1 = requests.post(config.url + 'auth/passwordreset/reset/v1', json={
        "reset_code": "..WyS1Vl0EHFSFsh4I7PL8e6d-kWag37ATAdWF_VhoSxM",
        "new_password": "new_password",
    })
    assert resp_reset_1.status_code == 400

def test_inccorrect_password_length():
    requests.delete(config.url + 'clear/v1')
    requests.post(config.url + "auth/register/v2",json={
        "email": "a@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    resp_reset_1 = requests.post(config.url + 'auth/passwordreset/reset/v1', json={
        "reset_code": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFAZ21haWwuY29tIn0.WyS1Vl0EHFSFsh4I7PL8e6d-kWag37ATAdWF_VhoSxM",
        "new_password": "",
    })
    assert resp_reset_1.status_code == 400

# def test_correct_case():
#     requests.delete(config.url + 'clear/v1')
#     requests.post(config.url + "auth/register/v2",json={
#         "email": "a@gmail.com",
#         "password": "old_password",
#         "name_first": "name_first",
#         "name_last": "name_last"
#     })
#     requests.post(config.url + "auth/register/v2",json={
#         "email": "b@gmail.com",
#         "password": "LetsGO!",
#         "name_first": "name_first",
#         "name_last": "name_last"
#     })
#     resp_change_request = requests.post(config.url + 'auth/passwordreset/request/v1', json={
#         "email": "a@gmail.com",
#     })
#     assert resp_change_request.status_code == 200
#     reset_code = resp_change_request.json()['reset_code']
#     resp_reset_1 = requests.post(config.url + 'auth/passwordreset/reset/v1', json={
#         "reset_code": reset_code,
#         "new_password": "Hello@2021",
#     })
#     assert resp_reset_1.status_code == 200

#     resp_login_1 = requests.post(config.url + 'auth/login/v2', json={
#         "email": "a@gmail.com",
#         "password": "old_password"
#     })
#     assert resp_login_1.status_code == 400

#     resp_login_2 = requests.post(config.url + 'auth/login/v2', json={
#         "email": "a@gmail.com",
#         "password": "Hello@2021"
#     })
#     assert resp_login_2.status_code == 200