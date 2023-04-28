import requests
from src import config

def test_check_return_sethandle():
    '''
    A simple test to check if the 
    auth_user_id returned when logging in is correct
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last",
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']

    resp_sethandle_1 = requests.put(config.url + 'user/profile/sethandle/v1', json={
        "token": token_1,
        "handle_str": "caspar",
    })
    assert resp_sethandle_1.status_code == 200
    assert len(resp_sethandle_1.json()) == 0

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "mahekshayeq@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_2.status_code == 200
    token_2 = resp_reg_2.json()['token']

    resp_sethandle_2 = requests.put(config.url + 'user/profile/sethandle/v1', json={
        "token": token_2,
        "handle_str": "differentcat"
    })
    assert resp_sethandle_2.status_code == 200
    assert len(resp_sethandle_2.json()) == 0

def test_handle_length_sethandle():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last",
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']

    resp_sethandle_1 = requests.put(config.url + 'user/profile/sethandle/v1', json={
        "token": token_1,
        "handle_str": "",
    })
    assert resp_sethandle_1.status_code == 400

    resp_sethandle_2 = requests.put(config.url + 'user/profile/sethandle/v1', json={
        "token": token_1,
        "handle_str": "applebatcatdogelephant",
        })
    assert resp_sethandle_2.status_code == 400

def test_handle_in_use_sethandle():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "Mahek",
        "name_last": "Mohammadi",
    })
    assert resp_reg_1.status_code == 200

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "different@gmail.com",
        "password": "LetsGO!",
        "name_first": "Nazneen",
        "name_last": "Shayeq",
    })
    assert resp_reg_2.status_code == 200
    token_2 = resp_reg_2.json()['token']
    #auth_user_id_2 = resp_reg_2.json()['auth_user_id']

    resp_sethandle_1 = requests.put(config.url + 'user/profile/sethandle/v1', json={
        "token": token_2,
        "handle_str": "mahekmohammadi",
    })
    assert resp_sethandle_1.status_code == 400


def test_handle_check_alphanumeric_sethandle():
    '''
    A simple test to check if the login endpoint
    will return an input error is the password is incorrect
    '''
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last",
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']

    resp_sethandle_1 = requests.put(config.url + 'user/profile/sethandle/v1', json={
        "token": token_1,
        "handle_str": "mahek@mohammadi",
    })
    assert resp_sethandle_1.status_code == 400

    resp_sethandle_2 = requests.put(config.url + 'user/profile/sethandle/v1', json={
        "token": token_1,
        "handle_str": "mahek_mohammadi",
    })
    assert resp_sethandle_2.status_code == 400


def test_invalid_token_sethandle():
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']

    resp_sethandle_1 = requests.put(config.url + 'user/profile/sethandle/v1', json={
        "token": token_1 + "a",
        "handle_str": "mahekmohammadi",
    })
    assert resp_sethandle_1.status_code == 403
