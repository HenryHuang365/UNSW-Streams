#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 2021

@author: mahek
"""
from src.error import AccessError
from src.data_store import data_store
from src.token_funcs import decode_token, check_valid_token

def notifications_get_v1(token):

    store = data_store.get()
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')
    
    auth_user_id = decode_token(token)['u_id']
    users = store['users']
    notifications = users[auth_user_id-1]["notifications"]
    notifications.reverse()
    return {
        "notifications": notifications[:20]
    }
