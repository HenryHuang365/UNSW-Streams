'''
    This file has been created to store all helper functions.
    These include the checking of the user id
    It has been implemented in a separate file to ensure that there is no circular
    referencing between the channel and channels files
'''
from flask.helpers import url_for
from src.data_store import data_store
from PIL import Image
import os
import io
import urllib.request

def check_channel(channel_id):
    '''
    This function checks a given channel id against data_store to see if it
    exists in the data already or not to then return a boolean value.

    Arguments:
    channel_Id(<int>) - A unique integer assigned to the channel for identification

    Exceptions:
    None

    Return Value:
    Returns found_channel(<Boolean>) will return True if the id exists in
    data_store and will return False if it is not found in data store.
    '''
    store = data_store.get()
    # check if channel_Id is valid
    # raise InputError
    found_channel = False
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            # the input channel_id is existing
            found_channel = True
    return found_channel

def check_user_in_channel(u_id, channel_id):
    '''
    This function checks a given user id against the user ids in a specific channel
    in data_store to see if it exists in the data already or not to then
    return a boolean value.

    Arguments:
    channel_Id(<int>) - A unique integer assigned to the channel for identification
    u_id(<int>) - A unique integer assigned to a user for identification

    Exceptions:
    None

    Return Value:
    Returns found_channel(<Boolean>) will return True if the id exists in
    data_store and will return False if it is not found in data store.
    '''
    store = data_store.get()
    # check if the given user_id is in the given channel or not
    found_id = False
    for channel in store['channels']:
        if channel["channel_id"] == channel_id:
            # found the matching channel
            if u_id in (member["u_id"] for member in channel["all_members"]):
                # the user is in the channel
                found_id = True

    return found_id

def check_user_exists(u_id):
    '''
    This function checks a given user id against data_store to see if it
    exists in the data already or not to then return a boolean value.

    Arguments:
    u_id(<int>) - A unique integer assigned to a user for identification

    Exceptions:
    None

    Return Value:
    Returns found_channel(<Boolean>) will return True if the id exists in
    data_store and will return False if it is not found in data store.
    '''
    store = data_store.get()
    # check if the given u_id is valid
    # InputError
    found_id = False
    for user in store['users']:
        if user["u_id"] == u_id and user["email"] != "":
            found_id = True

    return found_id

def channel_is_public(channel_id):
    '''
    This function checks a given channel to see if it is public against

    Arguments:
    channel_Id(<int>) - A unique integer assigned to the channel for identification

    Exceptions:
    None

    Return Value:
    Returns found_channel(<Boolean>) will return True if the id is public
    and will return False if it is private
    '''
    store = data_store.get()

    # returns the is_public value of a specific channel if the channel id matches the argument
    return True in (channel['is_public'] for channel in store['channels'] \
                    if channel['channel_id'] is channel_id)

def user_is_stream_owner(user_id):
    '''
    This function checks if the permission assigned to
    a user id is 1 (stream owner) or 2 (stream member)

    Arguments:
    user_id(<int>) - a unique integer assigned to the user for identification

    Exceptions:
    None

    Return Value: True if the user_id has a stream owner permission_id
    otherwise false if user is a stream member
    '''

    store = data_store.get()
    for user in store["users"]:
        if user["u_id"] == user_id:
            permission_id = user["permission_id"]

    if permission_id == 1:
        return True
    return False

def user_is_channel_owner(user_id, channel_id):
    '''
    This function checks if the user is a channel owner given a channel id

    Arguments:
    user_id(<int>) - a unique integer assigned to the user for identification
    channel_id(<int>) - a unique integer assigned to the channel for identification

    Exceptions:
    None

    Return Value: True if the user_id has a channel owner permission_id otherwise false
    '''
    store = data_store.get()
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            ch = channel
            
    return user_id in ch["owner_members"]

def check_name(name):
    return len(name) >= 1 and len(name) <= 50

def check_email_not_in_use(email):
    store = data_store.get()
    users = store['users']

    for user in users:
        if user["email"] == email:
            return False
    return True
