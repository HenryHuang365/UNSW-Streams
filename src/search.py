#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:18:29 2021

@author: caspar
"""
from src.error import InputError, AccessError
from src.data_store import data_store
from src.token_funcs import decode_token, check_valid_token



def search_v1(token, query_str):
    
    store = data_store.get()    
    #Check if token is in the daabased
    if check_valid_token(token) == False:
        raise AccessError(description ="The Token is invalid")    
        
    # Check the length of query string
    if len(query_str) > 1000 or len(query_str) < 1:
        raise InputError('Message cannot be less than 1 character or greater than 1000')
    
    msg_list = []
        
    auth_id = decode_token(token)['u_id']
    
    channels = store['channels']
    dms = store['DMs']
    
    #For msg in channels
    for ch in channels:
        for member in ch['all_members']:
            if member['u_id'] == auth_id:
                for msg in ch['messages']:
                    if query_str in msg['message']:
                        msg_list.append(msg)
    
    for dm in dms:
        for member in dm['members']:
            if member['u_id'] == auth_id:
                for msg in dm['messages']:
                    if query_str in msg['message']:
                        msg_list.append(msg)
                        
    data_store.set(store)   
    
    return {'messages': msg_list}