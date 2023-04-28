# import pytest
# from src.channel import channel_invite_v1, channel_details_v1
# from src.channels import channels_create_v1
# from src.auth import auth_register_v1, auth_login_v1
# from src.error import InputError, AccessError
# from src.other import clear_v1

# @pytest.fixture
# def clear_and_register():
    
#     clear_v1()
#     auth_register_v1("auth.person@gmail.com", "13254678", "Haden", "Smith")


# def test_details_simple(clear_and_register):
#     # tests if channel_details works properly 

#     auth_id = auth_login_v1("auth.person@gmail.com", "13254678")["auth_user_id"]
    
#     # create a new channel with the auth user
#     channel_id = channels_create_v1(auth_id, "channel1", True)["channel_id"]
    
#     # create a new user to be invited
#     auth_register_v1("invited.person@gmail.com", "87645231", "Jing", "Huang")
#     u_id = auth_login_v1("invited.person@gmail.com", "87645231")["auth_user_id"]
#     # call the channel_invite function
#     channel_invite_v1(auth_id, channel_id, u_id)
#     # upon this point the channel has an auth_user and a new-invited member

#     name = channel_details_v1(auth_id, channel_id)["name"]
#     is_public = channel_details_v1(auth_id, channel_id)["is_public"]
#     owner_members = channel_details_v1(auth_id, channel_id)["owner_members"]
#     all_members = channel_details_v1(auth_id, channel_id)["all_members"]
    
#     assert name == 'channel1'
#     assert is_public == True
#     assert auth_id == owner_members[0]["u_id"]
#     assert auth_id == all_members[0]["u_id"]
#     assert u_id == all_members[1]["u_id"]



# def test_details_invalid_channel(clear_and_register):
#     # call channel_details with an invalid channel_id
#     # InputError
    
#     auth_id = auth_login_v1("auth.person@gmail.com", "13254678")["auth_user_id"]
    

#     with pytest.raises(InputError):
#         channel_details_v1(auth_id, 55)["name"]
#         # owner_members = channel_details_v1(auth_id, 55)["owners"]
#         # all_members = channel_details_v1(auth_id, 55)["all_members"]

# def test_details_invalid_auth(clear_and_register):
#     # call channel_details with an invalid auth_id
#     # AccessError
    
#     auth_id = auth_login_v1("auth.person@gmail.com", "13254678")["auth_user_id"]
    
#     channel_id = channels_create_v1(auth_id, "channel2", True)["channel_id"]

#     with pytest.raises(AccessError):
#         # name = channel_details_v1(55, channel_id)["name"]
#         channel_details_v1(55, channel_id)["owner_members"]
#         # all_members = channel_details_v1(auth_id, 55)["all_members"]

# def test_invalid_auth_id(clear_and_register):
#     with pytest.raises(AccessError):
#         channels_create_v1(1111, "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1("", "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1("abc", "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1(-5, "COMP1531", False)
