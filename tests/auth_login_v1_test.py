# import pytest

# from src.auth import auth_login_v1
# from src.auth import auth_register_v1
# from src.error import InputError
# from src.other import clear_v1

# # test should return InputError email entered does not belong to user
# def test_email_use():
#     clear_v1
#    # emails that have not been previously registered
#     with pytest.raises(InputError):
#         assert auth_login_v1("apple@gmail.com", "password")
#     with pytest.raises(InputError):
#         assert auth_login_v1("cat@gmail.com", "password")
    

# # test should return InputError if password does not belong to user
# def test_password():
#     clear_v1
#     auth_register_v1("bat@gmail.com", "Hello@2021", "name_first", "name_last")
#     with pytest.raises(InputError):
#         assert auth_login_v1("bat@gmail.com", "password")
#     with pytest.raises(InputError):
#         assert auth_login_v1("bat@gmail.com", "Hello@2020")
#     with pytest.raises(InputError):
#         assert auth_login_v1("bat@gmail.com", "WhySoSerious")

# # test that right user id is returned with successful log in
# def test_u_id():
#     clear_v1
#     # create user and extract the u_id of said user
#     auth = auth_register_v1("cat@gmail.com", "Hello@2021", "name_first", "name_last")
#     # check that you were able to find the same user
#     assert auth_login_v1("cat@gmail.com", "Hello@2021") == auth
#     auth2 = auth_register_v1("dog@gmail.com", "new@2021", "name_first", "name_last")
#     assert auth_login_v1("dog@gmail.com", "new@2021") == auth2
    
