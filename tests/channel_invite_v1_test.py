# import pytest
# from src.channel import channel_invite_v1, channel_details_v1
# from src.channels import channels_create_v1
# from src.auth import auth_register_v1, auth_login_v1
# from src.error import InputError, AccessError
# from src.other import clear_v1


# def test_invite_simple():
#     clear_v1()
#     # regitsed and log the auth user in
#     auth_register_v1("auth.person@gmail.com", "13254678", "Haden", "Smith")
#     auth_id = auth_login_v1("auth.person@gmail.com", "13254678")["auth_user_id"]
    
#     # create a new channel with the auth user
#     channel_id = channels_create_v1(auth_id, "channel1", True)["channel_id"]
    
#     # create a new user to be invited
#     auth_register_v1("invited.person@gmail.com", "87645231", "Jing", "Huang")
#     u_id = auth_login_v1("invited.person@gmail.com", "87645231")["auth_user_id"]
#     # call the channel_invite function
#     channel_invite_v1(auth_id, channel_id, u_id)

#     # test if the user has been invited into the "channel1"
#     name = channel_details_v1(auth_id, channel_id)["name"]
#     all_members = channel_details_v1(auth_id, channel_id)["all_members"]
#     assert name == "channel1"
#     is_invited = False
#     for member in all_members:
#         if member['u_id'] == u_id:
#             is_invited = True
#     # if is_invited is True, the user is successfully invited into the "channel1"
#     assert is_invited == True

# def test_invite_invalid_channel():
#     # create a channel with invalid channel_id, 55
#     # Inputerror
#     clear_v1()
   
#     auth_register_v1("new.auth@gmail.com", "HarryPotter", "Joanne", "Rowling")
#     auth_id = auth_login_v1("new.auth@gmail.com", "HarryPotter")["auth_user_id"]
   
#     auth_register_v1("new.invited@gmail.com", "JaneEyre", "Bessie", "Lee")
#     u_id = auth_login_v1("new.invited@gmail.com", "JaneEyre")["auth_user_id"]
    
#     with pytest.raises(InputError):
#         channel_invite_v1(auth_id, 55, u_id)

# def test_invite_invalid_uid():
#     # invite a user with invalid u_id, 55
#     # Inputerror
#     clear_v1()
   
#     auth_register_v1("new.auth@yahoo.com", "easypassword1", "Jasmin", "Wang")
#     auth_id = auth_login_v1("new.auth@yahoo.com", "easypassword1")["auth_user_id"]
   
#     channel_id = channels_create_v1(auth_id, "Channel2", True)["channel_id"]
    
#     with pytest.raises(InputError):
#         channel_invite_v1(auth_id, channel_id, 55)

# def test_invite_user_in_channel():
#     # invite a user who already is a in that channel
#     # Inputerror
#     clear_v1()
   
#     auth_register_v1("new.auth@qq.com", "easypassword1", "Jasmin", "Wang")
#     auth_id = auth_login_v1("new.auth@qq.com", "easypassword1")["auth_user_id"]
   
#     channel_id = channels_create_v1(auth_id, "Channel3", True)["channel_id"]
    
#     with pytest.raises(InputError):
#         channel_invite_v1(auth_id, channel_id, auth_id)

# def test_invite_invalid_authid():
#     # valid channel_id but auth user is not in that channel, auth_id is 55
#     # Accesserror
#     clear_v1()
   
#     auth_register_v1("new.auth@qq.com", "easypassword1", "Jasmin", "Wang")
#     auth_id = auth_login_v1("new.auth@qq.com", "easypassword1")["auth_user_id"]
    
#     auth_register_v1("new.invited@gmail.com", "JaneEyre", "Bessie", "Lee")
#     u_id = auth_login_v1("new.invited@gmail.com", "JaneEyre")["auth_user_id"]

#     channel_id = channels_create_v1(auth_id, "Channel4", True)["channel_id"]
    
#     with pytest.raises(AccessError):
#         channel_invite_v1(55, channel_id, u_id)


# #-----------------------------------------------------------------------------------#
