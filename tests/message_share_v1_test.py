import pytest
import requests
import json
from src import config
from src.token_funcs import decode_token

@pytest.fixture()
def clear_and_register_create_channel():
    '''
    Clear and create user for temporary database
    '''
    #Clear
    requests.delete(config.url + '/clear/v1')
    
    #Register User 1
    resp = requests.post(config.url + '/auth/register/v2', json={
        "email": "first.person@email.com",
        "password": "password",
        "name_first": "Biggie",
        "name_last": "Smalls"
        })
    token = resp.json()['token']
    
    #Logout User 1
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        })
    
    #Resgiter User 2
    resp = requests.post(config.url + '/auth/register/v2', json={
            'email': 'second.person@email.com',
            'password': 'password',
            'name_first': 'Homer',
            'name_last': 'Simpson'
        })
    token = resp.json()['token']    
        
    #Logout User 2
    resp = requests.post(config.url + '/auth/logout/v1', json = {
        'token':token
        }) 
    
def test_messages_share_channel(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']
    
    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })   
    resp_channel_id2 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel2",
        "is_public": True
            }) 
    channel_id1 = resp_channel_id1.json()['channel_id']
    channel_id2 = resp_channel_id2.json()['channel_id']
    
    # initially, channel1 has no messages
    # now, send channel1 with message "Hello World"
    requests.post(config.url + 'message/send/v1', json = {
        'token': token,
        'channel_id': channel_id1,
        'message': "Hello World"
        })

    # after first send, message "Hello World" is in channel1
    resp_channel1_messages1 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id1,
        "start": 0
            })
    
    assert resp_channel1_messages1.status_code == 200
    assert len(resp_channel1_messages1.json()['messages']) == 1
    assert resp_channel1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_channel1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": token, 
        "og_message_id": resp_channel1_messages1.json()['messages'][0]['message_id'], 
        "message": "", 
        "channel_id": channel_id2, 
        "dm_id": -1,
    })
    assert resp_messages_share1.status_code == 200
    # once shared, the message "Hello World" is in channel2
    resp_channel2_messages_shared1 = requests.get(config.url + 'channel/messages/v2', params = {
    "token": token,
    "channel_id": channel_id2,
    "start": 0
        })
    
    assert resp_channel2_messages_shared1.status_code == 200
    assert type(resp_channel2_messages_shared1.json()['messages']) == list
    assert len(resp_channel2_messages_shared1.json()['messages']) == 1
    assert resp_channel2_messages_shared1.json()['messages'][0]['message_id'] == 2
    assert resp_channel2_messages_shared1.json()['messages'][0]['message'] == "Hello World"
    assert type(resp_channel2_messages_shared1.json()['start']) == int
    assert type(resp_channel2_messages_shared1.json()['end']) == int
    assert resp_channel2_messages_shared1.json()['end'] == -1
    
    # now, share the message with additional messages
    resp_messages_share2 = requests.post(config.url + 'message/share/v1', json = {
        "token": token, 
        "og_message_id": resp_channel1_messages1.json()['messages'][0]['message_id'], 
        "message": "Jing Huang", 
        "channel_id": channel_id2, 
        "dm_id": -1,
    })
    assert resp_messages_share2.status_code == 200
    # once shared, the message "Hello World" is in channel2
    resp_channel2_messages_shared2 = requests.get(config.url + 'channel/messages/v2', params = {
    "token": token,
    "channel_id": channel_id2,
    "start": 0
        })
    
    assert resp_channel2_messages_shared2.status_code == 200
    assert type(resp_channel2_messages_shared2.json()['messages']) == list
    assert len(resp_channel2_messages_shared2.json()['messages']) == 2
    assert resp_channel2_messages_shared2.json()['messages'][1]['message_id'] == 2
    assert resp_channel2_messages_shared2.json()['messages'][0]['message'] == "Hello World Jing Huang"
    assert type(resp_channel2_messages_shared2.json()['start']) == int
    assert type(resp_channel2_messages_shared2.json()['end']) == int
    assert resp_channel2_messages_shared2.json()['end'] == -1

def test_messages_share_dm(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']

    resp_regitesr2 = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token2 = resp_regitesr2.json()['token']
    
    u_id1 = decode_token(token)['u_id']
    u_id2 = decode_token(token2)['u_id']
    resp_dm_id1 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [u_id2]
        })
    assert resp_dm_id1.status_code == 200

    resp_dm_id2 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token2,
        'u_ids': [u_id1]
        })
    assert resp_dm_id2.status_code == 200
    dm_id1 = resp_dm_id1.json()['dm_id']
    dm_id2 = resp_dm_id2.json()['dm_id']
    # initially, dm1 has no messages
    # now, send dm1 with message "Hello World"
    requests.post(config.url + '/message/senddm/v1', json = {
        'token': token,
        'dm_id': dm_id1,
        'message': "Hello World",
        })

    # after first send, message "Hello World" is in dm1
    resp_dm1_messages1 = requests.get(config.url + '/dm/messages/v1', params = {
        "token": token,
        "dm_id": dm_id1,
        "start": 0,
            })
    
    assert resp_dm1_messages1.status_code == 200
    assert len(resp_dm1_messages1.json()['messages']) == 1
    assert resp_dm1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_dm1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": token, 
        "og_message_id": resp_dm1_messages1.json()['messages'][0]['message_id'], 
        "message": "", 
        "channel_id": -1, 
        "dm_id": dm_id2,
    })
    assert resp_messages_share1.status_code == 200
    # once shared, the message "Hello World" is in channel2
    resp_dm2_messages_shared1 = requests.get(config.url + '/dm/messages/v1', params = {
    "token": token,
    "dm_id": dm_id2,
    "start": 0
        })
    
    assert resp_dm2_messages_shared1.status_code == 200
    assert type(resp_dm2_messages_shared1.json()['messages']) == list
    assert len(resp_dm2_messages_shared1.json()['messages']) == 1
    assert resp_dm2_messages_shared1.json()['messages'][0]['message'] == "Hello World"
    assert type(resp_dm2_messages_shared1.json()['start']) == int
    assert type(resp_dm2_messages_shared1.json()['end']) == int
    assert resp_dm2_messages_shared1.json()['end'] == -1
    
    # now, share the message with additional messages
    resp_messages_share2 = requests.post(config.url + 'message/share/v1', json = {
        "token": token, 
        "og_message_id": resp_dm1_messages1.json()['messages'][0]['message_id'], 
        "message": "Jing Huang", 
        "channel_id": -1, 
        "dm_id": dm_id2,
    })
    assert resp_messages_share2.status_code == 200
    # once shared, the message "Hello World" is in channel2
    resp_dm2_messages_shared2 = requests.get(config.url + '/dm/messages/v1', params = {
    "token": token,
    "dm_id": dm_id2,
    "start": 0
        })
    
    assert resp_dm2_messages_shared2.status_code == 200
    assert type(resp_dm2_messages_shared2.json()['messages']) == list
    assert len(resp_dm2_messages_shared2.json()['messages']) == 2
    assert resp_dm2_messages_shared2.json()['messages'][1]['message_id'] == 2
    assert resp_dm2_messages_shared2.json()['messages'][0]['message'] == "Hello World Jing Huang"
    assert type(resp_dm2_messages_shared2.json()['start']) == int
    assert type(resp_dm2_messages_shared2.json()['end']) == int
    assert resp_dm2_messages_shared2.json()['end'] == -1

def test_messages_share_invalid_channel_id(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']
    
    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })   
    channel_id1 = resp_channel_id1.json()['channel_id']
    # the second channel is not created
    
    # initially, channel1 has no messages
    # now, send channel1 with message "Hello World"
    requests.post(config.url + 'message/send/v1', json = {
        'token': token,
        'channel_id': channel_id1,
        'message': "Hello World"
        })

    # after first send, message "Hello World" is in channel1
    resp_channel1_messages1 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id1,
        "start": 0
            })
    
    assert resp_channel1_messages1.status_code == 200
    assert len(resp_channel1_messages1.json()['messages']) == 1
    assert resp_channel1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_channel1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": token, 
        "og_message_id": resp_channel1_messages1.json()['messages'][0]['message_id'], 
        "message": "", 
        "channel_id": -100, 
        "dm_id": -1,
    })
    # raise an InputError since the channel_id is not valid
    # 400 error code for InputError
    assert resp_messages_share1.status_code == 400

def test_messages_share_invalid_dm_id(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']
    
    resp_dm_id1 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })
    assert resp_dm_id1.status_code == 200
    dm_id1 = resp_dm_id1.json()['dm_id']

    # initially, dm1 has no messages
    # now, send dm1 with message "Hello World"
    requests.post(config.url + '/message/senddm/v1', json = {
        'token': token,
        'dm_id': dm_id1,
        'message': "Hello World",
        })

    # after first send, message "Hello World" is in dm1
    resp_dm1_messages1 = requests.get(config.url + '/dm/messages/v1', params = {
        "token": token,
        "dm_id": dm_id1,
        "start": 0,
            })
    
    assert resp_dm1_messages1.status_code == 200
    assert len(resp_dm1_messages1.json()['messages']) == 1
    assert resp_dm1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_dm1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": token, 
        "og_message_id": resp_dm1_messages1.json()['messages'][0]['message_id'], 
        "message": "", 
        "channel_id": -1, 
        "dm_id": -100,
    })
    assert resp_messages_share1.status_code == 400

def test_messages_share_none_negative(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']
    
    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })   
    channel_id1 = resp_channel_id1.json()['channel_id']

    resp_dm_id1 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })
    assert resp_dm_id1.status_code == 200
    dm_id1 = resp_dm_id1.json()['dm_id']

    # initially, channel1 has no messages
    # now, send channel1 with message "Hello World"
    requests.post(config.url + 'message/send/v1', json = {
        'token': token,
        'channel_id': channel_id1,
        'message': "Hello World"
        })

    # after first send, message "Hello World" is in channel1
    resp_channel1_messages1 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id1,
        "start": 0
            })
    
    assert resp_channel1_messages1.status_code == 200
    assert len(resp_channel1_messages1.json()['messages']) == 1
    assert resp_channel1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_channel1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": token, 
        "og_message_id": resp_channel1_messages1.json()['messages'][0]['message_id'], 
        "message": "", 
        "channel_id": channel_id1, 
        "dm_id": dm_id1,
    })
    # raise an InputError since neither channel_id nor dm_id are -1
    # 400 error code for InputError
    assert resp_messages_share1.status_code == 400

def test_messages_share_invalid_message_id(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']
    
    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })   
    channel_id1 = resp_channel_id1.json()['channel_id']

    # initially, channel1 has no messages
    # now, send channel1 with message "Hello World"
    requests.post(config.url + 'message/send/v1', json = {
        'token': token,
        'channel_id': channel_id1,
        'message': "Hello World"
        })

    # after first send, message "Hello World" is in channel1
    resp_channel1_messages1 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id1,
        "start": 0
            })
    
    assert resp_channel1_messages1.status_code == 200
    assert len(resp_channel1_messages1.json()['messages']) == 1
    assert resp_channel1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_channel1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": token, 
        "og_message_id": -100, 
        "message": "", 
        "channel_id": channel_id1, 
        "dm_id": -1,
    })
    # raise an InputError since the message_id is invalid
    # 400 error code for InputError
    assert resp_messages_share1.status_code == 400

def test_messages_share_message_too_long(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']
    
    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })   
    channel_id1 = resp_channel_id1.json()['channel_id']

    # initially, channel1 has no messages
    # now, send channel1 with message "Hello World"
    requests.post(config.url + 'message/send/v1', json = {
        'token': token,
        'channel_id': channel_id1,
        'message': "Hello World"
        })

    # after first send, message "Hello World" is in channel1
    resp_channel1_messages1 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id1,
        "start": 0
            })
    
    assert resp_channel1_messages1.status_code == 200
    assert len(resp_channel1_messages1.json()['messages']) == 1
    assert resp_channel1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_channel1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": token, 
        "og_message_id": resp_channel1_messages1.json()['messages'][0]['message_id'], 
        "message": "Jing" * 1000, 
        "channel_id": channel_id1, 
        "dm_id": -1,
    })
    # raise an InputError since the message is more than 100 characters
    # 400 error code for InputError
    assert resp_messages_share1.status_code == 400

def test_messages_share_message_auth_not_inchannel(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']

    resp_regitesr2 = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token2 = resp_regitesr2.json()['token']
    
    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })   
    channel_id1 = resp_channel_id1.json()['channel_id']

    # initially, channel1 has no messages
    # now, send channel1 with message "Hello World"
    requests.post(config.url + 'message/send/v1', json = {
        'token': token,
        'channel_id': channel_id1,
        'message': "Hello World"
        })

    # after first send, message "Hello World" is in channel1
    resp_channel1_messages1 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id1,
        "start": 0
            })
    
    assert resp_channel1_messages1.status_code == 200
    assert len(resp_channel1_messages1.json()['messages']) == 1
    assert resp_channel1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_channel1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": token2, 
        "og_message_id": resp_channel1_messages1.json()['messages'][0]['message_id'], 
        "message": "Jing", 
        "channel_id": channel_id1, 
        "dm_id": -1,
    })
    # raise an AccessError since the auth_user is not in the channel
    # 403 error code for AccessError
    assert resp_messages_share1.status_code == 403

def test_messages_share_message_auth_not_indm(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']

    resp_regitesr2 = requests.post(config.url + 'auth/login/v2', json={
        "email": "second.person@email.com",
        "password": "password"
    })
    
    token2 = resp_regitesr2.json()['token']
    resp_dm_id1 = requests.post(config.url + '/dm/create/v1', json = {
        'token':token,
        'u_ids': [1]
        })
    assert resp_dm_id1.status_code == 200
    dm_id1 = resp_dm_id1.json()['dm_id']
    

    # initially, dm1 has no messages
    # now, send dm1 with message "Hello World"
    requests.post(config.url + '/message/senddm/v1', json = {
        'token': token,
        'dm_id': dm_id1,
        'message': "Hello World",
        })

    # after first send, message "Hello World" is in dm1
    resp_dm1_messages1 = requests.get(config.url + '/dm/messages/v1', params = {
        "token": token,
        "dm_id": dm_id1,
        "start": 0,
            })
    
    assert resp_dm1_messages1.status_code == 200
    assert len(resp_dm1_messages1.json()['messages']) == 1
    assert resp_dm1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_dm1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": token2, 
        "og_message_id": resp_dm1_messages1.json()['messages'][0]['message_id'], 
        "message": "", 
        "channel_id": -1, 
        "dm_id": dm_id1,
    })
    assert resp_messages_share1.status_code == 403

def test_messages_share_message_invalid_token(clear_and_register_create_channel):

    resp_regitesr1 = requests.post(config.url + 'auth/login/v2', json={
        "email": "first.person@email.com",
        "password": "password"
    })
    
    token = resp_regitesr1.json()['token']

    
    
    resp_channel_id1 = requests.post(config.url + 'channels/create/v2', json = {
        "token": token,
        "name": "channel1",
        "is_public": True
            })   
    channel_id1 = resp_channel_id1.json()['channel_id']

    # initially, channel1 has no messages
    # now, send channel1 with message "Hello World"
    requests.post(config.url + 'message/send/v1', json = {
        'token': token,
        'channel_id': channel_id1,
        'message': "Hello World"
        })

    # after first send, message "Hello World" is in channel1
    resp_channel1_messages1 = requests.get(config.url + 'channel/messages/v2', params = {
        "token": token,
        "channel_id": channel_id1,
        "start": 0
            })
    
    assert resp_channel1_messages1.status_code == 200
    assert len(resp_channel1_messages1.json()['messages']) == 1
    assert resp_channel1_messages1.json()['messages'][0]['message_id'] == 1
    assert resp_channel1_messages1.json()['messages'][0]['message'] == "Hello World"
    resp_messages_share1 = requests.post(config.url + 'message/share/v1', json = {
        "token": "invalid token", 
        "og_message_id": resp_channel1_messages1.json()['messages'][0]['message_id'], 
        "message": "Jing", 
        "channel_id": channel_id1, 
        "dm_id": -1,
    })
    # raise an AccessError since the auth_user is not in the channel
    # 403 error code for AccessError
    assert resp_messages_share1.status_code == 403

