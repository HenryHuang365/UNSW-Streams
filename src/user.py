'''
This module contains register and login
'''
import io
import os
import re
import urllib.request

from datetime import datetime
from urllib.error import HTTPError

from flask import url_for
from PIL import Image

from src import config
from src.checks import check_email_not_in_use, check_name, check_user_exists
from src.data_store import data_store
from src.error import AccessError, InputError
from src.token_funcs import check_valid_token, decode_token, gen_token


BASE_URL = config.url

def users_all_v1(token):
    if check_valid_token(token) == False:
        raise AccessError("The Token is invalid") 
  
    store = data_store.get()

    users_all = []

    #for users in the datastore, show all the users and relevant details
    for user in store["users"]:
        if user["email"] != "":
            users_all.append({
                "u_id": user["u_id"],
                "email": user["email"],
                "name_first": user["name_first"],
                "name_last": user["name_last"],
                "handle_str": user["handle_str"],
                "profile_img_url": user["profile_img_url"]
                })

    return {"users": users_all}

## NEW FUNCTIONS ---------------------------------------------------------------
def user_stats_v1(token):
    if check_valid_token(token) == False:
        raise AccessError("The Token is invalid") 
    
    store = data_store.get()
    u_id = decode_token(token)['u_id']
    user_stats = {}
    
    ch_hist = []
    dm_hist = []
    msg_hist = []
    
    for user in store['users']:
        if user['u_id'] == u_id:
            for ch_idx in range(len(user['ch_join'])):
                ch_dict = {'num_channels_joined': user['ch_join'][ch_idx],
                           'time_stamp': user['chs_time'][ch_idx]}
                ch_hist.append(ch_dict)
                
            for dm_idx in range(len(user['dm_join'])):
                dm_dict = {'num_dms_joined': user['dm_join'][dm_idx],
                           'time_stamp': user['dms_time'][dm_idx]}
                dm_hist.append(dm_dict)                
        
            for msg_idx in range(len(user['msg_sent'])):
                msg_dict = {'num_messages_sent': user['msg_sent'][msg_idx],
                           'time_stamp': user['msg_time'][msg_idx]}
                msg_hist.append(msg_dict)   
                
            num_channels_joined = user['no_ch']
            num_dms_joined = user['no_dm']
            num_msgs_sent = user['no_msg']

    nom = sum([num_channels_joined, num_dms_joined, num_msgs_sent])
    
    num_channels = store['total_no_chs']
    num_dms = store['total_no_dms']
    num_msgs = store['total_no_msg']
    denom = sum([num_channels, num_dms, num_msgs])    
    
    involvement_rate = 0
    
    if denom == 0:
        involvement_rate = 0
    else:
        involvement_rate = nom/denom
    
    if involvement_rate > 1:
        involvement_rate = 1
  
    user_stats = {
        "channels_joined": ch_hist,
        "dms_joined": dm_hist,
        "messages_sent": msg_hist,
        "involvement_rate": involvement_rate
    }

    return {"user_stats": user_stats}

def users_stats_v1(token):
    if check_valid_token(token) == False:
        raise AccessError("The Token is invalid") 
    
    store = data_store.get()

    workspace_stats = []

    users_in_one_channel_or_dm = 0
    
    
    num_users = len(store['users'])
    
    user_in_dm_channel = []
    
    channels_hist = []
    for ch_idx in range(len(store['no_channels'])):
        ch_dict = {"num_channels_exist": store['no_channels'][ch_idx], 
                    "time_stamp": store['channels_change'][ch_idx]}
        channels_hist.append(ch_dict)    
    
    dms_hist = []
    for dms_idx in range(len(store['no_dms'])):
        dms_dict = {"num_dms_exist": store['no_dms'][dms_idx], 
                    "time_stamp": store['DMs_change'][dms_idx]}
        dms_hist.append(dms_dict)    
    
    
    
    msg_hist = []
    for msg_idx in range(len(store['no_msg'])):
        msg_dict = {"num_messages_exist": store['no_msg'][msg_idx], 
                    "time_stamp": store['msg_change'][msg_idx]}
        msg_hist.append(msg_dict)
    

    for user in store['users']:
        for ch in store['channels']:
            for member in ch['all_members']:
                if member['u_id'] == user['u_id']:
                    user_in_dm_channel.append(user['u_id'])
                    
        for dm in store['DMs']:
            for member in dm['members']:
                if member['u_id'] == user['u_id']:
                    user_in_dm_channel.append(user['u_id']) 
                    
    
    user_in_dm_channel = list(set(user_in_dm_channel))               
    users_in_one_channel_or_dm = len(user_in_dm_channel)
    utilisation_rate = users_in_one_channel_or_dm/num_users

    workspace_stats = {
                "channels_exist": channels_hist,
                "dms_exist": dms_hist,
                "messages_exist": msg_hist,
                "utilization_rate": utilisation_rate
            }

    return {"workspace_stats": workspace_stats}

def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    if check_valid_token(token) == False:
        raise AccessError("The Token is invalid") 

    store = data_store.get()
    u_id = decode_token(token)['u_id']

    try:
        image_get = urllib.request.urlopen(img_url)
    except HTTPError as e:
        raise InputError("Wrong HTTP status code") from e
    
    image_open = io.BytesIO(image_get.read())
    img = Image.open(image_open)

    width,height = img.size

    if img.format != 'JPEG':

        raise InputError("Image uploaded is not a JPEG")


    if x_end - x_start > width or y_end - y_start > height:
        raise InputError("Dimensions not in image bounds")
    
    if x_end < x_start or y_end < y_start:
        raise InputError("End values cannot be smaller than start values")

    img_cropped = img.crop((x_start, y_start, x_end, y_end))


    img_name = str(u_id) + ".jpeg"
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/static/"
    #print("DIR PATH = " + dir_path)

    img_path = dir_path + img_name
    img_file = open(img_path,"wb")
    img_cropped.save(img_file, "JPEG")
    img_file.close()

    saved_img_url = url_for("static", filename = img_name, _external = True)
    print("SAVED URL = " + saved_img_url) 
    users = store['users']
    for user in users:
        if user["u_id"] == u_id:
            user["profile_img_url"] = saved_img_url

    data_store.set(store)  

    return {}

## OLD FUNCTIONS CONT ------------------------------------------------------------
def user_profile_v1(token, u_id):
    '''
    user_profile_v1 acts to show a users details

    Arguments:
    token(<string>) - Token provided my software to authenticate users
    u_id(<int>) - This is the user whos details need to be retrieved

    Exceptions:
    InputError - When the u_id entered does not refer to a valid user
    AccessError - When the token entered does not corealate to valid user

    Return Value:
    Returns user details -> their u_id, email, name_first, name_last 
    and handle_str
    '''
    if not check_valid_token(token):
        raise AccessError(description="Token invalid")
    if not check_user_exists(u_id):
        raise InputError(description="u_id does not refer to a valid user")
    user_ans = {}
    store = data_store.get()
    users = store['users']
    for user in users:
        if user["u_id"] == u_id:
            user_ans = user
    return {"user": {
       "u_id": user_ans["u_id"],
        "email": user_ans["email"],
        "name_first": user_ans["name_first"],
        "name_last": user_ans["name_last"],
        "handle_str": user_ans["handle_str"],
        "profile_img_url": user["profile_img_url"]
    }}


def user_profile_setname_v1(token, name_first, name_last):
    '''
    user_profile_setname_v1 acts to change a users name and sets in 
    data store

    Arguments:
    token(<string>) - Token provided my software to authenticate users
    name_first(<string>) - This is the new name_first provided by user
    name_last(<string>) - This is the new name_last provided by user

    Exceptions:
    InputError - When the length of name_first or name_last is not between 
    1 and 50 characters inclusive
    AccessError - When the token entered does not corealate to valid user

    Return Value:
    Returns empty java script object
    '''
    if not check_valid_token(token):
        raise AccessError(description="Token invalid")

    # check if length of first name is between 1 and 50 characters
    if not check_name(name_first):
        raise InputError(description='length of name_first is not between 1 and 50 characters inclusive')

    # check if length of last name is between 1 and 50 characters
    if not check_name(name_last):
        raise InputError(description='length of name_last is not between 1 and 50 characters inclusive')

    u_id = decode_token(token)['u_id']
    store = data_store.get()
    users = store['users']
    for user in users:
        if user["u_id"] == u_id:
            user["name_first"] = name_first
            user["name_last"] = name_last
    
    data_store.set(store)
    return {}


def user_profile_setemail_v1(token, email):
    '''
    user_profile_setemail_v1 acts to change a users email and sets in 
    data store

    Arguments:
    token(<string>) - Token provided my software to authenticate users
    email(<string>) - This is the new email provided by user

    Exceptions:
    InputError - When the email is already in use or when email is not valid
    AccessError - When the token entered does not corealate to valid user

    Return Value:
    Returns empty
    '''
    if not check_valid_token(token):
        raise AccessError(description="Token invalid")

    if not check_email_not_in_use(email):
        raise InputError(description='email address is already being used by another user')

    if re.search('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$', email) is None:
        raise InputError(description='email entered is not a valid email')
    
    u_id = decode_token(token)['u_id']
    store = data_store.get()
    users = store['users']
    for user in users:
        if user["u_id"] == u_id:
            user["email"] = email
    
    data_store.set(store)
    return {}

def user_profile_sethandle_v1(token, handle):
    '''
    user_profile_sethandle_v1 acts to change a users email and sets in 
    data store

    Arguments:
    token(<string>) - Token provided my software to authenticate users
    handle(<string>) - This is the new handle provided by user

    Exceptions:
    InputError - When the handle is non-alphanumeric or when the handle
    length is not between 3 and 20 characters
    AccessError - When the token entered does not corealate to valid user

    Return Value:
    Returns empty
    '''
    if not check_valid_token(token):
        raise AccessError(description="Token invalid")
    
    if len(handle) < 3 or len(handle) > 20:
        raise InputError(description="length of handle_str is not between 3 and 20 characters inclusive")
    
    #check for non-alphanumeric characters
    if re.search('[^A-Za-z0-9]', handle):
        raise InputError(description="handle_str contains characters that are not alphanumeric")

    u_id = decode_token(token)['u_id']
    store = data_store.get()
    users = store['users']
    for user in users:
        if user['handle_str'] == handle:
            raise InputError(description="the handle is already used by another user")

    for user in users:
        if user["u_id"] == u_id:
            user["handle_str"] = handle

    data_store.set(store)
    return {}
