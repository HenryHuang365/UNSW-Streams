# Assumptions (Iteration 1)

Submitted for Marking | Assumption No. | Impacted features | Assumption detail
----------------------|----------------| ------------------|------------------
NO | 1 | General | All the inputs and outputs are in the same types as provided in the project specifications
NO | 2 | data_store.py | The database contains the information as in the documentation (see data_store)
YES | 3 | auth_register.py | The first name and last name is allowed to be non-alphanumeric (e.g. first name = #$#@, last name = !@$@). However the first name + Last name will not be entirely non-alphanumeric (e.g. as least one character in first name +last name will be alphanumeric)
YES | 4 | channels_create_v1.py | It is assumed that channel ids will not be randomly assigned for any new channels created. Therefore, channel ids are to be assigned by adding one to the existing number of channels after confirming that a pre-existing channel is not currently using the intended channel id
YES | 5 | channels_create_v1.py | It is assumed that an own_member will also be added to the all members list once a channel has been created. All other functions which dependent on and utilise owner_members and all members will follow the same guidelines whereby an owner member should be displayed under all members but will retain a different permission set
YES | 6 | channels_list.py | The returned list contains the channels that the user is a part of and the associated details (except messages)
YES | 7 | channels_listall.py | The returned list contains all the channels and the associated details (except messages)
YES | 8 | channel_messages_v1.py | For iteration 1 the function will always raise an error as there is no ability to add messages, therefore any start value used in calling messages will be greater than the amount of messages

# Assumptions (Iteration 2)

Submitted for Marking | Assumption No. | Impacted features | Assumption detail
----------------------|----------------| ------------------|------------------
YES | 1 | channel_removeowner | Once a channel owner is removed from the owner members list they will still remain in the channel members list until the admin removes them from streams or they leave the channel
YES | 2 | channel_addowner and channel_join | When a global owner joins a channel they will be listed within all members however they will retain the channel permission id = 1 which indicates that they have the same permissions as that of a channel owner. Additionally, when a global owner is added as a channel owner there will be no changes to their channel permission id as it will remain as 1 but they will be added to the owner members list of that channel