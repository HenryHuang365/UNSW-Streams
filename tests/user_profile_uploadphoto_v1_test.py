"""
Author: Shagun Panwar
zID: 5165416
"""
from requests.models import Response
import pytest
import requests
import json
from PIL import Image
from src import config

BASE_URL = config.url

@pytest.fixture
def clear_and_register():
    requests.delete(BASE_URL + "clear/v1")

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "cat@gmail.com",
        "password": "LetsGO!",
        "name_first": "name_first",
        "name_last": "name_last"
    })

    response_login = requests.post(BASE_URL + "auth/login/v2",json={
        "email": "cat@gmail.com",
        "password": "LetsGO!"
    })

    token = response_login.json()["token"]
    # auth_user_id = response_login.json()["auth_user_id"]
    
    return token


# input error raised when img_url returns an HTTP status other than 200
def test_invalid_status_code(clear_and_register):
    token = clear_and_register

    response_user_uploadphoto = requests.post(BASE_URL + "/user/profile/uploadphoto/v1",json ={
        "token": token,
        "img_url": "http://www.cse.unsw.edu.au/~richardb/index_files/RicjhytvijkhnvbhghsxdfghjhardBuckland-200.jpg",
        "x_start": 0, 
        "y_start": 0, 
        "x_end": 100, 
        "y_end": 100
    })
    assert response_user_uploadphoto.status_code == 400

# input error raised when any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL
def test_invalid_image_bounds(clear_and_register):
    token = clear_and_register
    response_user_uploadphoto = requests.post(BASE_URL + "/user/profile/uploadphoto/v1",json ={
        "token": token,
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": 300, 
        "y_start": 300, 
        "x_end": 500, 
        "y_end": 500
    })
    assert response_user_uploadphoto.status_code == 400



# input error raised when x_end is less than x_start or y_end is less than y_start
def test_dimension_overshoot(clear_and_register):
    token = clear_and_register
    response_user_uploadphoto = requests.post(BASE_URL + "/user/profile/uploadphoto/v1",json ={
        "token": token,
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": 150, 
        "y_start": 150, 
        "x_end": 100, 
        "y_end": 100
    })
    assert response_user_uploadphoto.status_code == 400

# input error raised when image uploaded is not a JPG
def test_not_jpeg(clear_and_register):
    token = clear_and_register
    response_user_uploadphoto = requests.post(BASE_URL + "/user/profile/uploadphoto/v1",json ={
        "token": token,
        "img_url": "http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png",
        "x_start": 0, 
        "y_start": 0, 
        "x_end": 100, 
        "y_end": 100
    })
    assert response_user_uploadphoto.status_code == 400

# success case
def test_success(clear_and_register):
    token = clear_and_register

    requests.post(BASE_URL + "auth/register/v2",json={
        "email": "dogs@gmail.com",
        "password": "LetsGO!",
        "name_first": "tesingname",
        "name_last": "hello"
    })

    response_user_uploadphoto = requests.post(BASE_URL + "/user/profile/uploadphoto/v1",json ={
        "token": token,
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": 0, 
        "y_start": 0, 
        "x_end": 100, 
        "y_end": 100
    })
    assert response_user_uploadphoto.status_code == 200

# valid token test
def test_invalid_token(clear_and_register):
    token = clear_and_register
    response_user_uploadphoto = requests.post(BASE_URL + "/user/profile/uploadphoto/v1",json ={
        "token": token + "1",
        "img_url": "http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg",
        "x_start": 0, 
        "y_start": 0, 
        "x_end": 100, 
        "y_end": 100
    })
    assert response_user_uploadphoto.status_code == 403