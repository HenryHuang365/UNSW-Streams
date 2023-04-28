import sys
import signal
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from src.error import InputError
from src import config
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1, password_reset_request_v1, auth_password_reset_v1

from src.user import users_all_v1, user_stats_v1, users_stats_v1, user_profile_uploadphoto_v1, user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1, user_profile_sethandle_v1

from src.other import clear_v1
from src.dm import dm_create_v1, dm_list_v1, dm_messages_v1, dm_details_v1, dm_leave_v1, dm_remove_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.channel import channel_details_v2, channel_join_v2, channel_invite_v2, channel_messages_v2, channel_leave_v1
from src.admin_user import admin_user_remove_v1, admin_userpermission_change_v1
from src.channel_add_remove_owners import channel_addowner_v1, channel_removeowner_v1
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.messages import message_edit_v1, message_remove_v1, message_send_v1, message_senddm_v1, message_sendlater_v1, message_sendlaterdm_v1, message_share_v1, message_react_v1, message_unreact_v1, message_pin_v1, message_unpin_v1
from src.search import search_v1
from src.notifications import notifications_get_v1
import json
from src.data_store import data_store
import os.path




data = data_store.get()
with open(os.path.dirname(__file__) +'/../database.json','r', encoding='utf8') as FILE:
    json.load(FILE)
    data_store.set(data)  

      
def save():
    data = data_store.get()
    with open('database.json','w', encoding='utf8') as FILE:
        json.dump(data, FILE)
    
def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
# APP.debug = True
CORS(APP)
app = Flask(__name__, static_url_path='/static/')
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

### Clear
@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    clear_v1()
    save()
    return {}

@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

### Auth
@APP.route('/auth/login/v2', methods=["POST"])
def post_login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    save()
    return dumps(auth_login_v2(email, password))

@APP.route('/auth/register/v2', methods=["POST"])
def post_register():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    name_first = data["name_first"]
    name_last = data["name_last"]
    save()
    return dumps(auth_register_v2(email, password, name_first, name_last))

@APP.route('/auth/logout/v1', methods=["POST"])
def post_logout():
    data = request.get_json()
    token = data["token"]
    save()
    return dumps(auth_logout_v1(token))

@APP.route('/auth/passwordreset/request/v1', methods=["POST"])
def post_reset_request():
    data = request.get_json()
    email = data["email"]
    save()
    return dumps(password_reset_request_v1(email))

@APP.route('/auth/passwordreset/reset/v1', methods=["POST"])
def post_reset_password():
    data = request.get_json()
    reset_code = data["reset_code"]
    new_password = data["new_password"]
    save()
    return dumps(auth_password_reset_v1(reset_code, new_password))

# Users
@APP.route('/users/all/v1', methods=["GET"])
def get_users_all():
    token = request.args.get('token')
    return dumps(users_all_v1(token))

@APP.route('/user/profile/uploadphoto/v1', methods=["POST"])
def post_user_profile_uploadphoto():
    data = request.get_json()
    token = data["token"]
    img_url = data["img_url"]
    x_start = data["x_start"]
    x_end = data["x_end"]
    y_start = data["y_start"]
    y_end = data["y_end"]
    return dumps(user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end))

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('', path)

#workspace check
@APP.route('/users/stats/v1', methods=["GET"])
def get_users_stats():
    token = request.args.get('token')
    save()
    return dumps(users_stats_v1(token))

#user indiv stats 
@APP.route('/user/stats/v1', methods=["GET"])
def get_user_stats():
    token = request.args.get('token')
    save()
    return dumps(user_stats_v1(token))


@APP.route('/user/profile/v1', methods=["GET"])
def get_user_profile():
    token = request.args.get('token')
    u_id = int(request.args.get("u_id"))
    save()
    return dumps(user_profile_v1(token, u_id))

@APP.route('/user/profile/setname/v1', methods=["PUT"])
def put_profile_setname():
    data = request.get_json()
    token = data["token"]
    name_first = data["name_first"]
    name_last = data["name_last"]
    save()
    return dumps(user_profile_setname_v1(token, name_first, name_last))

@APP.route('/user/profile/setemail/v1', methods=["PUT"])
def put_profile_setemail():
    data = request.get_json()
    token = data["token"]
    email = data["email"]
    save()
    return dumps(user_profile_setemail_v1(token, email))

@APP.route('/user/profile/sethandle/v1', methods=["PUT"])
def put_profile_sethandle():
    data = request.get_json()
    token = data["token"]
    handle = data["handle_str"]
    save()
    return dumps(user_profile_sethandle_v1(token, handle))

### Channel
@APP.route("/channels/list/v2", methods=['GET'])
def get_channels_list():
    token = request.args.get('token')
    result = channels_list_v2(token)
    save()
    return dumps(result)

@APP.route("/channels/listall/v2",  methods=['GET'])
def get_channels_listall():
    token = request.args.get('token')
    save()
    return dumps(channels_listall_v2(token))
    
@APP.route("/channels/create/v2", methods=['POST'])
def post_channels_create():
    data = request.get_json()
    token = data['token']
    name = data['name']
    is_public = data['is_public']
    save()
    return dumps(channels_create_v2(token, name, is_public))

@APP.route("/channel/join/v2", methods=['POST'])
def post_channel_join():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    save()
    return dumps(channel_join_v2(token, channel_id))

@APP.route("/channel/leave/v1", methods=['POST'])
def post_channel_leave():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    save()
    return dumps(channel_leave_v1(token, channel_id))

@APP.route("/channel/messages/v2", methods=['GET'])
def get_channel_messages():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    save()
    return dumps(channel_messages_v2(token, channel_id, start))

@APP.route("/channel/details/v2",  methods=['GET'])
def get_channel_details():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    save()
    return dumps(channel_details_v2(token, channel_id))


@APP.route("/channel/invite/v2",  methods=['POST'])
def post_channel_invite():
    data = request.get_json()
    token = data["token"]
    channel_id = data["channel_id"]
    u_id = data["u_id"]
    save()
    return dumps(channel_invite_v2(token, channel_id,u_id))

@APP.route("/channel/removeowner/v1",  methods=['POST'])
def post_channel_removeowner():
    data = request.get_json()
    token = data["token"]
    channel_id = data["channel_id"]
    u_id = data["u_id"]
    save()
    return dumps(channel_removeowner_v1(token, channel_id, u_id))

@APP.route("/channel/addowner/v1",  methods=['POST'])
def post_channel_addowner():
    data = request.get_json()
    token = data["token"]
    channel_id = data["channel_id"]
    u_id = data["u_id"]
    save()
    return dumps(channel_addowner_v1(token, channel_id, u_id))

@APP.route("/dm/create/v1", methods=['POST'])
def post_dm_create():
    data = request.get_json()
    token = data['token']
    u_ids = data['u_ids']
    save()
    return dumps(dm_create_v1(token, u_ids))

@APP.route("/dm/list/v1", methods=['GET'])
def get_dm_list():
    token = request.args.get('token')
    save()
    return dumps(dm_list_v1(token))

@APP.route("/dm/messages/v1", methods=['GET'])
def get_dm_messages():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    save()
    return dumps(dm_messages_v1(token, dm_id, start))

@APP.route("/dm/remove/v1", methods=['DELETE'])
def delete_dm_remove():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    save()
    return dumps(dm_remove_v1(token, dm_id))

@APP.route("/dm/details/v1", methods=['GET'])
def get_dm_details():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    save()
    return dumps(dm_details_v1(token, dm_id))

@APP.route("/dm/leave/v1", methods=['POST'])
def post_dm_leave():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    save()
    return dumps(dm_leave_v1(token, dm_id))

@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def delete_admin_user_remove():
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
    save()
    return dumps(admin_user_remove_v1(token, u_id))

@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def post_admin_userpermission_change():
    data = request.get_json()
    token = data['token']
    u_id = data['u_id']
    permission_id = data['permission_id']
    save()
    return dumps(admin_userpermission_change_v1(token, u_id, permission_id))

# Message
@APP.route("/message/send/v1", methods=['POST'])
def post_message_send():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    save()
    return dumps(message_send_v1(token, channel_id, message))
    
@APP.route("/message/edit/v1", methods=['PUT'])
def put_message_edit():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    message = data['message']
    save()
    return dumps(message_edit_v1(token, message_id, message))

@APP.route("/message/remove/v1", methods=['DELETE'])
def delete_message_remove():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    save()
    return dumps(message_remove_v1(token, message_id))

@APP.route("/message/senddm/v1", methods=['POST'])
def post_message_senddm():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    message = data['message']
    save()
    return dumps(message_senddm_v1(token, dm_id, message))

@APP.route("/message/sendlater/v1", methods=['POST'])
def post_message_sendlater():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    time_sent = data['time_sent']
    save()
    return dumps(message_sendlater_v1(token, channel_id, message, time_sent))

@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def post_message_sendlaterdm():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    message = data['message']
    time_sent = data['time_sent']
    save()
    return dumps(message_sendlaterdm_v1(token, dm_id, message, time_sent))

@APP.route("/message/react/v1", methods=['POST'])
def post_message_react():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react = data['react_id']
    save()
    return dumps(message_react_v1(token, message_id, react))

@APP.route("/message/unreact/v1", methods=['POST'])
def post_message_unreact():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    react = data['react_id']
    save()
    return dumps(message_unreact_v1(token, message_id, react))

@APP.route("/message/pin/v1", methods=['POST'])
def post_message_pin():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    save()
    return dumps(message_pin_v1(token, message_id))

@APP.route("/message/unpin/v1", methods=['POST'])
def post_message_unpin():
    data = request.get_json()
    token = data['token']
    message_id = data['message_id']
    save()
    return dumps(message_unpin_v1(token, message_id))

@APP.route("/message/share/v1", methods=['POST'])
def post_message_share():
    data = request.get_json()
    token = data['token']
    og_message_id = data['og_message_id']
    message = data['message']
    channel_id = data['channel_id']
    dm_id = data['dm_id']
    save()
    return dumps(message_share_v1(token, og_message_id, message, channel_id, dm_id))

@APP.route("/standup/start/v1", methods=['POST'])
def post_standup_start():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    length = data["length"]
    save()
    return dumps(standup_start_v1(token, channel_id, length))

@APP.route("/standup/active/v1", methods=['GET'])
def get_standup_active():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    save()
    return dumps(standup_active_v1(token, channel_id))

@APP.route("/standup/send/v1", methods=['POST'])
def post_standup_send():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data["message"]
    save()
    return dumps(standup_send_v1(token, channel_id, message))

@APP.route("/search/v1", methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    save()
    return dumps(search_v1(token,query_str))

@APP.route("/notifications/get/v1", methods=['GET'])
def notifications():
    token = request.args.get('token')
    save()
    return dumps(notifications_get_v1(token))

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(threaded = True, port=config.port) # Do not edit this port
    app.run()
    
    data = data_store.get()
    with open(os.path.dirname(__file__) +'/../database.json','r', encoding='utf8') as FILE:
        json.load(FILE)
        data_store.set(data)  