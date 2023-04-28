# import pytest

# from src.channel import channel_messages_v1, channel_join_v1, channel_details_v1
# from src.auth import auth_login_v1, auth_register_v1
# from src.error import InputError, AccessError
# from src.channels import channels_create_v1
# from src.other import clear_v1

# @pytest.fixture
# def clear_and_register():

#     clear_v1()
#     auth_register_v1("me.person@email.com","password","Biggie","Smalls")

# def test_channel_messages_invalid_channel(clear_and_register):
    
#     auth_id = auth_login_v1("me.person@email.com","password")["auth_user_id"]

#     #Testing messages function interaction with invalid channel id, 11111
    
#     with pytest.raises(InputError):
#         channel_messages_v1(auth_id, 11111, 0)
        
# def test_channel_messages_start_greater(clear_and_register):

#     #Testing when messages function is called with a greater starting index than possible messages
  
#     #We set start at 10, as a newly created channel would have 0 messages and therefore create a scenario where start is greater than messages 
    
#     auth_id = auth_login_v1("me.person@email.com","password")["auth_user_id"]
#     channel_id = channels_create_v1(auth_id, "channel1", True)["channel_id"]
   
#     with pytest.raises(InputError):
#         channel_messages_v1(auth_id,channel_id,10)

# def test_channel_messages_not_a_member(clear_and_register):
    
#     #After clearing, authorising a user and create a channel we create a second user which will attempt to access the messages without being a member

#     auth_id = auth_login_v1("me.person@email.com","password")["auth_user_id"]
#     channel_id = channels_create_v1(auth_id, "channel1", True)["channel_id"]
#     auth_register_v1("not_member.person@email.com","1234568465","Not","Member")
#     auth_id2 = auth_login_v1("not_member.person@email.com","1234568465")["auth_user_id"]
    
#     with pytest.raises(AccessError):
#         channel_messages_v1(auth_id2, channel_id, 0)
        
# def test_invalid_auth_id(clear_and_register):
#     with pytest.raises(AccessError):
#         channels_create_v1(1111, "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1("", "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1("abc", "COMP1531", False)  
#     with pytest.raises(AccessError):
#         channels_create_v1(-5, "COMP1531", False)