import requests
from src import config

def test_check_return_setname():
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

    resp_setname_1 = requests.put(config.url + 'user/profile/setname/v1', json={
        "token": token_1,
        "name_first": "Scheherezade",
        "name_last": "Noor"
    })
    assert resp_setname_1.status_code == 200
    assert len(resp_setname_1.json()) == 0

    resp_reg_2 = requests.post(config.url + 'auth/register/v2', json={
        "email": "different@gmail.com",
        "password": "LetsGO!",
        "name_first": "mahek",
        "name_last": "mohammadi"
    })
    assert resp_reg_2.status_code == 200
    token_2 = resp_reg_2.json()['token']

    resp_setname_2 = requests.put(config.url + 'user/profile/setname/v1', json={
        "token": token_2,
        "name_first": "Alizeh",
        "name_last": "Zaidi"
    })
    assert resp_setname_2.status_code == 200
    assert len(resp_setname_2.json()) == 0

def test_firstname_setname():
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

    resp_setname_1 = requests.put(config.url + 'user/profile/setname/v1', json={
        "token": token_1,
        "name_first": "",
        "name_last": "new_name"
    })
    assert resp_setname_1.status_code == 400

    resp_setname_2 = requests.put(config.url + 'user/profile/setname/v1', json={
        "token": token_1,
        "name_first": "a"*51,
        "name_last": "new_name"
    })
    assert resp_setname_2.status_code == 400

def test_lastname_setname():
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

    resp_setname_1 = requests.put(config.url + 'user/profile/setname/v1', json={
        "token": token_1,
        "name_first": "new_name",
        "name_last": ""
    })
    assert resp_setname_1.status_code == 400

    resp_setname_2 = requests.put(config.url + 'user/profile/setname/v1', json={
        "token": token_1,
        "name_first": "new_name",
        "name_last": "a"* 51
    })
    assert resp_setname_2.status_code == 400

def test_invalid_token_setname():
    requests.delete(config.url + 'clear/v1')

    resp_reg_1 = requests.post(config.url + 'auth/register/v2', json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })
    assert resp_reg_1.status_code == 200
    token_1 = resp_reg_1.json()['token']

    resp_setname_1 = requests.put(config.url + 'user/profile/setname/v1', json={
        "token": token_1 + "a",
        "name_first": "Scheherezade",
        "name_last": "Noor"
    })
    assert resp_setname_1.status_code == 403
