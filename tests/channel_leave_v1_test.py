import pytest
import requests
import json
from src import config
# from src.data_store import data_store
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

def test_channel_leave(clear_and_register_create_channel):
    # test for the functionality of dm_leave
    # if the member leaves the dm
    
    resp_register1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        }) 
    # get token
    token1 = resp_register1.json()['token']

    resp_register3 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'c@abc.com',
        'password': '123456'
        })    
    token3 = resp_register3.json()['token']
    u_id3 = decode_token(token3)['u_id']

    resp_register4 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'd@abc.com',
        'password': '123456'
        })    
    token4 = resp_register4.json()['token']
    u_id4 = decode_token(token4)['u_id']

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
    assert resp_channel_id3.status_code == 200
    resp_channel_id4 = requests.post(config.url + '/channels/create/v2', json = {
        'token':token4,
        'name': 'channel4', 
        'is_public': True,
        })    
    assert resp_channel_id4.status_code == 200
    # get channel_id
    channel_id = resp_channel_id.json()['channel_id']
    
    resp_invite3 = requests.post(config.url + '/channel/invite/v2', json = {
        'token':token1,
        'channel_id': channel_id, 
        'u_id': u_id3,
        })        
    
    resp_invite4 = requests.post(config.url + '/channel/invite/v2', json = {
        'token':token1,
        'channel_id': channel_id, 
        'u_id': u_id4,
        })        

    resp_leave = requests.post(config.url + '/channel/leave/v1', json = {
        'token':token1,
        'channel_id': channel_id, 
        })

    
    
    assert resp_leave.status_code == 200
    assert resp_invite3.status_code == 200
    assert resp_invite4.status_code == 200
    resp_details = requests.get(config.url + '/channel/details/v2', params = {
        'token':token1,
        'channel_id': channel_id,
        })
    # raise an AcccessError since the authorised user is not in the dm
    # 403 error code for AccessError
    assert resp_details.status_code == 403
    

def test_invalid_channel_id(clear_and_register_create_channel):
    
    
    resp_register1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        }) 
    # get token
    token1 = resp_register1.json()['token']
    
    
    resp_leave = requests.post(config.url + '/channel/leave/v1', json = {
        'token':token1,
        'channel_id': 100,
        })
    
    # raise an InputError since the channel_id is not valid
    # 400 error code for InputError
    assert resp_leave.status_code == 400

def test_auth_user_not_in_channel(clear_and_register_create_channel):

    resp_register1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        }) 
    # get token
    token1 = resp_register1.json()['token']

    resp_register2 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'b@abc.com',
        'password': '123456'
        }) 
    # get token
    token2 = resp_register2.json()['token']
    
    resp_channel_id = requests.post(config.url + '/channels/create/v2', json = {
        'token':token1,
        'name': 'channel1',
        'is_public': True, 
        })
    # get channel_id
    channel_id = resp_channel_id.json()['channel_id']
    
    resp_leave = requests.post(config.url + '/channel/leave/v1', json = {
        'token':token2,
        'channel_id': channel_id,
        })
    
    # raise an AccessError since the token is not valid
    # 403 error code for AccessError
    assert resp_leave.status_code == 403
    

def test_invalid_token(clear_and_register_create_channel):

    resp_register1 = requests.post(config.url + '/auth/login/v2', json = {
        'email': 'a@abc.com',
        'password': '123456'
        }) 
    # get token
    token1 = resp_register1.json()['token']
    
    resp_channel_id = requests.post(config.url + '/channels/create/v2', json = {
        'token':token1,
        'name': 'channel1',
        'is_public': True, 
        })
    # get channel_id
    channel_id = resp_channel_id.json()['channel_id']
    
    resp_leave = requests.post(config.url + '/channel/leave/v1', json = {
        'token': 'not in channel',
        'channel_id': channel_id,
        })
    
    # raise an AccessError since the token is not valid
    # 403 error code for AccessError
    assert resp_leave.status_code == 403


'''
    store = data_store.get()
    channels = store['DMs']
    found_user = False
    for channel in channels:
        if channel['channel_id'] == channel_id:
            for member in channel['members']:
                if member['u_id'] == u_id:
                    found_user = True
    
    assert found_user == False  # auth_user has been left
    '''