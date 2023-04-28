'''
This module contains list, listall and channel_create
'''
from src.data_store import data_store
from src.error import InputError
from src.checks import check_user_exists, check_user_in_channel
from src.error import  AccessError
from src.token_funcs import gen_token, add_token, decode_token, check_valid_token
from datetime import datetime

def channels_list_v2(token):
    '''
    Provide a list of all channels (and their associated details)
    that the authorised user is part of

    Arguments:
    token (str) - Used to identify what channels the user is apart of

    Excpetions:
    AccessError - Occurs when the token is invalid

    Return Value:
    Returns channel_list([dict]) on condition that auth_user_id is valid
    '''
    #Check if token is in the daabased
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
    
    
    #load in the current database
    store = data_store.get()
    
    #decode_token to find the corresponding user (owner)
    auth_id = decode_token(token)['u_id']

    #Create a blank channel list
    channel_list = []

    #Looping through the database
    for channel in store['channels']:
        # If the user belongs to that channel
        if check_user_in_channel(auth_id ,channel["channel_id"]):
            # copy and paste the channel details into channel_list
            channel_list.append({
                "channel_id": channel['channel_id'],
                "name": channel['name'],
                })

    return {'channels': channel_list}


def channels_listall_v2(token):
    '''
    Provide a list of all channels, including private channels,
    (and their associated details)

    Arguments:
    token (str) - Used to identify what channels the user is apart of

    Exceptions:
    AccessError - Occurs when the auth_user_id is invalid

    Return Value:
    Returns all_list([dict]) on condition that auth_user_id is valid
    '''
    #Check if token is in the daabased
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
    
    
    #load in the current database
    store = data_store.get()
    
    #Create a blank list
    all_list = []

    #Show all the channels in the database
    for channel in store['channels']:
        all_list.append({
            "channel_id": channel['channel_id'],
            "name": channel['name'],
            })

    return {'channels': all_list}


def channels_create_v2(token, name, is_public):
    '''
    Creates a new channel with the given name that is either a public or private channel.
    The user who created it automatically joins the channel.
    For this iteration, the only channel owner is the user who created the channel.

    Arguments:
    auth_user_id(<int>) - Used to identify what channels the user is apart of
    name(<string>) - Is the name of the channel
    is_public(<Booblean>) - Is the privacy type, True if it is open to public
    False if it is a private channel

    Excpetions:
    AccessError - Occurs when the auth_user_id is invalid
    InputError - Occurs when the channel name is greater than 20 characters or
    less than one character

    Return Value:
    Returns channel_id(<int>) on condition that auth_user_id is valid and the
    channel name is valid
    '''
    store = data_store.get()
    channels = store["channels"]

    if check_valid_token(token) == False:
        raise AccessError(description = "invalid token")

    #Checking for and raising input error if the name character requirement is not met
    if len(name) > 20 or len(name) < 1:
        raise InputError(description ="The length of the name is not between 1 and 20 characters")

    auth_user_id = decode_token(token)["u_id"]
    #If the character len is fulfilled
    #then a unique channel id is created by adding 1 to the total number of existing channels

    time_changed = int(datetime.now().timestamp())
    
    channel_id = len(channels) + 1
    store["channels"].append({
        "channel_id": channel_id,
        "name": name,
        "is_public": is_public,
        "owner_members": [auth_user_id],
        "all_members": [{
            "u_id": auth_user_id,
            "channel_permission_id": 1
        }],
        "messages": [],
        "standup": {
            "status": False,
            "message_buffer": [],
            "time_finish": None,
        },
    })
    
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            user['no_ch'] += 1
            user['ch_join'].append(user['no_ch'])
            user['chs_time'].append(time_changed)
            
    store['channels_change'].append(time_changed)
    store['total_no_chs'] += 1
    store['no_channels'].append(store['total_no_chs'])

    #setting the values to the data store
    data_store.set(store)

    return {
        'channel_id': channel_id,
    }
