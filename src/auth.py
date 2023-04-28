'''
This module contains register and login
'''
import hashlib
import os
import random
import re
import smtplib
import string

import jwt
from flask import url_for

from src.checks import check_email_not_in_use, check_name
from src.data_store import data_store
from src.error import AccessError, InputError
from src.token_funcs import add_token, decode_token, gen_token
from datetime import datetime

def auth_login_v2(email, password):
    '''
    auth_login_v2 acts to login the user to the software. It does this through
    checking that the user exists in data record data_store. If the user is
    found it will return their unique authorised user id.

    Arguments:
    email(<string>) - Chosen email the user inputs when they register
    password(<string>) - Chosen password of the user, must be 6 characters or
    greater

    Exceptions:
    InputError - Occurs when the email entered does not belong to any existing
    user in data_store
    InputError - Occurs when the password that is entered does not match
    to the corresponding email.

    Return Value:
    Returns 'auth_user_id'(<int>) on condition that both the email and password
    both are correct and correspond with the single user.
    '''
    store = data_store.get()
    users = store['users']
    exists = False
    for user in users:
        if user["email"] == email:
            exists = True
            if user["password"] == hashlib.sha256(password.encode()).hexdigest():
                u_id = user["u_id"]
            else:
                raise InputError(description='password is not correct')
    if not exists:
        raise InputError(description='email entered does not belong to a user')
    token = gen_token(u_id)
    add_token(token)
    data_store.set(store)
    return {
            'token': token,
            'auth_user_id': u_id,
        }

def auth_logout_v1(token):

    '''
    auth_logout_v1 acts to logout the user to the software. It does this through
    checking that the token is valid and then removing token from 
    data store

    Arguments:
    token(<string>) - Token provided to user when they login or register

    Exceptions:
    AccessError - If token is not valid
    InputError - Occurs when the password that is entered does not match
    to the corresponding email.

    Return Value:
    Returns empty json
    '''
    store = data_store.get()
    tokens = store['tokens']

    if token in tokens: 
        tokens.remove(token)
    else:
        raise AccessError(description='Token invalid')
    data_store.set(store)
    return {}

def auth_register_v2(email, password, name_first, name_last):

    #region docs
    '''
    auth_register_v2 acts as an intial registrition of an account for a user
    user into data_store. It takes multiple user details and creates a
    dictionary of their detials with a unique user id, which is then stored
    into data_store.

    Arguments:
    email(<string>) - Chosen email the user inputs when they register
    password(<string>) - Chosen password of the user, must be 6 characters or
    greater
    name_first(<string>) - the first name of the user between 1 and 50
    characters
    name_last:(<string>) - the last name of the user between 1 and 50
    characters

    Exceptions:
    InputError - Occurs when the email entered does not belong to any existing
    user in data_store
    InputError - Occurs when the password that is entered does not match
    to the corresponding email.

    Return Value:
    Returns 'auth_user_id'(<int>) and 'token'(<string>) on condition that both the email and password
    both are correct and correspond with the single user.
    '''
    #endregion

    # check if length of first name is between 1 and 50 characters
    if not check_name(name_first):
        raise InputError(description='length of name_first is not between 1 and 50 characters inclusive')

    # check if length of last name is between 1 and 50 characters
    if not check_name(name_last):
        raise InputError(description='length of name_last is not between 1 and 50 characters inclusive')

    # check if password is less than 6 characters
    if len(password) < 6:
        raise InputError(description='length of password is less than 6 characters')

    # check if email is valid
    if re.search('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$', email) is None:
        raise InputError(description='email entered is not a valid email')

    # check if email is already in use
    if not check_email_not_in_use(email):
            raise InputError(description='email address is already being used by another user')
    
    # figure out u_id
    store = data_store.get()
    users = store['users']
    u_id = len(users) + 1

    permission_id = 1 if len(users) == 0 else 2

    # create handle
    handle = create_handle(name_first, name_last, users)

    #profile_image default set
    img_name = "default.jpeg"
    profile_img_url = url_for("static", filename = img_name, _external = True)
    
    curr_time = datetime.now()   
    curr_timestamp = int(curr_time.timestamp())    
    if len(store['users']) == 0:
        store['channels_change'].append(curr_timestamp)
        store['DMs_change'].append(curr_timestamp)
        store['msg_change'].append(curr_timestamp)
        store['no_channels'].append(0)
        store['no_dms'].append(0)
        store['no_msg'].append(0)
    # create a user and append user to data store
    users.append({
        "u_id": u_id,
        "email": email,
        "password": hashlib.sha256(password.encode()).hexdigest(),
        "name_first": name_first,
        "name_last": name_last,
        "handle_str": handle,
        "permission_id": permission_id,
        "reset_code": "",
        'chs_time': [curr_timestamp],
        'dms_time': [curr_timestamp],
        'msg_time': [curr_timestamp],
        'msg_sent': [0],
        'ch_join': [0],
        'dm_join': [0],
        'no_ch': 0,
        'no_dm': 0,
        'no_msg': 0,
        'profile_img_url': profile_img_url,
        "notifications": []
    })

    token = gen_token(u_id)
    add_token(token)
    data_store.set(store)
    return {
        'token': token,
        'auth_user_id': u_id,
    }

def password_reset_request_v1(email):
    # check if user exists
    if check_email_not_in_use(email):
        return {}

    # log out of all current sessions
    store = data_store.get()
    users = store['users']

    reset_code = random_string()
    hash_code = hashlib.sha256(reset_code.encode()).hexdigest()

    tokens = store['tokens']
    for user in users:
        if user["email"] == email:
            u_id = user["u_id"]
            user['reset_code'] = hash_code
    tokens[:] = [token for token in tokens if decode_token(token)["u_id"] != u_id]

    data_store.set(store)

    # sending the email
    gmail_user = 'streamsunsw@gmail.com'
    gmail_password = 'Hello@2021'

    sent_from = gmail_user
    to = email
    subject = 'Password reset for your UNSW Streams account'
    body = 'You can reset your password using the following code:' + reset_code

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, email, subject, body)
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
    finally:
        return {}

def auth_password_reset_v1(reset_code, new_password):
    if len(new_password) < 6:
        raise InputError(description='length of password is less than 6 characters')

    encoded = hashlib.sha256(reset_code.encode()).hexdigest()
    store = data_store.get()
    found = False

    users = store['users']
    for user in users:
        if user["reset_code"] == encoded:
            found = True
            user["password"] = hashlib.sha256(new_password.encode()).hexdigest()
            user["reset_code"] = ""
    data_store.set(store)
    if not found:
        raise InputError(description='reset_code not correct')
    return {}

def create_handle(name_first, name_last, users):
    '''
    This function creates a handle for the user

    Arguments:
    name_first(<string>) - the first name of the user between 1 and 50
    characters
    name_last:(<string>) - the last name of the user between 1 and 50
    characters
    users:(<list>) - contains all the users in the datastore

    Exceptions:
    None

    Return Value:
    Returns handle_con(<string>)
    '''
    # handle created, first name, last name, -- concantenate both and last to loewercase
    handle = name_first.lower() + name_last.lower()

    #remove non-alphanumeric characters
    handle = re.sub(r'[^a-z0-9]', '', handle)

    if len(handle) > 20:
        handle = handle[:20]

    # check if handle is taken and if so concantenate a number
    #that is one increment of previously available
    num = 0
    handle_con = handle
    for user in users:
        if user['handle_str'] == handle_con:
            handle_con = handle + str(num)
            num += 1
    return handle_con

def random_string():
    result = ''.join(random.choice(string.ascii_letters) for i in range(10))
    return result
