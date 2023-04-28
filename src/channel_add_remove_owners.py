'''
Author: Shagun
'''
from src.error import InputError, AccessError
from src.data_store import data_store
from src.checks import check_user_exists, check_user_in_channel, check_channel, channel_is_public, user_is_stream_owner, user_is_channel_owner
from src.token_funcs import decode_token, check_valid_token

def channel_addowner_v1(token,channel_id,u_id):

    store = data_store.get()
    channels = store["channels"]
    
    #Check if token is in the database
    if not check_valid_token(token):
        raise AccessError('Invalid Token')  

    auth_user_id = decode_token(token)["u_id"]

    if check_channel(channel_id) == True and user_is_channel_owner(auth_user_id,channel_id) == False:
        raise AccessError(description = "channel_id is valid but the auth user doesn't have owner permissions in the channel")

    if check_channel(channel_id) == False:
        raise InputError("Channel_id does not refer to a valid channel")
    
    if check_user_exists(u_id) == False:
        raise InputError("u_id does not refer to a valid user")

    if check_user_in_channel(u_id,channel_id) == False:
        raise InputError("u_id refers to a user who is not a member of the channel")

    if user_is_channel_owner(u_id,channel_id) == True:
        raise InputError("u_id refers to a user who is already an owner of the channel")

    for channel in channels:
        if channel['channel_id'] == channel_id:
            channel["owner_members"].append(u_id)

    data_store.set(store)
    
    return {}
    
    
def channel_removeowner_v1(token,channel_id,u_id):

    store = data_store.get()
    channels = store["channels"]
    
    if check_valid_token(token) == False:
        raise AccessError(description = "The Token is invalid")    

    auth_user_id = decode_token(token)["u_id"]

    if check_channel(channel_id) == True and user_is_channel_owner(auth_user_id,channel_id) == False:
        raise AccessError(description = "channel_id is valid but the auth user doesn't have owner permissions in the channel")
        
    if check_channel(channel_id) == False:
        raise InputError(description = "Channel_id does not refer to a valid channel")

    if check_user_exists(u_id) == False:
        raise InputError(description = "u_id does not refer to a valid user")

    if user_is_channel_owner(u_id,channel_id) == False:
        raise InputError(description = "u_id refers to a user who is not an owner of the channel")
    
    for channel in channels:
        if channel['channel_id'] == channel_id:
            ch = channel

    if user_is_channel_owner(u_id, channel_id) == True and len(ch["owner_members"]) == 1:
        raise InputError(description = "u id refers to a user who is currently the only owner of the channel")

    ch["owner_members"].remove(u_id)

    data_store.set(store)

    return {}




    