from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# from django.test import TestCase, Client
# from django.urls import reverse
# 
# from rest_framework import status
#  from rest_framework.test import APITestCase
import requests

class TestCards:
    _testData = {
        'test_user': {
            'id': '',
            'username': 'testuser',
            'password': 'grumpymcgrumpface88',
            'token': '7b2f9b036a5eefb31489c981ac8216dda5d15cf7',
        },
        'admin_user': {
            'id': '',
            'username': 'admin',
            'password': 'superduperpassword',
            'token': '',
        }
    }

