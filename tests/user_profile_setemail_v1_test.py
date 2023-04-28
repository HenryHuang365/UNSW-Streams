import requests
from src import config

def test_check_return_setemail():
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

    resp_setemail_1 = requests.put(config.url + 'user/profile/setemail/v1', json={
        "token": token_1,
        "email": "different@gmail.com"
    })
    assert resp_setemail_1.status_code == 200
    assert len(resp_setemail_1.json()) == 0

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "carrot@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 200
    token_2 = resp_reg_2.json()['token']

    resp_setemail_2 = requests.put(config.url + 'user/profile/setemail/v1', json={
        "token": token_2,
        "email": "new@gmail.com"
    })
    assert resp_setemail_2.status_code == 200
    assert len(resp_setemail_2.json()) == 0

def test_email_invalid_setemail():
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

    resp_setemail_1 = requests.put(config.url + 'user/profile/setemail/v1', json={
        "token": token_1,
        "email": "@gmail.com"
    })
    assert resp_setemail_1.status_code == 400

    resp_setemail_2 = requests.put(config.url + 'user/profile/setemail/v1', json={
        "token": token_1,
        "email": "a@b.c"
    })
    assert resp_setemail_2.status_code == 400

def test_email_in_use_setemail():
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

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "different@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 200
    token_2 = resp_reg_2.json()['token']
    # auth_user_id_2 = resp_reg_2.json()['auth_user_id']

    resp_setemail_1 = requests.put(config.url + 'user/profile/setemail/v1', json={
        "token": token_2,
        "email": "cat@gmail.com"
    })
    assert resp_setemail_1.status_code == 400

    resp_setemail_2 = requests.put(config.url + 'user/profile/setemail/v1', json={
        "token": token_1,
        "email": "different@gmail.com"
    })
    assert resp_setemail_2.status_code == 400

def test_invalid_token_setemail():
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']
    # auth_user_id_1 = resp_reg_1.json()['auth_user_id']

    resp_setname_1 = requests.put(config.url + 'user/profile/setemail/v1', json={
        "token": token_1 + "a",
        "email": "new@gmail.com",
    })
    assert resp_setname_1.status_code == 403
