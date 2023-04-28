'''
Author: Shagun

'''
import re
from src.checks import  check_user_exists, check_user_in_channel, check_channel, channel_is_public, user_is_stream_owner, user_is_channel_owner
from src.data_store import data_store
from src.error import InputError, AccessError
from src.token_funcs import gen_token, add_token, decode_token, check_valid_token
from src.dm import dm_create_v1, dm_leave_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_messages_v1

def admin_user_remove_v1(token, u_id):
    '''
    Given a user by their u_id, remove them from the Streams. 
    This means they should be removed from all channels/DMs, and will not be included in the list of users returned by users/all. 
    Streams owners can remove other Streams owners (including the original first owner). 
    Once users are removed, the contents of the messages they sent will be replaced by 'Removed user'. 
    Their profile must still be retrievable with user/profile, however name_first should be 'Removed' and name_last should be 'user'. 
    The user's email and handle should be reusable.

    Arguments:
    token - Used to identify the authorised user making the request
    u_id(<int>) - Used to identify which user will be removed
    
    Excpetions:
    AccessError - the authorised user is not a global owner
    InputError - u_id does not refer to a valid user, u_id refers to a user who is the only global owner

    Return Value:
    Returns {}
    '''
    store = data_store.get()
    channels = store["channels"]
    users = store["users"]

    if not check_valid_token(token):
        raise AccessError(description="Token invalid")

    if check_user_exists(u_id) == False:
        raise InputError(description = "u_id does not refer to a valid user")

    global_owners = [user["u_id"] for user in users if user["permission_id"] == 1]
    
    auth_user_id = decode_token(token)["u_id"]
    
    if user_is_stream_owner(auth_user_id) == False:
        raise AccessError(description = "the authorised user is not a global owner")

    if user_is_stream_owner(u_id) == True and len(global_owners) == 1:
        raise InputError(description = "u_id refers to a user who is the only global owner")

    for index in range(len(channels)):
        channel = channels[index]
        messages = channel["messages"]

        if u_id in channel["owner_members"]:
            channel["owner_members"].remove(u_id)

        for user in channel["all_members"]:
            if user["u_id"] == u_id:
                channel["all_members"].remove(user)
        
        for msg in messages:
            if msg["u_id"] == u_id:
                msg["message"] = "Removed user"

    data_store.set(store)

    store = data_store.get()
    dms = store["DMs"]

    token = gen_token(u_id)

    # using dm to remove them from dms
    for dm in dms:
        for user in dm['members']:
            if u_id == user['u_id']:
                dm_leave_v1(token,dm["dm_id"])

    store = data_store.get() 

    store["tokens"].remove(token)
    
    # changing the name of the user to Removed user and removing handle and email for reuse

    users = store["users"]
    for user in users:
        if user['u_id'] == u_id:
            user["name_first"] = "Removed"
            user["name_last"] = "user"
            user["email"] = ""
            user["handle"] = ""            


 
    data_store.set(store)      
    
    return {}

def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    Given a user by their user ID, set their permissions to new permissions described by permission_id.

    Arguments:
    token - Used to identify the authorised user making the request
    u_id(<int>) - Used to identify which user will be removed
    permission_id(<int>) - Used to identify the permission a user has. 1 is global owner and 2 is global member
    
    Excpetions:
    AccessError - the authorised user is not a global owner
    InputError - u_id does not refer to a valid user
    InputError - u_id refers to a user who is the only global owner and they are being demoted to a user
    InputError - permission_id is invalid

    Return Value:
    Returns {}
    '''
    store = data_store.get()
    users = store["users"]

    if not check_valid_token(token):
        raise AccessError(description="Token invalid")

    if permission_id !=1 and permission_id != 2:
        raise InputError(description = "Permission id is invalid")
        
    if check_user_exists(u_id) == False:
        raise InputError(description = "u_id does not refer to a valid user")

    auth_user_id = decode_token(token)["u_id"]

    if user_is_stream_owner(auth_user_id) == False:
        raise AccessError(description = "the authorised user is not a global owner")

    global_owners = [user["u_id"] for user in users if user["permission_id"] == 1]
    
    if user_is_stream_owner(u_id) == True and len(global_owners) == 1 and permission_id != 1:
        raise InputError(description = "u_id refers to a user who is the only global owner and they are being demoted to user")
    
    for user in users:
        if user["u_id"] == u_id:
           user["permission_id"] = permission_id
        
    data_store.set(store)

    return {}
        

