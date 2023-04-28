#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 01:39:26 2021

@author: caspar
"""
from src import dm
from src.admin_user import admin_user_remove_v1, admin_userpermission_change_v1
from src.auth import auth_login_v2, auth_register_v2
from src.channel import channel_details_v2, channel_invite_v2, \
channel_is_public, channel_join_v2, channel_messages_v2
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.notifications import notifications_get_v1
from src.other import clear_v1
from src.checks import check_channel, check_user_exists, check_user_in_channel
from src.data_store import data_store
from src.error import InputError, AccessError
from src.token_funcs import gen_token, add_token, decode_token, check_valid_token
from src.dm import dm_create_v1, dm_list_v1, dm_messages_v1, dm_details_v1, dm_leave_v1
from src.user import user_profile_setemail_v1, user_profile_sethandle_v1, user_profile_setname_v1, user_profile_v1
from src.messages import message_send_v1, message_senddm_v1, message_edit_v1, message_remove_v1, message_sendlater_v1, message_sendlaterdm_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1
from src.channel_add_remove_owners import channel_addowner_v1, channel_removeowner_v1
from datetime import timezone, datetime, timedelta
from src.search import search_v1
data= data_store.get()

"""
Create users and channels
"""
clear_v1()

a = auth_register_v2('a@abc.com', '123456123', 'sheriff', 'woody')
b = auth_register_v2('ab@abc.com', '123456123', 'buzz', 'lightyear')
c = auth_register_v2('acb@abc.com', '123456123', 'daspar', 'chan')

a_token = a['token']
b_token = b['token']
c_token = c['token']

a_id = a['auth_user_id']
b_id = b['auth_user_id']
c_id = c['auth_user_id']

ch_id = channels_create_v2(a_token, 'new', True)['channel_id']
#message_send_v1(a_token, ch_id, "@sheriffwoody how are you doing")
#channel_invite_v2(a_token, ch_id, b_id)
#m_id = message_send_v1(b_token, ch_id, "sup my man see you there @buzzlightyear")["message_id"]
#dm_id = dm_create_v1(c_token, [b_id, a_id])["dm_id"]
#message_senddm_v1(c_token, dm_id, "@buzzlightyear this is a dms")
#notifications = notifications_get_v1(b_token)
#print("hello there")
#print(notifications)
channel_invite_v2(a_token, ch_id, b_id)

# dm_id = dm_create_v1(a_token, [])['dm_id']


msg_id = message_send_v1(a_token, ch_id, 'asdadas')['message_id']

msg_id = message_send_v1(a_token, ch_id, 'asdadas')['message_id']
msg_id = message_send_v1(a_token, ch_id, 'asdadas')['message_id']
msg_id = message_send_v1(a_token, ch_id, 'asdadas')['message_id']

msg_list = channel_messages_v2(a_token, ch_id, 0)

# message_send_v1(a_token, ch_id, 'asdadaasdasdasds')
# message_send_v1(a_token, ch_id, 'asdadasdasddddddddddddddddddddddddas')

# message_send_v1(b_token, ch_id, 'asdadasdasddddddddddddddddddddddddas')
# message_send_v1(b_token, ch_id, 'asdadasdasddddddddddddddddddddddddas')

#message_senddm_v1(a_token, dm_id, '12313123')
# message_senddm_v1(a_token, dm_id, '1asd123')
message_react_v1(a_token,msg_id, 1)
message_react_v1(b_token,msg_id, 1)

# msg_list = search_v1(b_token, 'asd')

# curr_time = datetime.now()
# time_sent_before = datetime.now() + timedelta(seconds = 10)
# round_time = round(curr_time.timestamp())
# time_sent = round(time_sent_before.timestamp())


# #message_sendlaterdm_v1(a_token, dm_id, 'asdasd', time_sent)
# message_sendlater_v1(a_token, ch_id, 'asdasd', time_sent)

message_pin_v1(a_token, msg_id)

msgs = channel_messages_v2(a_token, ch_id, 0)
#message_unreact_v1(a_token,msg_id, 1)
message_unpin_v1(a_token,msg_id)
msgs_2 = channel_messages_v2(a_token, ch_id, 0)
#message_unreact_v1(a_token,msg_id_2, 1)
#msgs_3 = channel_messages_v2(a_token, ch_id, 0)
#message_unreact_v1(a_token,msg_id_3, 1)
#msgs_4 = channel_messages_v2(a_token, ch_id, 0)

#message_pin_v1(a_token, msg_id)
#
#msgs_2 = channel_messages_v2(a_token, ch_id, 0)
#
#
#msgs_3 = channel_messages_v2(a_token, ch_id, 0)