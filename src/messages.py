#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 20:35:45 2021

@author: caspar
"""

"""
Message Functions
"""
import re
from src.error import InputError, AccessError
from src.data_store import data_store
from src.checks import check_user_in_channel, check_channel, user_is_stream_owner, user_is_channel_owner
from src.token_funcs import decode_token, check_valid_token
from datetime import datetime
import time
import threading

def message_send_v1(token, channel_id, message):
    """
    When this function is called, a message will be sent to the specified
    channel and stored. The contents of will be a message, a message id,
    the user who sent the message and the time the message was created.

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member of the channel
    channel_id(<int>) - A unique integer assigned to a channel, which is
    represents the channel the user is sending a message to
    message(<string>) - A string of characters from 1 to 1000 in length

    Exceptions:
    AccessError - Occurs when token is not in Streams
    InputError - Occurs when an invalid channel_id is passed into the function
    AccessError - Occurs when the authorised user is not in the channel
    InputError - Occurs when the message provided is above 1000 characters
    or is below 1 character.

    Return Value:
    Returns 'message_id'([<int>]) on condition that user, channel and message
    are valid
    """

    store = data_store.get()

    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
        
    auth_id = decode_token(token)['u_id']

    if check_channel(channel_id) == False:
        raise InputError(description ='Invalid Channel Id')

    if not check_user_in_channel(auth_id, channel_id):
        raise AccessError(description ='User is not in the channel called')

    if len(message) > 1000 or len(message) < 1:
        raise InputError(description ='Message cannot be less than 1 character or greater than 1000')

    store['m_id_create'] = store['m_id_create'] + 1

    message_id = store['m_id_create']
    
    sent_time = datetime.now()
    
    time_created = sent_time.timestamp()
    
    time_created = round(time_created)
    
    store['msg_change'].append(time_created)
    store['total_no_msg'] += 1
    store['no_msg'].append(store['total_no_msg'])
    
    
    store['channels'][channel_id-1]['ch_msg_time'] = time_created  
    for user in store['users']:
        if user['u_id'] == auth_id:
            user['msg_time'].append(time_created)
            user['no_msg'] += 1
            user['msg_sent'].append(user['no_msg'])
            
    store['channels'][channel_id-1]['messages'].append(
        {
            'message_id': message_id,
            'u_id': auth_id,
            'message': message,
            'time_created': time_created,
            'reacts': [],
            'is_pinned': False,
        }
      )
    
    data_store.set(store)
    tag_notification(auth_id, message, channel_id, -1)
    
    return {'message_id': message_id}

def message_senddm_v1(token, dm_id, message):
    """
    When this function is called, a message will be sent to the specified
    DM and stored. The contents of will be a message, a message id,
    the user who sent the message and the time the message was created.

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member of the DM
    dm_id(<int>) - A unique integer assigned to a dm, which is
    represents the dm the user is sending a message to
    message(<string>) - A string of characters from 1 to 1000 in length

    Exceptions:
    AccessError - Occurs when token is not in Streams
    InputError - Occurs when an invalid dm_id is passed into the function
    AccessError - Occurs when the authorised user is not in the dm
    InputError - Occurs when the message provided is above 1000 characters
    or is below 1 character.

    Return Value:
    Returns 'message_id'([<int>]) on condition that user, dm and message
    are valid
    """

    store = data_store.get()

    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
        
    auth_id = decode_token(token)['u_id']

    dm_exists = False
    
    for dms in store['DMs']:
        if dm_id == dms['dm_id']:
            dm_exists = True
        
    if dm_exists == False:
        raise InputError(description ='Invalid dm_id Id')

    dm_user = False
    
    for user in store['DMs'][dm_id-1]['members']:
        if user['u_id'] == auth_id:
            dm_user = True

    if dm_user == False:
        raise AccessError(description ='User not in DM')
        
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description ='Message cannot be less than 1 character or greater than 1000')

    store['m_id_create'] = store['m_id_create'] + 1

    message_id = store['m_id_create']

    sent_time = datetime.now()
    
    time_created = sent_time.timestamp()
    
    time_created = round(time_created)
    
    store['msg_change'].append(time_created)
    store['total_no_msg'] += 1
    store['no_msg'].append(store['total_no_msg'])
    
    for user in store['users']:
        if user['u_id'] == auth_id:
            user['msg_time'].append(time_created)
            user['no_msg'] += 1
            user['msg_sent'].append(user['no_msg'])
            
    store['DMs'][dm_id-1]['dm_message_time'] = time_created  

    store['DMs'][dm_id-1]['messages'].append({
            'message_id': message_id,
            'u_id': auth_id,
            'message': message,
            'time_created': time_created,
            'reacts': [],
            'is_pinned': False,
            }
      )
    
    data_store.set(store)
    tag_notification(auth_id, message, -1, dm_id)
    return {'message_id': message_id}

def message_edit_v1(token, message_id, message):
    """
    When this function is called, a specificed message will be edited using the
    new message provided which will replace the existing message that belongs
    to the message ID. If the message provided is blank it will compeletly
    remove the message.

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member
    message_id(<int>) - A unique integer assigned to a message, which is
    represents the message the user is editing
    message(<string>) - A string of characters from 1 to 1000 in length

    Exceptions:
    AccessError - Occurs when token is not in Streams
    InputError - Occurs when the message provided is above 1000 characters
    InputError - Occurs when an invalid message_id is passed
    AccessError - Occurs when the user attempting to edit a message that they
    do not have permission to edit.

    Return Value:
    No Return
    """

    store = data_store.get()

    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')

    auth_id = decode_token(token)['u_id']
    
    type_channel = False
    type_dm = False
    user_in_dm = False
    remove_message = False
    message_channel = -1
    message_dm = -1

    if len(message) > 1000:
        raise InputError(description ='Characters cannot be greater than 1000')

    if len(message) == 0:
        remove_message = True

    #Find the message in channels;
    for channels in store['channels']:
        for msg_ch in channels['messages']:
            if message_id == msg_ch['message_id']:
                message_channel = channels['channel_id']
                sent_id = msg_ch['u_id']
                message_index = channels['messages'].index(msg_ch)
                type_channel = True
                
    #Find the message in dms;        
    if type_channel == False:
        for dms in store['DMs']:
            for msg_dm in dms['messages']:
                if message_id == msg_dm['message_id']:
                    message_dm = dms['dm_id']
                    sent_id = msg_dm['u_id']
                    message_index = dms['messages'].index(msg_dm)
                    type_dm = True
    
    #message is not found in either channels and dms
    if type_channel == False and type_dm == False:
        raise InputError(description ='Invalid message ID')
    
    #Valid message in channel
    
    #If the user is not owner of the channel/stream 
    #and the message was not sent by the auth user
    if type_channel == True:
        if auth_id != sent_id and user_is_stream_owner(auth_id) == False \
        and user_is_channel_owner(auth_id, message_channel) == False:
            raise AccessError(description ='Invalid permission to remove message')
        
    #if the user is the sender but he is no longer a member in the channel    
        elif not check_user_in_channel(auth_id, message_channel):
            raise AccessError(description ='Invalid permission to remove message')
        
    #Valid message in dm
    
    #If the user is not owner of the dm
    #and the message was not sent by the auth user
    if type_dm == True:
        if auth_id != sent_id and auth_id != store['DMs'][message_dm-1]['owner']:
            raise AccessError(description ='Invalid permission to remove message')  
        
        else:
            for users in store['DMs'][message_dm-1]['members']:
                if auth_id == users['u_id']:
                    user_in_dm = True
            if user_in_dm == False:    
                raise AccessError(description ='Invalid permission to remove message')             

       
    if type_channel == True:
        for n in store['channels'][message_channel-1]['messages']:
            if message_id == n['message_id'] and remove_message == False:
                n['message'] = message
            elif message_id == n['message_id'] and remove_message == True:
                curr_time = datetime.now()   
                curr_timestamp = int(curr_time.timestamp())
                store['channels'][message_channel-1]['ch_msg_time'] = curr_timestamp 
                store['msg_change'].append(curr_timestamp)  
                store['total_no_msg'] -= 1
                store['no_msg'].append(store['total_no_msg'])              
                del store['channels'][message_channel-1]['messages'][message_index]

    if type_dm == True:
        for n in store['DMs'][message_dm-1]['messages']:
            if message_id == n['message_id'] and remove_message == False:
                n['message'] = message
            elif message_id == n['message_id'] and remove_message == True:
                curr_time = datetime.now()   
                curr_timestamp = int(curr_time.timestamp())
                store['DMs'][message_dm-1]['dm_message_time'] = curr_timestamp 
                store['total_no_msg'] -= 1
                store['no_msg'].append(store['total_no_msg'])
                del store['DMs'][message_dm-1]['messages'][message_index]
                

    data_store.set(store)
    tag_notification(auth_id, message, message_channel, message_dm)
    return {}

def message_remove_v1(token, message_id):
    """
    When this function is called, a specificed message will be removed from
    the channel or dm it is in.

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member
    message_id(<int>) - A unique integer assigned to a message, which is
    represents the message the user is removing

    Exceptions:
    AccessError - Occurs when token is not in Streams
    InputError - Occurs when an invalid message_id is passed
    AccessError - Occurs when the user attempting to remove a message that they
    do not have permission to remove.

    Return Value:
    No Return
    """

    store = data_store.get()

    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
        
    type_message = False
    type_dm = False
    user_in_dm = False

    auth_id = decode_token(token)['u_id']
    message_channel = 0
    
    for channels in store['channels']:
        for message in channels['messages']:
            if message_id == message['message_id']:
                message_channel = channels['channel_id']
                sent_id = message['u_id']
                type_message = True

    
    if type_message == False:
        for dms in store['DMs']:
            for message in dms['messages']:
                if message_id == message['message_id']:
                    message_dm = dms['dm_id']
                    sent_id = message['u_id']
                    type_dm = True

        
    if type_message == False and type_dm == False:
        raise InputError(description ='Invalid message ID')

    

    if type_message == True:
        if auth_id != sent_id and user_is_stream_owner(auth_id) == False \
        and user_is_channel_owner(auth_id, message_channel) == False:
            raise AccessError(description ='Invalid permission to remove message')
            
        if not check_user_in_channel(auth_id, message_channel):
            raise AccessError(description ='User is not in channel')
            
    if type_dm == True:
        if auth_id != sent_id and auth_id != store['DMs'][message_dm-1]['owner']:
            raise AccessError(description ='Invalid permission to remove message')  
            
        else:
            for users in store['DMs'][message_dm-1]['members']:
                if auth_id == users['u_id']:
                    user_in_dm = True
            if user_in_dm == False:    
                raise AccessError(description ='Invalid permission to remove message') 
                
    if type_message == True:
        for n in store['channels']:
            for msg in n['messages']:
                if message_id == msg['message_id']:
                    curr_time = datetime.now()   
                    curr_timestamp = int(curr_time.timestamp())
                    n['ch_msg_time'] = curr_timestamp 
                    msg_index = n['messages'].index(msg)
                    del n['messages'][msg_index]

    if type_dm == True:
        for d in store['DMs']:
            for msg in d['messages']:
                if message_id == msg['message_id']:
                    msg_index = d['messages'].index(msg)
                    curr_time = datetime.now()   
                    curr_timestamp = int(curr_time.timestamp())
                    d['dm_message_time'] = curr_timestamp 
                    del d['messages'][msg_index]
                    
    curr_time = datetime.now()   
    curr_timestamp = int(curr_time.timestamp())
    store['msg_change'].append(curr_timestamp)             
    store['total_no_msg'] -= 1
    store['no_msg'].append(store['total_no_msg'])
    data_store.set(store)
    
    return {}


def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    Send a message from the authorised user to the channel specified by channel_id 
    automatically at a specified time in the future.
    
    Arguments:
        token (str)    - The token of the corresponding user (who call this function)j
        channel_id (int) - id of the channel
        message(str) - message to be sent
        time_sent(int (timestamp)) - time to send the message
        
    Exceptions:
        AccessError - Occurs when token is invalid
        AccessError - channel_id is valid and the authorised user is not a member 
        of the channel they are trying to post to
        
        InputError- channel_id does not refer to a valid channel
        InputError- length of message is over 1000 characters
        InputError- time_sent is a time in the past
    
    Return Value:
        Returns {message_id} (int) on successful call
    '''    
    store = data_store.get()    
    #Check if token is in the daabased
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
    
    #Get the u_id of the user from token
    u_id = decode_token(token)['u_id']
    
    #Check if channel_id is valid and the user is also a member of the channel
    if check_channel(channel_id) == True and check_user_in_channel(u_id,channel_id) == False:
        raise AccessError(description ="The user is not in the channel")  
        
    #Chec if channel_id is valid
    if check_channel(channel_id) == False:
        raise InputError(description ="The channel_id is invalid")
        
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description ="message too long/ empty message")
     
    curr_time = datetime.now()        
    curr_timestamp = int(curr_time.timestamp())

    if curr_timestamp > time_sent:
        raise InputError(description ="time_sent is a time in the past")
    
    time_diff = time_sent - curr_timestamp

    store['m_id_create'] = store['m_id_create'] + 1
    store['time_changed'] = time_sent
    message_id = store['m_id_create']   

    data_store.set(store) 
    new_thread = threading.Thread(target = actual_send_ch , args = (u_id, channel_id, message, time_diff, message_id,))
    new_thread.start()
    
    return {'message_id': message_id}    

def actual_send_ch(u_id ,channel_id, message, time_diff, message_id):
    '''
    Send a message from the authorised user to the channel specified by channel_id 
    automatically at a specified time in the future.
    
    Arguments:
        u_id (int) - user id
        channel_id (int) - id of the channel
        message(str) - message to be sent
        time_diff(int (timestamp)) - amount of time the actual send waits
        message_id = id of the message
        
    Return Value:
        {}
    '''   
    store = data_store.get()
    
    time.sleep(time_diff)
    curr_time = datetime.now()   
    curr_timestamp = int(curr_time.timestamp())
    
    for user in store['users']:
        if user['u_id'] == u_id:
            user['msg_time'].append(curr_timestamp)
            user['no_msg'] += 1
            user['msg_sent'].append(user['no_msg'])
            
    store['channels'][channel_id-1]['ch_msg_time'] = curr_timestamp      
    store['msg_change'].append(curr_timestamp)    
    store['total_no_msg'] += 1
    store['no_msg'].append(store['total_no_msg'])
    
    store['channels'][channel_id-1]['messages'].append(
        {
            'message_id': message_id,
            'u_id': u_id,
            'message': message,
            'time_created': curr_timestamp,
            'reacts': [],
            'is_pinned': False,
        }
      )
        
    data_store.set(store)    
    tag_notification(u_id, message, channel_id, -1)        
    
    return {}


def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    Create a DM with name based on the members in the DM
    
    Arguments:
        token (str)    - The token of the corresponding user (who call this function)j
        dm_id (int) - id of the dm
        message(str) - message to be sent
        time_sent(int (timestamp)) - time to send the message
    
    Exceptions:
        AccessError - Occurs when token is invalid
        AccessError - dm_id is valid and the authorised user is not a member 
        of the dm they are trying to post to
        
        InputError- channel_id does not refer to a valid channel
        InputError- length of message is over 1000 characters
        InputError- time_sent is a time in the past
    
    Return Value:
        Returns {message_id} (int) on successful call
    '''    
    store = data_store.get()    
    #Check if token is in the daabased
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
    
    #Get the u_id of the user from token
    u_id = decode_token(token)['u_id']
    
    #Return Access error if dm_id is valid and 
    #the authorised user is not a member of the DM    
    DMs = store['DMs']
    
    found_DM = False
    member_list = []
    for dm in DMs:
        if dm['dm_id'] == dm_id:
            found_DM = True
            #Extract all the user_id in the dm            
            for user in dm['members']:
                member_list.append(user['u_id'])
            #if the authoriised user is not a member of the DM, return AccessError
            if not u_id in member_list:
                raise AccessError(description ="The authorised user is not a member of the DM")
    

    #Return InputError if dm_id is not found
    if found_DM == False:
        raise InputError(description ='dm_id does not refer to a valid DM')
        
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description ="message too long, keep it under 1000 characters")
    
    curr_time = datetime.now()        
    curr_timestamp = int(curr_time.timestamp())
    
    if curr_timestamp > time_sent:
        raise InputError(description ="time_sent is a time in the past")

    store['m_id_create'] = store['m_id_create'] + 1

    message_id = store['m_id_create']

    time_diff = time_sent - curr_timestamp
    
    new_thread = threading.Thread(target = actual_send_dm , args = (u_id, dm_id, message, time_diff, message_id,))
    new_thread.start()

    store['time_changed'] = time_sent
    data_store.set(store)
    return {'message_id': message_id}

def actual_send_dm(u_id , dm_id, message, time_diff, message_id):
    '''
    Send a message from the authorised user to the channel specified by channel_id 
    automatically at a specified time in the future.
    
    Arguments:
        u_id (int) - user id
        dm_id (int) - id of the dm
        message(str) - message to be sent
        time_diff(int (timestamp)) - amount of time the actual send waits
        message_id = id of the message
        
        
    Return Value:
        {}
    '''   
    store = data_store.get()
    
    time.sleep(time_diff)
    
    curr_time = datetime.now()   
    curr_timestamp = int(curr_time.timestamp())
    
    for user in store['users']:
        if user['u_id'] == u_id:
            user['msg_time'].append(curr_timestamp)
            user['no_msg'] += 1
            user['msg_sent'].append(user['no_msg'])
            
    store['DMs'][dm_id-1]['messages'].append({
            'message_id': message_id,
            'u_id': u_id,
            'message': message,
            'time_created': curr_timestamp,
            'reacts': [],
            'is_pinned': False,
            }
      )
    
    store['DMs'][dm_id-1]['dm_message_time'] = curr_timestamp  
    store['msg_change'].append(curr_timestamp)    
    store['total_no_msg'] += 1
    store['no_msg'].append(store['total_no_msg'])
    
    data_store.set(store)    
    tag_notification(u_id, message, -1, dm_id)        
    
    return {}

def message_react_v1(token, message_id, react_id):
    """
    When this function is called, a specificed message will be reacted to by
    the user, it adds a specific react depending on the given react id and adds
    the user to a list of users who have reacted to that same message

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member
    message_id(<int>) - A unique integer assigned to a message, which is
    represents the message the user is removing
    react_id(<int>) - A unique integer assigned to specific forms of reacts

    Exceptions:
    AccessError - Occurs when token is not in Streams
    InputError - Occurs when react id is invalid
    InputError - Occurs when an invalid message_id is passed
    AccessError - Occurs when the user attempting to react is not in the channel or dm
    InputError - Occurs if the user has already reacted to that message.

    Return Value:
    No Return
    """
    
    store = data_store.get()
    
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
        
    if react_id != 1:
        raise InputError(description ='Invalid React')

    auth_id = decode_token(token)['u_id']
    
    type_channel = False
    type_dm = False
    user_in_dm = False
    message_channel = -1
    message_dm = -1

    #Find the message in channels;
    for channels in store['channels']:
        for msg_ch in channels['messages']:
            if message_id == msg_ch['message_id']:
                message_channel = channels['channel_id']
                type_channel = True
                
    #Find the message in dms;        
    if type_channel == False:
        for dms in store['DMs']:
            for msg_dm in dms['messages']:
                if message_id == msg_dm['message_id']:
                    message_dm = dms['dm_id']
                    type_dm = True
    
    #message is not found in either channels and dms
    if type_channel == False and type_dm == False:
        raise InputError(description ='Invalid message ID')
    

    if type_channel == True:
        if not check_user_in_channel(auth_id, message_channel):
            raise InputError(description ='Invalid permission to react')
        

    if type_dm == True:
        for users in store['DMs'][message_dm-1]['members']:
            if auth_id == users['u_id']:
                user_in_dm = True
        if user_in_dm == False and auth_id != store['DMs'][message_dm-1]['owner']:    
            raise InputError(description ='Invalid permission to react')             
       
    if type_channel == True:
        id_message_sender = store['channels'][message_channel-1]['messages'][message_id-1]['u_id']
        name = store['channels'][message_channel-1]["name"]
        for n in store['channels'][message_channel-1]['messages']:
            if message_id == n['message_id'] and len(n['reacts']) == 0:
                n['reacts'].append({})
                n['reacts'][0]['react_id'] = react_id
                n['reacts'][0]['u_ids'] = []
                n['reacts'][0]['u_ids'].append(auth_id)
                n['reacts'][0]['is_this_user_reacted'] = False
                break
                
            elif message_id == n['message_id'] and auth_id in n['reacts'][0]['u_ids']:
                raise InputError(description ='User has already reacted to message')
                
            elif message_id == n['message_id'] and not auth_id in n['reacts'][0]['u_ids']:
                n['reacts'][0]['u_ids'].append(auth_id)
                break
                
    if type_dm == True:
        id_message_sender = store['DMs'][message_dm-1]['messages'][message_id-1]['u_id']
        name = store['DMs'][message_dm-1]["name"]
        for n in store['DMs'][message_dm-1]['messages']:
            if message_id == n['message_id'] and len(n['reacts']) == 0:
                n['reacts'].append({})
                n['reacts'][0]['react_id'] = react_id
                n['reacts'][0]['u_ids'] = []
                n['reacts'][0]['u_ids'].append(auth_id)
                n['reacts'][0]['is_this_user_reacted'] = False
                break
            
            elif message_id == n['message_id'] and auth_id in n['reacts'][0]['u_ids']:
                raise InputError(description ='User has already reacted to message')
                
            elif message_id == n['message_id'] and not auth_id in n['reacts'][0]['u_ids']:
                n['reacts'][0]['u_ids'].append(auth_id)
                break    

    # add in notifications
    users = store["users"]
    user_handle = users[auth_id-1]["handle_str"]
    users[id_message_sender-1]["notifications"].append({
        "channel_id": message_channel,
        "dm_id": message_dm,
        "notification_message": f"{user_handle} reacted to your message in {name}"
    })
    data_store.set(store)

    return {}

def message_unreact_v1(token, message_id, react_id):
    """
    When this function is called, a specificed message will be unreacted to by
    the user, it removes a specific react depending on the given react id and removes
    the user to a list of users who have reacted to that same message

    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member
    message_id(<int>) - A unique integer assigned to a message, which is
    represents the message the user is removing
    react_id(<int>) - A unique integer assigned to specific forms of reacts

    Exceptions:
    AccessError - Occurs when token is not in Streams
    InputError - Occurs when react id is invalid
    InputError - Occurs when an invalid message_id is passed
    AccessError - Occurs when the user attempting to react is not in the channel or dm
    InputError - Occurs if there are is no reaction to undo.

    Return Value:
    No Return
    """
    
    store = data_store.get()
    
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
        
    if react_id != 1:
        raise InputError(description ='Invalid Unreact')

    auth_id = decode_token(token)['u_id']
    
    type_channel = False
    type_dm = False
    user_in_dm = False
    message_channel = -1
    message_dm = -1

    #Find the message in channels;
    for channels in store['channels']:
        for msg_ch in channels['messages']:
            if message_id == msg_ch['message_id']:
                message_channel = channels['channel_id']
                type_channel = True
                
    #Find the message in dms;        
    if type_channel == False:
        for dms in store['DMs']:
            for msg_dm in dms['messages']:
                if message_id == msg_dm['message_id']:
                    message_dm = dms['dm_id']
                    type_dm = True
    
    #message is not found in either channels and dms
    if type_channel == False and type_dm == False:
        raise InputError(description ='Invalid message ID')
    

    if type_channel == True:
        if not check_user_in_channel(auth_id, message_channel):
            raise InputError(description ='Invalid permission to unreact')
        

    if type_dm == True:
        for users in store['DMs'][message_dm-1]['members']:
            if auth_id == users['u_id']:
                user_in_dm = True
        if user_in_dm == False and auth_id != store['DMs'][message_dm-1]['owner']:    
            raise InputError(description ='Invalid permission to unreact')             
       
    if type_channel == True:
        for n in store['channels'][message_channel-1]['messages']:
            if message_id == n['message_id'] and len(n['reacts']) == 0:
                raise InputError(description ='There are no reactions to this message')
                
            elif message_id == n['message_id'] and len(n['reacts'][0]['u_ids']) == 1:
                n['reacts'].clear()
                break
                
            elif message_id == n['message_id'] and auth_id in n['reacts'][0]['u_ids']:
                n['reacts'][0]['u_ids'].remove(auth_id)
                break
                
    if type_dm == True:
        for n in store['DMs'][message_dm-1]['messages']:
            if message_id == n['message_id'] and len(n['reacts']) == 0:
                raise InputError(description ='There are no reactions to this message')
                
            elif message_id == n['message_id'] and len(n['reacts'][0]['u_ids']) == 1:
                n['reacts'].clear()
                break
                
            elif message_id == n['message_id'] and auth_id in n['reacts'][0]['u_ids']:
                n['reacts'][0]['u_ids'].remove(auth_id)
                break

    data_store.set(store)
    
    return {}

def message_pin_v1(token, message_id):
    """
    When this function is called, a specificed message will be pinned by a
    owner of a channel
    
    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member
    message_id(<int>) - A unique integer assigned to a message, which is
    represents the message the user is removing
    react_id(<int>) - A unique integer assigned to specific forms of reacts

    Exceptions:
    AccessError - Occurs when token is not in Streams
    InputError - Occurs when an invalid message_id is passed
    InputError - Occurs when the user attempting to pin is not in the channel or dm
    AccessError - Occurs if the user does not have owner permissions
    InputError - Occurs if the message is already pinned
    

    Return Value:
    No Return
    """
    store = data_store.get()

    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
        
    type_message = False
    type_dm = False
    user_in_dm = False

    auth_id = decode_token(token)['u_id']
    message_channel = 0
    
    for channels in store['channels']:
        for message in channels['messages']:
            if message_id == message['message_id']:
                message_channel = channels['channel_id']
                type_message = True

    
    if type_message == False:
        for dms in store['DMs']:
            for message in dms['messages']:
                if message_id == message['message_id']:
                    message_dm = dms['dm_id']
                    type_dm = True

        
    if type_message == False and type_dm == False:
        raise InputError(description ='Invalid message ID')

    if type_message == True:
        if not check_user_in_channel(auth_id, message_channel):
            raise InputError(description ='User is not in channel')
            
        if user_is_stream_owner(auth_id) == False \
        and user_is_channel_owner(auth_id, message_channel) == False:
            raise AccessError(description ='Invalid permission to pin message')
            
    if type_dm == True:
        for users in store['DMs'][message_dm-1]['members']:
            if auth_id == users['u_id']:
                    user_in_dm = True
                
        if user_in_dm == False and auth_id != store['DMs'][message_dm-1]['owner']:    
            raise InputError(description ='User is not in DM')
            
        if user_in_dm == True and auth_id != store['DMs'][message_dm-1]['owner']:
            raise AccessError(description ='Invalid permission to pin message')  
                
    if type_message == True:
        for n in store['channels']:
            for msg in n['messages']:
                if message_id == msg['message_id'] and msg['is_pinned'] == True:
                    raise InputError(description ='Message already pinned')
                    
                elif message_id == msg['message_id'] and msg['is_pinned'] == False:
                    msg['is_pinned'] = True
                    break

    if type_dm == True:
        for d in store['DMs']:
            for msg in d['messages']:
                if message_id == msg['message_id'] and msg['is_pinned'] == True:
                   raise InputError(description ='Message already pinned')
                    
                elif message_id == msg['message_id'] and msg['is_pinned'] == False:
                    msg['is_pinned'] = True
                    break

                
    data_store.set(store)
    
    return {}

def message_unpin_v1(token, message_id):
    """
    When this function is called, a specificed message will be unpinned by an
    owner of a channel
    
    Arguments:
    token(an authorisation hash) - token assigned to an authorised user, this
    authorised user should be an existing member
    message_id(<int>) - A unique integer assigned to a message, which is
    represents the message the user is removing
    react_id(<int>) - A unique integer assigned to specific forms of reacts

    Exceptions:
    AccessError - Occurs when token is not in Streams
    InputError - Occurs when an invalid message_id is passed
    InputError - Occurs when the user attempting to unpin is not in the channel or dm
    AccessError - Occurs if the user does not have owner permissions
    InputError - Occurs if the message is not pinned
    

    Return Value:
    No Return
    """
    store = data_store.get()

    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
        
    type_message = False
    type_dm = False
    user_in_dm = False

    auth_id = decode_token(token)['u_id']
    message_channel = 0
    
    for channels in store['channels']:
        for message in channels['messages']:
            if message_id == message['message_id']:
                message_channel = channels['channel_id']
                type_message = True

    
    if type_message == False:
        for dms in store['DMs']:
            for message in dms['messages']:
                if message_id == message['message_id']:
                    message_dm = dms['dm_id']
                    type_dm = True

        
    if type_message == False and type_dm == False:
        raise InputError(description ='Invalid message ID')

    if type_message == True:
        if not check_user_in_channel(auth_id, message_channel):
            raise InputError(description ='User is not in channel')
            
        if user_is_stream_owner(auth_id) == False \
        and user_is_channel_owner(auth_id, message_channel) == False:
            raise AccessError(description ='Invalid permission to unpin message')
            
    if type_dm == True:
        for users in store['DMs'][message_dm-1]['members']:
            if auth_id == users['u_id']:
                    user_in_dm = True
                
        if user_in_dm == False and auth_id != store['DMs'][message_dm-1]['owner']:    
            raise InputError(description ='User is not in DM')
            
        if user_in_dm == True and auth_id != store['DMs'][message_dm-1]['owner']:
            raise AccessError(description ='Invalid permission to unpin message')  
                
    if type_message == True:
        for n in store['channels']:
            for msg in n['messages']:
                if message_id == msg['message_id'] and msg['is_pinned'] == False:
                    raise InputError(description ='Message is not pinned')
                    
                elif message_id == msg['message_id'] and msg['is_pinned'] == True:
                    msg['is_pinned'] = False
                    break

    if type_dm == True:
        for d in store['DMs']:
            for msg in d['messages']:
                if message_id == msg['message_id'] and msg['is_pinned'] == False:
                    raise InputError(description ='Message is not pinned')
                    
                elif message_id == msg['message_id'] and msg['is_pinned'] == True:
                    msg['is_pinned'] = False
                    break

                
    data_store.set(store)
    
    return {}

def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    print("additional message")
    print(message)
    store = data_store.get()
    
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
    auth_id = decode_token(token)['u_id']
    found_channel_message = False
    found_dm_message = False
    
    for channels in store['channels']:
        for messages in channels['messages']:
            if og_message_id == messages['message_id']:
                message_content = messages['message']
                found_channel_message = True
    
    if found_channel_message == False:
        for dms in store['DMs']:
            for messages in dms['messages']:
                if og_message_id == messages['message_id']:
                    message_content = messages['message']
                    print("message_content")
                    print(message_content)
                    found_dm_message = True
    if not found_dm_message and not found_channel_message: 
        raise InputError(description ='Invalid og_message_id')
    
    if len(message) > 1000:
        raise InputError(description ='Message cannot be greater than 1000')

    if dm_id == -1:
        # share message to channel
        # check for channel_id
        if check_channel(channel_id) == False:
            raise InputError(description ='Invalid Channel Id')
        if not check_user_in_channel(auth_id, channel_id):
            raise AccessError(description ='User is not in the channel called')
        if len(message) > 0:
            message_sent = message_content + " " + message
            print("message_sent1")
            print(message_sent)
        else:
            message_sent = message_content
        print("message_sent parameter")
        print(message_sent)
        shared_message_id = message_send_v1(token, channel_id, message_sent)
    elif channel_id == -1:
        # share message to dm
        # check for dm 
        dm_exists = False
        for dms in store['DMs']:
            if dm_id == dms['dm_id']:
                dm_exists = True

        if dm_exists == False:
            raise InputError(description ='Invalid dm_id')

        dm_user = False
        for user in store['DMs'][dm_id-1]['members']:
            if user['u_id'] == auth_id:
                dm_user = True

        if dm_user == False:
            raise AccessError(description ='The auth_user not in DM')
        if len(message) > 0:
            message_sent = message_content + " " + message
        else:
            message_sent = message_content
        shared_message_id = message_senddm_v1(token, dm_id, message_sent)
    else:
        raise InputError(description ='neither channel_id nor dm_id are -1')
    
    return {'shared_message_id': shared_message_id}

# type == 1: then its a channel, type == 2: then its a dm
def tag_notification(u_id, message, channel_id, dm_id):
    # look through message for an @
    handles = re.findall('@[a-z0-9]*', message)

    store = data_store.get()
    # finding channel/dm name
    if dm_id == -1:
        name = store['channels'][channel_id-1]["name"]
        # dictioanry containing u_id and permission_id
        members = store['channels'][channel_id-1]["all_members"]
    else: 
        name = store['DMs'][dm_id-1]["name"]
        # has all of user
        members = store['DMs'][dm_id-1]["members"]

    users = store["users"]
    # find handle of user that is tagging
    user_handle = users[u_id-1]["handle_str"]

    # look through saved handles and see if there is one that exists
    for handle in handles:
        for user in users:
            if user["handle_str"] == handle[1:]:
                #then handle is correct
                # now check if this user is part of this particular channel or dm
                for member in members:
                    if member["u_id"] == user["u_id"]:        
                        user["notifications"].append({
                            "channel_id": channel_id,
                            "dm_id": dm_id,
                            "notification_message": f"{user_handle} tagged you in {name}: {message[:20]}"
                        })
    data_store.set(store)
    return {}
