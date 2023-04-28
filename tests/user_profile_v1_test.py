import requests
from src import config

def test_basic_user():
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
    auth_user_id_1 = resp_reg_1.json()['auth_user_id']

    resp_profile_1 = requests.get(config.url + 'user/profile/v1', params={
        "token": token_1,
        "u_id": auth_user_id_1
    })
    assert resp_profile_1.status_code == 200
    assert resp_profile_1.json()['user']['u_id'] == auth_user_id_1
    assert resp_profile_1.json()['user']['email'] == "cat@gmail.com"
    assert resp_profile_1.json()['user']['name_first'] == "name_first"
    assert resp_profile_1.json()['user']['name_last'] == "name_last"
    assert resp_profile_1.json()['user']['handle_str'] == "namefirstnamelast"

def test_invalid_token_user():
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']
    auth_user_id_1 = resp_reg_1.json()['auth_user_id']

    resp_setname_1 = requests.get(config.url + 'user/profile/v1', params={
        "token": token_1 + "a",
        "u_id": auth_user_id_1,
    })
    assert resp_setname_1.status_code == 403

def test_invalid_id_user():
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']
    auth_user_id_1 = resp_reg_1.json()['auth_user_id']

    resp_profile_1 = requests.get(config.url + 'user/profile/v1', params={
        "token": token_1,
        "u_id": auth_user_id_1 + 2,
    })
    assert resp_profile_1.status_code == 400
