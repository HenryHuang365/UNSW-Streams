#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 01:22:23 2021

@author: caspar
"""
import jwt
from src.data_store import data_store

def gen_token(auth_user_id):
    '''
    Returns a token based on the uid and the time it is generated
    '''
    SECRET = 'COMP1531'
    
    encode_data = {
        'u_id': auth_user_id,
        }
    
    token = jwt.encode(encode_data, SECRET, algorithm ='HS256')
    
    return token


def decode_token(encoded_token):
    '''
    Decode the encoded_token using jwt
    '''
    SECRET = 'COMP1531'
    return jwt.decode(encoded_token, SECRET, algorithms ='HS256')
    
def add_token(token):
    '''
    Add token into data_store
    '''
    #Get token from the database
    store = data_store.get()
    tokens = store['tokens']
    
    #Add tokens
    tokens.append(token)

def check_valid_token(token):
    '''
    check if token is in the database
    '''
    #Get token from the database
    store = data_store.get()
    tokens = store['tokens']
    
    return token in tokens