'''
Documentation
# [...] = a list of

'users' contains

"u_id" = int
"email" = string
"password" = string
"name_first" = string
"name_last"  = string
"handle" = string
"permission_id" = int

'channels' contains

"channel_id" = int
"name" = string
"owner_members" = [int]
"all_members" = [dict{
    "u_id" = int,
    "channel_permission_id" = int
}],
"is_public": Boolean
"messages" = [dict{
    "message_id" = int,
    "u_id" = int,
    "message" = string,
    "time_created" = string
}]

"DMs" contains
    
"dm_id" = int
"creator_id" = int
"name" = str
"members": members (dict of user),
"messages" = [dict{
    "message_id" = int,
    "u_id" = int,
    "message" = string,
    "time_created" = string
    "reacts" = [dict{
    "react_id" = int,
    "u_ids" = ["u_id" = int]
    "is_this_user_reacted" = boolean
    }]
    "is_pinned" = boolean
    

}]
'''

import json
import os
import threading

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    "channels": [],
    "DMs": [],
    'tokens': [],
    'm_id_create': 0,
    'channels_change': [],
    'no_channels': [],
    'DMs_change': [],
    'no_dms':[],
    'msg_change': [],
    'no_msg':[],
    'total_no_msg': 0,
    'total_no_chs': 0,
    'total_no_dms': 0
}


## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    '''
    global variable
    '''
    def __init__(self):
        self.__store = initial_object

    def get(self):
        '''
        get the global vairable
        '''        
        return self.__store

    def set(self, store):
        '''
        Check if the global variable stored is a dictionary
        '''
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store


print('Loading Datastore...')

    
global data_store
data_store = Datastore()