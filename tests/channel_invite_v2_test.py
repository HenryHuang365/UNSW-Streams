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
    
def test_channel_invite_v2(clear_and_register_create_channel):
   
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
    u_id = decode_token(token2)['u_id']

    resp_register3 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'c@abc.com',
        'password': '123456'
        })    
    token3 = resp_register3.json()['token']

    resp_register4 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'd@abc.com',
        'password': '123456'
        })    
    token4 = resp_register4.json()['token']

    resp_channel_id = requests.post(config.url + '/channels/create/v2', json = {
        'token':token1,
        'name': 'channel1', 
        'is_public': True,
        })    

    resp_channel_id3 = requests.post(config.url + '/channels/create/v2', json = {
        'token':token3,
        'name': 'channel3', 
        'is_public': True,
        })    
    
    resp_channel_id4 = requests.post(config.url + '/channels/create/v2', json = {
        'token':token4,
        'name': 'channel4', 
        'is_public': True,
        })    

    channel_id = resp_channel_id.json()['channel_id']
    channel_id3 = resp_channel_id3.json()['channel_id']
    channel_id4 = resp_channel_id4.json()['channel_id']
    resp_invite = requests.post(config.url + '/channel/invite/v2', json = {
        'token':token1,
        'channel_id': channel_id, 
        'u_id': u_id,
        })        

    resp_invite3 = requests.post(config.url + '/channel/invite/v2', json = {
        'token':token3,
        'channel_id': channel_id3, 
        'u_id': u_id,
        })        
    
    resp_invite4 = requests.post(config.url + '/channel/invite/v2', json = {
        'token':token4,
        'channel_id': channel_id4, 
        'u_id': u_id,
        })        
    assert resp_invite.status_code == 200
    assert resp_invite3.status_code == 200
    assert resp_invite4.status_code == 200
    resp_details = requests.get(config.url + '/channel/details/v2', params = {
        'token':token1,
        'channel_id': channel_id, 
        })        
    members = []
    members = resp_details.json()['all_members']
    found_uid = False
    for member in members:
        if member['u_id'] == u_id:
            found_uid = True

    assert found_uid ==  True

def test_invalid_channel_id(clear_and_register_create_channel):
    
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
    u_id = decode_token(token2)['u_id']

    resp_invite = requests.post(config.url + '/channel/invite/v2', json = {
        'token':token1,
        'channel_id': -100, 
        'u_id': u_id,
        })        
    
    # raise an InputError since the channel_id is not valid
    # 400 error code for InputError
    assert resp_invite.status_code == 400

def test_invalid_u_id(clear_and_register_create_channel):
    
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

    resp_invite = requests.post(config.url + '/channel/invite/v2', json = {
        'token':token1,
        'channel_id': channel_id, 
        'u_id': -100,
        })        
    
    # raise an InputError since the u_id is not valid
    # 400 error code for InputError
    assert resp_invite.status_code == 400

def test_u_id_already_in_channel(clear_and_register_create_channel):
    
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

    resp_invite = requests.post(config.url + '/channel/invite/v2', json = {
        'token':token1,
        'channel_id': channel_id, 
        'u_id': u_id,
        })        
    
    # raise an InputError since the invited user is already in the channel
    # 400 error code for InputError
    assert resp_invite.status_code == 400

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
    u_id = decode_token(token2)['u_id']

    resp_channel_id = requests.post(config.url + '/channels/create/v2', json = {
        'token':token1,
        'name': 'channel1', 
        'is_public': True,
        })    
    channel_id = resp_channel_id.json()['channel_id']

    resp_invite = requests.post(config.url + '/channel/invite/v2', json = {
        'token':token2,
        'channel_id': channel_id, 
        'u_id': u_id,
        })        
    
    # raise an AccessError since the authorised user is not a member of the channel
    # 403 error code for AccessError
    assert resp_invite.status_code == 403

def test_invalid_token(clear_and_register_create_channel):
    
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
    u_id = decode_token(token2)['u_id']

    resp_channel_id = requests.post(config.url + '/channels/create/v2', json = {
        'token':token1,
        'name': 'channel1', 
        'is_public': True,
        })    
    channel_id = resp_channel_id.json()['channel_id']

    resp_invite = requests.post(config.url + '/channel/invite/v2', json = {
        'token':'not in channel',
        'channel_id': channel_id, 
        'u_id': u_id,
        })        
    
    # raise an AccessError since the authorised user is not a member of the channel
    # 403 error code for AccessError
    assert resp_invite.status_code == 403