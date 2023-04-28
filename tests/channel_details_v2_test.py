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
            'name_first': 'aaspar',
            'name_last': 'last1'
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
            'name_first': 'baspar',
            'name_last': 'last2'
        })
    token = resp.json()['token']    
        
    #Logout User 2
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        }) 
    
def test_channel_details_v2(clear_and_register_create_channel):
   
    resp_register1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        })    
    token1 = resp_register1.json()['token']
    u_id = decode_token(token1)['u_id']

    resp_channel_id = requests.post(config.url + '/channels/create/v2', json = {
        'token':token1,
        'name': 'channel1', 
        'is_public': True,
        })    
    channel_id = resp_channel_id.json()['channel_id']
    resp_details = requests.get(config.url + '/channel/details/v2', params = {
        'token':token1,
        'channel_id': channel_id,
        })        
    assert resp_details.status_code == 200
    assert resp_details.json()['name'] == 'channel1'
    assert resp_details.json()['is_public'] == True
    assert resp_details.json()['owner_members'][0]['u_id'] == u_id
    assert resp_details.json()['all_members'][0]['u_id'] == u_id
    
def test_invalid_channel(clear_and_register_create_channel):
   
    resp_register1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        })    
    token1 = resp_register1.json()['token']

    resp = requests.post(config.url + '/channels/create/v2', json = {
        'token':token1,
        'name': 'channel1', 
        'is_public': True,
        })    
    resp = requests.get(config.url + '/channel/details/v2', params = {
        'token':token1,
        'channel_id': -100,
        }) 

    # raise an InputError since the channel_id is not valid
    # 400 error code for InputError
    assert resp.status_code == 400

def test_invalid_token(clear_and_register_create_channel):
   
    resp_register1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        })    
    token1 = resp_register1.json()['token']

    resp_channel_id = requests.post(config.url + '/channels/create/v2', json = {
        'token':token1,
        'name': 'channel1', 
        'is_public': True,
        })    
    channel_id = resp_channel_id.json()['channel_id']
    resp_details = requests.get(config.url + '/channel/details/v2', params = {
        'token': 'not in the channel',
        'channel_id': channel_id,
        })

    # raise an AccessError since the the authorised user is not a member of the channel
    # 403 error code for InputError
    assert resp_details.status_code == 403

def test_auth_user_not_in_channel(clear_and_register_create_channel):
   
    resp_register1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        })    
    token1 = resp_register1.json()['token']

    resp_register2 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        })    
    token2 = resp_register2.json()['token']

    resp_channel_id = requests.post(config.url + '/channels/create/v2', json = {
        'token':token1,
        'name': 'channel1', 
        'is_public': True,
        })    
    channel_id = resp_channel_id.json()['channel_id']
    resp_details = requests.get(config.url + '/channel/details/v2', params = {
        'token': token2,
        'channel_id': channel_id,
        })

    # raise an AccessError since the the authorised user is not a member of the channel
    # 403 error code for InputError
    assert resp_details.status_code == 403
    