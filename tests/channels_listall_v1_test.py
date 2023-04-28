# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Thu Sep 23 19:32:37 2021

# @author: caspar
# """

# import pytest


# from src.channels import channels_list_v1, channels_listall_v1, channels_create_v1
# from src.other import clear_v1
# from src.auth import auth_login_v1, auth_register_v1
# from src.data_store import data_store
# from src.channel import channel_invite_v1, channel_details_v1
# from src.error import InputError, AccessError


# @pytest.fixture()
# #preps before every test
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
#     #User with id=0 creates a new channel
#     channels_create_v1(1, 'test', True)
    
#     assert type(channels_listall_v1(1)) == dict

# '''
# Functionality test
# '''
# #If there is no channel created
# def test_empty(clear_and_register):
#     assert channels_listall_v1(1) == {'channels':[]}

# #Provide list of all channels (mixed with public and non-public)
# def test_all_lists(clear_and_register):
#     #Register new users
#     auth_id = auth_register_v1('b@abc.com', '123456', 'a', 'b')['auth_user_id']
    
#     #User with id=0 creates 2 new channels  
#     channels_create_v1(auth_id, 'test1', True)
#     channels_create_v1(auth_id, 'test2', False)

#     auth_id_2 = auth_register_v1('barack@abc.com', '123456', 'a', 'b')['auth_user_id']
#     #User with id=1 creates 2 new channels  
#     channels_create_v1(auth_id_2, 'test3', True)
#     channels_create_v1(auth_id_2, 'test4', False)
    

#     assert channels_listall_v1(auth_id) == {
#         'channels' : [
#             {
#               "channel_id": 1,
#               "name": "test1",
#               },
#             {
#               "channel_id": 2,
#               "name": "test2",
#               }, 
#             {
#               "channel_id": 3,
#               "name": "test3",
#               },
#             {
#               "channel_id": 4,
#               "name": "test4",
#               },             
#             ]
#         }   

# def test_invalid_auth_id(clear_and_register):
#     with pytest.raises(AccessError):
#         channels_list_v1(11111111)
#     with pytest.raises(AccessError):
#         channels_list_v1("")
#     with pytest.raises(AccessError):
#         channels_list_v1("abc")
#     with pytest.raises(AccessError):
#         channels_list_v1(-5)