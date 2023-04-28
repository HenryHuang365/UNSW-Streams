# """
# Author: Shagun Panwar
# zID: 5165416

# """
# import pytest

# from src.channels import channels_create_v1
# from src.error import AccessError, InputError
# from src.data_store import data_store
# from src.other import clear_v1
# from src.auth import auth_register_v1


# '''
# 1- check the name of the channel created - length
# 2 - check owner = creater of channel
# 3 - test to see if the creator has joined the channel
# 4 - check public / private values
# 5 - check the type of the channel id
# 6 - check that the channel id is unique
# '''
# @pytest.fixture()
# #preps before every test
# def clear_and_register():
#     #Clear and create user for temporary database
#     clear_v1()
#     auth_id = auth_register_v1('a@abc.com', '123456', 'a', 'b')
#     return auth_id

# # Test1: tests if the length of name is less than 1 or more than 20 characters and raises an Input error
# # assumption - spaces and special characters can be included in the channel name
# def test_channel_name(clear_and_register):
#     auth_id = clear_and_register["auth_user_id"]
#     with pytest.raises(InputError):
#         assert channels_create_v1(auth_id, "", True)
#     with pytest.raises(InputError):
#         assert channels_create_v1(auth_id, "Fundamentals of SEngg", True) 
    
# # Test2: test to check that the channel creator is a channel owner
# def test_channel_creator(clear_and_register):
#     auth_id = clear_and_register["auth_user_id"]
#     return_value = channels_create_v1(auth_id, "COMP1531", False)  
#     for channel in data_store.get()["channels"]: 
#         if channel["channel_id"] == return_value["channel_id"]:
#             assert channel["owner_members"] == [auth_id]


# # Test3: test to check that the channel creator has automatically joined the channel
# def test_channel_creator_join(clear_and_register):
#     auth_id = clear_and_register["auth_user_id"]
#     return_value = channels_create_v1(auth_id, "COMP1531", False)  
#     for channel in data_store.get()["channels"]:
#         if channel["channel_id"] == return_value["channel_id"]:
#             assert channel["all_members"][0]["u_id"] == auth_id

# # Test4: test to check that the channel status is listed as either public or private
# def test_channel_status(clear_and_register):
#     # check that the default value for is_public changes within the function 
#     auth_id = clear_and_register["auth_user_id"]
#     return_value = channels_create_v1(auth_id, "COMP1531", True)  
#     for channel in data_store.get()["channels"]:
#         if channel["channel_id"] == return_value["channel_id"]:
#             assert channel["is_public"] == True

# # Test5: test that the type of the channel ID after creation
# def test_channel_id_type(clear_and_register):
#     auth_id = clear_and_register["auth_user_id"]
#     return_value = channels_create_v1(auth_id, "COMP1531", True)  
#     assert type(return_value) is dict
#     assert type(return_value["channel_id"]) is int

# # Test6: test that the channel ID is unique and not duplicate
# def test_unique_channel_id(clear_and_register):
#     auth_id = clear_and_register["auth_user_id"]
#     return_value = channels_create_v1(auth_id, "COMP1531", True)  
#     for channel in data_store.get()["channels"]:
#         if channel["channel_id"] == return_value["channel_id"]:
#             assert channel["channel_id"] == len(data_store.get()["channels"]) 

# # Test7: test that the channel_permission_id is set to one for the creator's u_id
# def test_creator_channel_permission(clear_and_register):
#     auth_id = clear_and_register["auth_user_id"]
#     channel_id = channels_create_v1(auth_id, "COMP1531", False)
#     print(channel_id)
#     channels = data_store.get()["channels"]
#     for channel in channels:
#         if channel["channel_id"] == channel_id:
#             assert channel["all_members"] == [{
#                 "u_id": auth_id,
#                 "channel_permission_id": 1
#             }]

# def test_invalid_auth_id(clear_and_register):
#     with pytest.raises(AccessError):
#         channels_create_v1(1111, "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1("", "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1("abc", "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1(-5, "COMP1531", False)