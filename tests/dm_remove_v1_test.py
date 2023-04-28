import pytest
import requests
import json
from src import config
from src.token_funcs import decode_token, check_valid_token

@pytest.fixture()
def clear_and_register_create_channel():
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

    #Resgiter User 3
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'c@abc.com',
            'password': '123456',
            'name_first': 'caspar',
            'name_last': 'last3'
        })
    token = resp.json()['token']   

    #Resgiter User 4
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'd@abc.com',
            'password': '123456',
            'name_first': 'daspar',
            'name_last': 'last4'
        })
    token = resp.json()['token']  
        
    #Logout User 4
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        }) 

def test_dm_remove(clear_and_register_create_channel):
    # test for the functionality of dm_remove
    # if it removes a dm properly
    
    resp_register1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        }) 
    assert resp_register1.status_code == 200
    # get token
    token = resp_register1.json()['token']
    
    u_id = decode_token(token)['u_id']

    resp_register2 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        }) 
    # get token
    token2 = resp_register2.json()['token']
    u_id2 = decode_token(token2)['u_id']

    resp_register3 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'c@abc.com',
        'password': '123456'
        }) 
    # get token
    token3 = resp_register3.json()['token']
    u_id3 = decode_token(token3)['u_id']

    resp_register4 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'd@abc.com',
        'password': '123456'
        }) 
    # get token
    token4 = resp_register4.json()['token']

    resp_dm_id = requests.post(config.url + '/dm/create/v1', json = {
        'token':token2,
        'u_ids': [u_id],
        })
    # get dm_id
    assert resp_dm_id.status_code == 200
    dm_id = resp_dm_id.json()['dm_id']

    resp_dm_id2 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token4,
        'u_ids': [u_id2, u_id3],
        })
    
    requests.post(config.url + '/dm/create/v1', json = {
        'token':token4,
        'u_ids': [u_id2, u_id3],
        })
    assert resp_dm_id2.status_code == 200
    dm_id2 = resp_dm_id2.json()['dm_id']
    
    resp_remove = requests.delete(config.url + '/dm/remove/v1', json = {
        'token':token2,
        'dm_id': dm_id,
        })
    
    assert resp_remove.status_code == 200
    
    resp_details = requests.get(config.url + '/dm/details/v1', params = {
        'token':token,
        'dm_id': dm_id,
        })
    # raise an InputError since the dm_id is not valid
    # 400 error code for InputError
    assert resp_details.status_code == 400

    resp_remove2 = requests.delete(config.url + '/dm/remove/v1', json = {
        'token':token4,
        'dm_id': dm_id2,
        })
    
    assert resp_remove2.status_code == 200
    
    resp_details2 = requests.get(config.url + '/dm/details/v1', params = {
        'token':token2,
        'dm_id': dm_id2,
        })
    # raise an InputError since the dm_id is not valid
    # 400 error code for InputError
    assert resp_details2.status_code == 400
    
def test_invalid_dm_id(clear_and_register_create_channel):
    
    
    resp1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        }) 
    # get token
    token = resp1.json()['token']
    
    requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })
    # get dm_id
    # dm_id = resp2.json()['dm_id']
    
    resp_remove = requests.delete(config.url + '/dm/remove/v1', json = {
        'token':token,
        'dm_id': -100,
        })
    
    # raise an InputError since the dm_id is not valid
    # 400 error code for InputError
    assert resp_remove.status_code == 400

def test_invalid_token(clear_and_register_create_channel):
    
    
    resp1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        }) 
    # get token
    token = resp1.json()['token']
    
    resp2 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })
    # get dm_id
    dm_id = resp2.json()['dm_id']
    
    resp_remove = requests.delete(config.url + '/dm/remove/v1', json = {
        'token':'invalid owner',
        'dm_id': dm_id,
        })
    
    # raise an AccessError since the token is not valid
    # 403 error code for AccessError
    assert resp_remove.status_code == 403

def test_auth_user_not_creator(clear_and_register_create_channel):
    
    
    resp1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        }) 
    # get token
    token = resp1.json()['token']

    resp_register2 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        }) 
    # get token
    token2 = resp_register2.json()['token']
    
    resp2 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })
    # get dm_id
    dm_id = resp2.json()['dm_id']
    
    resp_remove = requests.delete(config.url + '/dm/remove/v1', json = {
        'token':token2,
        'dm_id': dm_id,
        })
    
    # raise an AccessError since the token is not valid
    # 403 error code for AccessError
    assert resp_remove.status_code == 403
