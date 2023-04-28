#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 01:01:33 2021

@author: caspar
"""

from src.data_store import data_store
from src.token_funcs import decode_token, check_valid_token
from src.error import AccessError, InputError
from datetime import datetime

def dm_create_v1(token, u_ids):
    '''
    Create a DM with name based on the members in the DM
    
    Arguments:
        u-ids (list of ints)    - Contains the user(s) that this DM is directed to, and will not include the creator.
        token (str)    - The token of the corresponding user (who call this function)
    
    Exceptions:
        InputError  - Occurs when any u_id in u_ids does not refer to a valid user
        AccessError - Occurs when token is invalid
    
    Return Value:
        Returns {dm_id} (int) on successful call
    '''
    #Check if token is in the daabased
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")
    
    #Load the database
    store = data_store.get()
    
    #Check if u_ids are all existing
    existing_uids = []
    for user in store['users']:
        existing_uids.append(user['u_id'])
    
    
    if not all(ids in existing_uids for ids in u_ids):
        raise InputError(description ="The uids are not all in the database")

    #decode_token to find the corresponding user (owner)
    auth_id = decode_token(token)['u_id']
    
    dm_name = []
    
    members = []
    #add the handle into dm_name and add them into the member list
    for user in store['users']:        
        if user['u_id'] in u_ids:
            members.append(user)
            time_changed = int(datetime.now().timestamp())   
            user['no_dm'] += 1
            user['dm_join'].append(user['no_dm'])
            user['dms_time'].append(time_changed) 
            dm_name.append(user['handle_str'])
        elif user['u_id'] == auth_id:
            members.append(user)
            time_changed = int(datetime.now().timestamp())   
            user['no_dm'] += 1
            user['dm_join'].append(user['no_dm'])
            user['dms_time'].append(time_changed) 
            dm_name.append(user['handle_str'])
           
    #Arrange the dm_name in alphabetical order       
    dm_name.sort()
    dm_name = ', '.join(dm_name)
    
    DMs = store['DMs']
        
    dm_id = len(DMs) + 1

    store["DMs"].append({
        "dm_id": dm_id,
        "name": dm_name,
        "members": members,
        "owner": auth_id,
        "messages": [],
        'dm_message_time': None
    })

    time_changed = int(datetime.now().timestamp())    
    store['DMs_change'].append(time_changed)
    store['total_no_dms'] += 1
    store['no_dms'].append(store['total_no_dms'])    


    # add notification
    users = store["users"]
    user_handle = users[auth_id-1]["handle_str"]
    for user in store['users']:        
        if user['u_id'] in u_ids:
            user["notifications"].append({
                "channel_id": -1,
                "dm_id": dm_id,
                "notification_message": f"{user_handle} added you to {dm_name}"
            })

    #setting the values to the data store
    data_store.set(store)

    return {
        'dm_id': dm_id,
        }
    
def dm_list_v1(token):
    '''
    Returns the list of DMs that the user is a member of.
    
    Arguments:
        token (str)    - A unique token of the corresponding user (who call this function)
    
    Exceptions:
        AccessError - Occurs when token is invalid
    
    Return Value:
        Returns {dms} (a list of dict{dm_id, name})
    '''    
    #Return access error if the token is invalid
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
    
    #decode_token to find the corresponding user (owner)
    auth_id = decode_token(token)['u_id']
    
    #Load the database
    store = data_store.get()
    
    #loop through the DMs to find the DM that the user is a member of 
    DMs = store['DMs']    
    
    dms = []
    for dm in DMs:
        for member in dm['members']:
            if member['u_id'] == auth_id:
                dms.append({
                    'dm_id': dm['dm_id'],
                    'name': dm['name']
                    })
       
    return {
        'dms': dms
        }


def dm_messages_v1(token, dm_id, start):
    """
    Given a DM with ID dm_id that the authorised user is a member of, 
    return up to 50 messages between index "start" and "start + 50".
    Message with index 0 is the most recent message in the DM.
    This function returns a new index "end" which is the value of "start + 50", or,
    if this function has returned the least recent messages in the DM,
    returns -1 in "end" to indicate there are no more messages to load after this return.

    Arguments:
    token (str) - A unique token of the corresponding user (who call this function)
    dm_id (int) - A unique integer assigned to a DM
    start(<int>) - This is a chosen integer referring to the first index
    position of a list of messages.

    Exceptions:
    AccessError - Occurs when token is invalid
    AccessError - dm_id is valid and the authorised user is not a member of the DM    
    InputError - dm_id does not refer to a valid DM
    InputError - start is greater than the total number of messages in the channel

    Return Value:
    Returns 'messages'<[string]> on condition that there are more messages in
    data_store than the value of start
    Returns 'end'<int> on condition that is is start+50 if there are more than
    50 messages in data_store that follow the starting index called
    Returns 'start'<int> on condition that it isn't greater than the amount
    of messages
    """
    #Return access error if the token is invalid
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
    
    store = data_store.get()
    
    #decode_token to find the corresponding user (owner)
    auth_id = decode_token(token)['u_id']        
    
    #Return Access error if dm_id is valid and 
    #the authorised user is not a member of the DM    
    DMs = store['DMs']
    
    found_DM = False
    member_list = []
    for dm in DMs:
        if dm['dm_id'] == dm_id:
            target_dm = dm
            found_DM = True
            #Extract all the user_id in the dm            
            for user in dm['members']:
                member_list.append(user['u_id'])
            #if the authoriised user is not a member of the DM, return AccessError
            if not auth_id in member_list:
                raise AccessError(description ="The authorised user is not a member of the DM")
    
    #Return InputError if dm_id is not found
    if found_DM == False:
        raise InputError(description ='dm_id does not refer to a valid DM')
        
    #check if start is greater than messages, however not fail if there are no messages.
    messages = target_dm['messages']
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
        if len(msg['reacts']) != 0 and auth_id in msg['reacts'][0]['u_ids']:
            msg['reacts'][0]['is_this_user_reacted'] = True
    
    return {
        'messages': msg_from_start,
        'start': start,
        'end': end,
    }    


def dm_details_v1(token, dm_id):
    ''' Users that are part of this direct message can view basic information about the DM
    Arguments:
    token - token of the person calling the function
    dm_id (integer) - dm id of the specific channel 

    Exceptions:
    InputError - invalid dm_id, u_id is not a valid user, invalid auth_id
    AccessError - auth_id is not part of the dm'''
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
    
    store = data_store.get()
    
    #decode_token to find the corresponding user (owner)
    auth_id = decode_token(token)['u_id']        
    
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
            if not auth_id in member_list:
                raise AccessError(description ="The authorised user is not a member of the DM")
    
    #Return InputError if dm_id is not found
    if found_DM == False:
        raise InputError(description ='dm_id does not refer to a valid DM')

    # error checking finished

    members = []
    name = ''
    for specific_dm in DMs:
        # add more dm
        if dm_id == specific_dm['dm_id']:
            name = specific_dm["name"]
            for member in specific_dm['members']:
                members.append({
                    "u_id": member['u_id'],
                    "email": member['email'],
                    "name_first": member['name_first'],
                    "name_last": member['name_last'],
                    "handle_str": member['handle_str'],
                    "profile_img_url": member["profile_img_url"]
                    })

    return {
        "name" : name,
        "members" : members
    }

#---------------------------------------------------------------------#


def dm_remove_v1(token, dm_id):
    '''
    Remove an existing DM. This can only be done by the original creator
    of the DM.
    
    Arguments:
        dm_id (integer) - DM id of the specific DM

    Exceptions:
        InputError: dm_id does not refer to a valid DM
        AccessError: the user is not the original DM creator
    '''
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
    
    store = data_store.get()
    
    #decode_token to find the corresponding user (owner)
    auth_id = decode_token(token)['u_id']        
    
    #Return Access error if dm_id is valid and 
    #the authorised user is not a member of the DM    
    DMs = store['DMs']
    found_DM = False
    
    for dm in DMs:
        if dm['dm_id'] == dm_id:
            found_DM = True
    
    # Return InputError if dm_id is not found
    if found_DM == False:
        raise InputError(description ='dm_id does not refer to a valid DM')

    for specific_dm in DMs:
        if dm_id == specific_dm["dm_id"] and auth_id != specific_dm['owner']:
            raise AccessError(description ="The authorised user is not the original DM creator")      

            

    for user in store['users']:  
        for dm in DMs:
            if dm_id == dm['dm_id']:
                for member in dm['members']:
                     if user['u_id'] == member['u_id']:
                         time_changed = int(datetime.now().timestamp())   
                         user['no_dm'] -= 1
                         user['dm_join'].append(user['no_dm'])
                         user['dms_time'].append(time_changed)  
                 
    for specific_dm in DMs:   
       if dm_id == specific_dm["dm_id"] and auth_id == specific_dm['owner']:        
            DMs.remove(specific_dm)



            
    time_changed = int(datetime.now().timestamp())    
    store['DMs_change'].append(time_changed)
    store['total_no_dms'] -= 1
    store['no_dms'].append(store['total_no_dms'])    
    
    data_store.set(store)
    return {}

#-----------------------------------------------------------------------------------------------------#

def dm_leave_v1(token, dm_id):
    '''Given a DM ID, user is removed as a member of this DM.
    Arguments:
    dm_id (integer) - dm id of the specific DM
    Exceptions:
    InputError  - dm_id is not a valid DM
    AccessError - authorised user is not a member of DM with dm_id '''
    # check for invalid dm_id
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
    
    store = data_store.get()
    
    #decode_token to find the corresponding user (owner)
    auth_id = decode_token(token)['u_id']        
    
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
                # [1, 2, ,3,,,]
                member_list.append(user['u_id'])
            #if the authoriised user is not a member of the DM, return AccessError
            if not auth_id in member_list:
                raise AccessError(description ="The authorised user is not a member of the DM")
    
    #Return InputError if dm_id is not found
    if found_DM == False:
        raise InputError(description ='dm_id does not refer to a valid DM')

    # error checking finished

    for dm in DMs:
        # add more dm
        if dm["dm_id"] == dm_id:
            for member in dm['members']:
                if member['u_id'] == auth_id:
                    dm['members'].remove(member) # remove the user_dic from the members list
    
    time_changed = int(datetime.now().timestamp())        
    u_id = decode_token(token)['u_id']
    for user in store['users']:
        if user['u_id'] == u_id:
            time_changed = int(datetime.now().timestamp())   
            user['no_dm'] -= 1
            user['dm_join'].append(user['no_dm'])
            user['dms_time'].append(time_changed) 
    data_store.set(store)
    
    return {}

