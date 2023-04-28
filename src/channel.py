'''
This module contains invite, join, details and messages
'''
from src.error import InputError, AccessError
from src.data_store import data_store
from src.checks import check_user_exists, check_user_in_channel, check_channel, channel_is_public, user_is_stream_owner, user_is_channel_owner
from src.token_funcs import decode_token, check_valid_token
from datetime import datetime

def channel_invite_v2(token, channel_id, u_id):
    '''
    Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately.
    In both public and private channels, all members are able to invite users.

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member of the channel
    channel_id(<int>) - A unique integer assigned to a channel, which is
    represents the channel the user is being invited to
    u_id(<int>) - A unique integer assigned to a user, this is called to
    invite that user into the channel, adding them to the data_store.

    Exceptions:
    AccessError - Occurs when token is not in steams
    InputError - Occurs when an invalid channel_id is passed into the function
    AccessError - Occurs when the authorised user is not in the channel
    InputError - Occurs when an invalid user id is passed into the function
    InputError - Occurs when the invited user is already in the channel

    Return Value:
    No Return Values
    '''
    
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')    
    auth_user_id = decode_token(token)['u_id']
    store = data_store.get()
    #check if channel_id is valid
    if not check_channel(channel_id):
        raise InputError(description ="Not a valid channel_id")

    '''
    coverage fixed
    # check if auth_user is valid
    if not check_user_exists(auth_user_id):
        raise AccessError("Not a valid auth_user_id")
    '''

    # check if auth_user is in that channel
    if not check_user_in_channel(auth_user_id, channel_id):
        raise AccessError(description ="Authorised user is not a member of the channel")

    # check if user is valid
    if not check_user_exists(u_id):
        raise InputError(description ="Not a valid user_id")

    # check if the user is already in the channel
    if check_user_in_channel(u_id, channel_id):
        raise InputError(description ="User is already a member of the channel")

    # check if user is channel owner
    channel_permission_id = 1 if user_is_channel_owner(u_id, channel_id) else 2

    # create new user in channel[channel_id]
    for channel in store['channels']:
        # add one more channel
        if channel["channel_id"] == channel_id:
            name = channel["name"]
            # add the invited user into the channel
            channel["all_members"].append({
                "u_id": u_id,
                "channel_permission_id": channel_permission_id,
            })

    time_changed = int(datetime.now().timestamp())        
    for user in store['users']:
        if user['u_id'] == u_id:
            user['no_ch'] += 1
            user['ch_join'].append(user['no_ch'])
            user['chs_time'].append(time_changed)
            

    # add notifications
    users = store["users"]
    user_handle = users[auth_user_id-1]["handle_str"]
    users[u_id-1]["notifications"].append({
        "channel_id": channel_id,
        "dm_id": -1,
        "notification_message": f"{user_handle} added you to {name}"
    })

    data_store.set(store)
    return {}

# ------------------------------------------------------------------------------ #

def channel_details_v2(token, channel_id):
    '''
    Given a channel with ID channel_id that the authorised user is a member of,
    provide basic details about the channel.

    Invites a user with ID u_id to join a channel with ID channel_id.
    Once invited, the user is added to the channel immediately.
    In both public and private channels, all members are able to invite users.

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member of the channel
    channel_id(<int>) - A unique integer assigned to a channel, which is
    represents the channel the user is being invited to

    Exceptions:
    AccessError - Occurs when token is not in Streams
    InputError - Occurs when an invalid channel_id is passed into the function
    AccessError - Occurs when the authorised user is not in the channel

    Return Value:
    Returns 'name'(<string>) on condition that user and channel are valid
    Returns 'is_public'(<Boolen>) on condition that user and channel are valid
    Returns 'owners'([<int>]) on condition that user and channel are valid
    Returns 'all_members'([<int>]) on condition that user and channel are valid
    '''
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')    
    
    auth_user_id = decode_token(token)['u_id']
    
    store = data_store.get()
    #check if channel_id is valid
    if not check_channel(channel_id):
        raise InputError(description ="Not a valid channel_id")

    # check if auth_user is in that channel
    if not check_user_in_channel(auth_user_id, channel_id):
        raise AccessError(description ="Authorised user is not a member of the channel")

    owners = []
    members = []
    channels = store['channels']
    
    for ch in channels:
        # add one more channel
        if ch['channel_id'] == channel_id:
            name = ch['name']
            is_public = ch['is_public']
            owners = [owner for owner in ch["owner_members"]]
            members = [member["u_id"] for member in ch["all_members"]]            

    owner_members = []
    channel_members = []


    for user in store["users"]:
        if user["u_id"] in members:
            channel_members.append(user)
        if user["u_id"] in owners:
            owner_members.append(user)                


    return {
        'name': name,
        'is_public': is_public,
        'owner_members':owner_members,
        'all_members':channel_members,
    }


def channel_messages_v2(token, channel_id, start):
    """
    Given a channel with ID channel_id that the authorised user is a member of,
    return up to 50 messages between index "start" and "start + 50".
    Message with index 0 is the most recent message in the channel.
    This function returns a new index "end" which is the value of "start + 50",
    or, if this function has returned the least recent messages in the channel,
    returns -1 in "end" to indicate there are no more messages to load
    after this return.

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member of the channel
    channel_id(<int>) - A unique integer assigned to a channel, which is
    represents the channel the user is being invited to
    start(<int>) - This is a chosen integer referring to the first index
    position of a list of messages.

    Exceptions:
    AccessError - Occurs when an invalid auth user id is passed into the function
    InputError - Occurs when an invalid channel_id is passed into the function
    AccessError - Occurs when the authorised user is not in the channel
    InputError - Occurs when the inputed start index is greator than the amount
    of messages

    Return Value:
    Returns 'messages'<[string]> on condition that there are more messages in
    data_store than the value of start
    Returns 'end'<int> on condition that is is start+50 if there are more than
    50 messages in data_store that follow the starting index called
    Returns 'start'<int> on condition that it isn't greater than the amount
    of messages
    """
    store = data_store.get()
    
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
    
    auth_user_id = decode_token(token)['u_id']

    if not check_channel(channel_id):
        raise InputError(description ="Invalid channel id")

    if not check_user_in_channel(auth_user_id, channel_id):
        raise AccessError(description ="User is not a member of this channel")

    channels = store['channels']
    for ch in channels:
        if ch['channel_id'] == channel_id:
            channel = ch
    messages = channel['messages']

    if len(messages) <= start and start != 0:
        raise InputError(description ="Start cannot be greater than amount of messages")
        
    #we define variables end
    end = 0
    
    #extract the messages from start to start + 50
    messages.reverse()
    msg_from_start = messages[start:(start+50)]
    
    if len(msg_from_start) < 50:
        end = -1
    else:
        end = start + 50
    
    for msg in msg_from_start:
        if len(msg['reacts']) != 0 and auth_user_id in msg['reacts'][0]['u_ids']:
            msg['reacts'][0]['is_this_user_reacted'] = True

    return {
        'messages': msg_from_start,
        'start': start,
        'end': end,
    }   



def channel_join_v2(token, channel_id):
    """
    Given a channel_id of a channel that the authorised user can join, 
    adds them to that channel.
    
    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member of the channel
    channel_id(<int>) - A unique integer assigned to a channel, which is
    represents the channel the user is joining
    
    Exceptions:
    InputError - Occurs when an invalid channel_id is passed into the function
    InputError - Occurs when the authorised user is already in the channel
    AccessError - Occurs when an the user is invited to a private channel and
    they do not have global permissions
    AccessError - Occurs when the auth user id is invalid
    
    Return Value:
    No Return Values
    """

    
    if check_valid_token(token) == False:
        raise AccessError(description ='Invalid Token')
        
    store = data_store.get()
    #Make sure that we are receiving a valid channel_id, raise an error if invalid 
    if not check_channel(channel_id):
        raise InputError(description ="Not a valid channel_id")

    
    auth_user_id = decode_token(token)['u_id']
    #Make sure that the user is not a memeber of the channel already, raise an error if invalid
    #If the user is not already a member than we have to check if they can be, if it is public
    #If the channel is private, we only allow the user to join if they have global permission
    
    
    permission_global = False
    if user_is_stream_owner(auth_user_id):
            permission_global = True
            
    
    if check_user_in_channel(auth_user_id, channel_id):
        raise InputError(description ="The user is already a member of this channel")
    elif channel_is_public(channel_id) is False and permission_global == False:
        raise AccessError(description ="This is a private channel. User must be invited by a current member")
    
    # check if user is stream owner
    channel_permission_id = 1 if permission_global == True else 2
    
    #If channel and user are both valid then add them to the list of members for that channel
    for channel in store['channels']:
        if channel["channel_id"] == channel_id:
            # add the invited user into the channel
            channel["all_members"].append({
                "u_id": auth_user_id,
                "channel_permission_id": channel_permission_id
            })
            
            
    time_changed = int(datetime.now().timestamp())        
    u_id = decode_token(token)['u_id']
    for user in store['users']:
        if user['u_id'] == u_id:
            user['no_ch'] += 1
            user['ch_join'].append(user['no_ch'])
            user['chs_time'].append(time_changed)             
   
    data_store.set(store)
    
    return {}

def channel_leave_v1(token, channel_id):
    '''
    Given a channel with ID channel_id that the authorised user is a member of, 
    remove them as a member of the channel. 
    Their messages should remain in the channel. 
    If the only channel owner leaves, the channel will remain.

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member of the channel
    channel_id(<int>) - A unique integer assigned to a channel, which is
    represents the channel the user is removed from


    Exceptions:
    AccessError - Occurs when token is not in steams
    InputError - Occurs when an invalid channel_id is passed into the function
    AccessError - Occurs when the authorised user is not in the channel

    Return Value:
    No Return Values
    '''

    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token') 
    auth_user_id = decode_token(token)['u_id']
    store = data_store.get()
    #Make sure that we are receiving a valid channel_id, raise an error if invalid 
    if not check_channel(channel_id):
        raise InputError(description ="Not a valid channel_id")

    #Make sure that the user is not a memeber of the channel already, raise an error if invalid
    #If the user is not already a member than we have to check if they can be, if it is public
    #If the channel is private, we only allow the user to join if they have global permission
    
    #if auth_user_id is not an int and is less than 0 
    '''
    found_uid = check_user_exists(auth_user_id)
    coverage fixed
    if not found_uid:
        raise AccessError("The user id is invalid")
    '''
    
    if not check_user_in_channel(auth_user_id, channel_id):
        raise AccessError(description ="Authorised user is not a member of the channel")

    #If channel and user are both valid then add them to the list of members for that channel
    for channel in store['channels']:
        # add channels
        if channel["channel_id"] == channel_id:
            # remove user from the channel
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    channel["all_members"].remove(member)
            
            
    time_changed = int(datetime.now().timestamp())        
    u_id = decode_token(token)['u_id']
    for user in store['users']:
        if user['u_id'] == u_id:
            user['no_ch'] -= 1
            user['ch_join'].append(user['no_ch'])
            user['chs_time'].append(time_changed)       
    
    data_store.set(store)
    return {}
