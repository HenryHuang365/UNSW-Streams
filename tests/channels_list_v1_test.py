# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Wed Sep 22 01:14:04 2021

# @author: caspar
# """

# import pytest
# import re


# from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
# from src.other import clear_v1
# from src.auth import auth_login_v1, auth_register_v1
# from src.data_store import data_store
# from src.channel import channel_invite_v1, channel_details_v1
# from src.error import InputError, AccessError


# @pytest.fixture()
# #preparation for every tests
# def clear_and_register():
#     #Clear and create user for temporary database
#     clear_v1()
#     auth_register_v1('a@abc.com', '123456', 'a', 'b')



# #Test Access Error
# def test_auth_id_invalid():
#     with pytest.raises(AccessError):
#         assert channels_list_v1("abc")


# '''
# Type test
# '''
# #test whether the return type is a dictionary
# def test_type_match(clear_and_register):
#     #User with id=1 creates a new channel
#     channels_create_v1(1, 'test', True)
    
#     assert type(channels_list_v1(1)) == dict

# '''
# Functionality test
# '''
# #The user is not a member in any channel
# def test_not_in_channel(clear_and_register):
#     #Register new users
#     auth_register_v1('b@abc.com', '123456', 'c', 'd')

#     #User with id=2 creates a new channel
#     channels_create_v1(2, 'test2', True)
    
#     assert channels_list_v1(1) == {'channels':[]}



# #To see if the user is the authenticor ated user
# #and gives the corresponding channel list
# def test_match_channels(clear_and_register):
#     #Set up a temporary database
#     #Register new users
#     auth_id = auth_register_v1('b@abc.com', '123456', 'c', 'd')['auth_user_id']
#     auth_id_2 = auth_register_v1('barack@abc.com', '123456', 'c', 'd')['auth_user_id']

#     #User with id=0 creates a new channel
#     channel_id = channels_create_v1(auth_id, 'test1', True)['channel_id']
    
#     #User with id=1 creates a new channel
#     channels_create_v1(auth_id_2, 'test2', True)
        
#     assert channels_list_v1(auth_id) == {
#         'channels' : [
#             {
#               "channel_id": channel_id,
#               "name": "test1",
#               }
#             ]
#         }

# #The user is a member in 2 channels
# def test_2_channels(clear_and_register):
#     #User with id=0 creates 2 new channels  
#     auth_id = auth_register_v1('b@abc.com', '123456', 'c', 'd')['auth_user_id']
#     channels_create_v1(auth_id, 'test1', False)
#     channels_create_v1(auth_id, 'test2', True)

#     assert channels_list_v1(auth_id) == {
#         'channels' : [
#             {
#               "channel_id": 1,
#               "name": "test1",
#               },
#             {
#               "channel_id": 2,
#               "name": "test2",
#               }, 
#             ]
#         }
    
# def test_invalid_auth_id(clear_and_register):
#     with pytest.raises(AccessError):
#         channels_list_v1(1111111)
#     with pytest.raises(AccessError):
#         channels_list_v1("")
#     with pytest.raises(AccessError):
#         channels_list_v1("abc")
#     with pytest.raises(AccessError):
#         channels_list_v1(-5)