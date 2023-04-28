# import pytest

# from src.channel import channel_join_v1, channel_details_v1
# from src.auth import auth_login_v1, auth_register_v1
# from src.error import InputError, AccessError
# from src.channels import channels_create_v1
# from src.other import clear_v1


# @pytest.fixture #Repeated action of clearing and  registering a user
# def clear_and_register():

#     clear_v1()
#     auth_register_v1("me.person@email.com","password","Biggie","Smalls")

# def test_channel_join_simple(clear_and_register): 
#     # Tests that join functions correctly

#     #Create an authorised user to create a channel
#     auth_id = auth_login_v1("me.person@email.com","password")["auth_user_id"]
    
#     #Create a channel
#     channel_id = channels_create_v1(auth_id, "channel1", True)["channel_id"]
    
#     # Create a user to join that channel
#     auth_id_2 = auth_register_v1("mewtwo.person@email.com","password","Mew","Two")['auth_user_id']
    
#     #Join the user to the channel
#     channel_join_v1(auth_id_2, channel_id)
    
#     #Make sure they are in the channel
#     name = channel_details_v1(auth_id, channel_id)["name"]
#     all_members = channel_details_v1(auth_id, channel_id)["all_members"]
#     assert name == "channel1"
#     has_joined = False
#     for member in all_members:
#         if member['u_id'] == auth_id_2:
#             has_joined = True
    
#     assert has_joined == True
    

# def test_channel_join_invalid_channel_id(clear_and_register): 
#     #Tests the interaction with an invalid channel id, 11111
#     auth_id = auth_login_v1("me.person@email.com","password")["auth_user_id"]
        
#     with pytest.raises(InputError):
#         channel_join_v1(auth_id, 11111)

# def test_channel_join_aleady_member(clear_and_register):
#     #Tests if the user who is attempting to join the channel is already in it
#     auth_id = auth_login_v1("me.person@email.com","password")["auth_user_id"]
#     channel_id = channels_create_v1(auth_id, "channel1", False)["channel_id"]
    
#     with pytest.raises(InputError):
#         channel_join_v1(auth_id,channel_id)

# def test_channel_join_non_global_user_private_channel(clear_and_register):
#     #Tests if the user is attempting to join a private channel not as a global owner
    
#     auth_id = auth_login_v1("me.person@email.com","password")["auth_user_id"]
#     auth_id_2 = auth_register_v1("mewtwo.person@email.com","password","Mew","Two")['auth_user_id']
#     channel_id = channels_create_v1(auth_id, "channel1", False)["channel_id"]
    
#     with pytest.raises(AccessError):
#         channel_join_v1(auth_id_2, channel_id)

# def test_channel_join_global_user_permission(clear_and_register):
    
#     auth_id = auth_login_v1("me.person@email.com","password")["auth_user_id"]
#     auth_id_2 = auth_register_v1("mewtwo.person@email.com","password","Mew","Two")['auth_user_id']
#     channel_id = channels_create_v1(auth_id_2, "channel1", False)["channel_id"]
    
#     channel_join_v1(auth_id, channel_id)

#     name = channel_details_v1(auth_id, channel_id)["name"]
#     all_members = channel_details_v1(auth_id, channel_id)["all_members"]
#     assert name == "channel1"
#     has_joined = False
#     for member in all_members:
#         if member['u_id'] == auth_id:
#             has_joined = True
    
#     assert has_joined == True

# def test_invalid_auth_id(clear_and_register):
#     with pytest.raises(AccessError):
#         channels_create_v1(11111111, "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1("", "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1("abc", "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1(-5, "COMP1531", False)
