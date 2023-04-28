# import pytest

# from src.auth import auth_register_v1
# from src.error import InputError
# from src.data_store import data_store
# from src.other import clear_v1
# from src.channels import channels_create_v1

# # test should return InputError if password is less than 6 characters in length
# def test_password_length():
#     clear_v1
#     with pytest.raises(InputError):
#         assert auth_register_v1("a@a.com", "", "name_first", "name_last")
#     with pytest.raises(InputError):
#         assert auth_register_v1("a@a.com", "apple", "name_first", "name_last")
#     assert type(auth_register_v1("a@a.com", "password", "name_first", "name_last")) == dict
    

# # test should return InputError if first name is less than 1 or greater than 50
# def test_firstname_length():
#     clear_v1
#     with pytest.raises(InputError):
#         assert auth_register_v1("b@b.com", "password", "", "name_last")
#     with pytest.raises(InputError):
#         assert auth_register_v1("b@b.com", "password", "a"*51, "name_last")
#     assert type(auth_register_v1("b@b.com", "password", "a*50", "name_last")) == dict

# # test should return InputError if last name name is less than 1 or greater than 50
# def test_lastname_length():
#     clear_v1
#     with pytest.raises(InputError):
#         assert auth_register_v1("c@c.com", "password", "name_first", "")
#     with pytest.raises(InputError):
#         assert auth_register_v1("c@c.com", "password", "name_first", "a"*51)
#     assert type(auth_register_v1("c@c.com", "password", "name_first", "a"*49)) == dict

# # test should return InputError if email is valid string and 
# # should match this regex '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
# def test_email_regex():
#     clear_v1
#     # test when there is no expression ahead of @
#     with pytest.raises(InputError):
#         assert auth_register_v1("@a.com", "password", "name_first", "name_last")
#     # test when there is no expression between @ and .
#     with pytest.raises(InputError):
#         assert auth_register_v1("apple@.co", "password", "name_first", "name_last")
#     # test when there is no @
#     with pytest.raises(InputError):
#         assert auth_register_v1("applegmail.com", "password", "name_first", "name_last")
#     # test when there is less than 2 characters after .
#     with pytest.raises(InputError):
#         assert auth_register_v1("apple@gmail.c", "password", "name_first", "name_last")
#     # test when there is a number after .
#     with pytest.raises(InputError):
#         assert auth_register_v1("apple@gmail.com3", "password", "name_first", "name_last")
#     # check that it works with correct details
#     assert type(auth_register_v1("apple@gmail.com", "password", "name_first", "name_last")) == dict

# # test should return InputError if email is already in use.
# def test_email_valid():
#     clear_v1
#     # will first register a user and get an int return showing that the user was created
#     assert type(auth_register_v1("peach@gmail.com", "password", "name_first", "name_last")) == dict
#     # try to create another user with the same email address i should get input error
#     with pytest.raises(InputError):
#         assert auth_register_v1("peach@gmail.com", "password", "new_name_first", "new_name_last")
#     # will create another user
#     assert type(auth_register_v1("pear@gmail.com", "password", "name_first2", "name_last2")) == dict
#     with pytest.raises(InputError):
#         assert auth_register_v1("pear@gmail.com", "password", "new_name_first2", "new_name_last2")

# def test_correct_details():
#     clear_v1
#     assert type(auth_register_v1("correct@gmail.com", "password", "name_first", "name_last")) == dict
#     assert type(auth_register_v1("correct1@gmail.com", "password", "name_first", "name_last")) == dict
    
# def test_handle_20_characters():
#     clear_v1()
#     data = data_store.get()
#     #cut off at 20 characters
#     auth_register_v1('a@abc.com', 'caspar', 'caspar12345678901', 'Chan') 
    
#     assert data['users'][0]['handle'] == 'caspar12345678901cha'

# def test_handle_non_alphanumeric_and_all_lower_case():
#     clear_v1()
#     data = data_store.get()
#     #remove @ and , and change Capial into lower cases
#     auth_register_v1('a@abc.com', 'caspar', 'c@spar1234567890,', 'Chan')     
#     assert data['users'][0]['handle'] == 'cspar1234567890chan'
# def test_handle_samehandle():
#     #add a 0 if handle was taken
#     clear_v1()
#     data = data_store.get()  
    
#     #handle shd add from 0 
#     auth_register_v1('a@abc.com', 'caspar', 'caspar1234567890', 'Chan') 
#     auth_register_v1('b@abc.com', 'caspar', 'caspar1234567890', 'Chan') 
#     auth_register_v1('c@abc.com', 'caspar', 'caspar1234567890', 'Chan') 
    
#     assert data['users'][0]['handle'] == 'caspar1234567890chan'
#     assert data['users'][1]['handle'] == 'caspar1234567890chan0'
#     assert data['users'][2]['handle'] == 'caspar1234567890chan1'