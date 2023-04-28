from src.messages import message_send_v1
from src.error import InputError, AccessError
from src.data_store import data_store
from src.checks import check_user_in_channel, check_channel, user_is_stream_owner, user_is_channel_owner
from src.token_funcs import decode_token, check_valid_token
from datetime import timezone, datetime, timedelta
import time
import threading

def standup_start_v1(token, channel_id, length):
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')    
    auth_user_id = decode_token(token)['u_id']
    store = data_store.get()
    #check if channel_id is valid
    if not check_channel(channel_id):
        raise InputError(description = "Not a valid channel_id")
    if length < 0:
        raise InputError(description = "Length is a negative integer")
    # check if auth_user is in that channel
    if not check_user_in_channel(auth_user_id, channel_id):
        raise AccessError(description ="Authorised user is not a member of the channel")
    # error checking finished

    time_finish = None
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            if not channel["standup"]["status"]:
                channel["standup"]["status"] = True
                time_finish = int(datetime.now().timestamp()) + length
                channel["standup"]["time_finish"] = time_finish
            else:
                raise InputError(description = "Channel has an active standup running now")
    t = threading.Timer(length, stand_actual_send, (token, channel_id))
    t.start()
    return {"time_finish": time_finish}

def stand_actual_send(token, channel_id):
    store = data_store.get()
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            buffer_message = channel["standup"]["message_buffer"]
            for each_message in buffer_message:
                message_send_v1(token, channel_id, each_message)
    
    # deactive the standup 
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            channel["standup"]["status"] = False
            channel["standup"]["message_buffer"] = []
            channel["standup"]["time_finish"] = None
            
def standup_active_v1(token, channel_id):
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')    
    auth_user_id = decode_token(token)['u_id']
    store = data_store.get()
    #check if channel_id is valid
    if not check_channel(channel_id):
        raise InputError(description = "Not a valid channel_id")
    if not check_user_in_channel(auth_user_id, channel_id):
        raise AccessError(description ="Authorised user is not a member of the channel")
    # error checking finished
    is_active = False
    time_finish = None
    for channel in store["channels"]:
        if channel["channel_id"] == channel_id:
            is_active = channel["standup"]["status"]
            time_finish = channel["standup"]["time_finish"]
    
    return {"is_active": is_active, "time_finish": time_finish}

def standup_send_v1(token, channel_id, message):
    if not check_valid_token(token):
        raise AccessError(description ='Invalid Token')    
    auth_user_id = decode_token(token)['u_id']
    
    #check if channel_id is valid
    if not check_channel(channel_id):
        raise InputError(description = "Not a valid channel_id")
    
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description = 'Message cannot be less than 1 character or greater than 1000')

    is_active = standup_active_v1(token, channel_id)["is_active"]
    if not is_active:
        raise InputError(description = "Channel has no active standup running now")

    if not check_user_in_channel(auth_user_id, channel_id):
        raise AccessError(description ="Authorised user is not a member of the channel")
    # error checking finished
    store = data_store.get()
    channels = store["channels"]
    for channel in channels:
        if channel["channel_id"] == channel_id:
            channel["standup"]["message_buffer"].append(message)