from __future__ import absolute_import

from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.test import Client

from . import control

def get_team_client():
    client = Client()
    logged_in = client.login(username=user.username, 
        password=control.DEFAULT_PASSWORD)
    if not logged_in:
        raise PermissionDenied("""
            user could not be logged in:
                username: %s
                password: %s
            """ % (user.username, control.DEFAULT_PASSWORD))
    return client

def get(view_name=None, view_url=None, user=None, args=None):
    if view_name and view_url:
        raise Exception("set either view_name or view_url, not both.")

    if view_name:
        view_url = reverse(view_name)

    client = Client()
    if user:
        logged_in = client.login(username=user.username, 
            password=control.DEFAULT_PASSWORD)
        if not logged_in:
            raise PermissionDenied("""
                user could not be logged in:
                    username: %s
                    password: %s
                """ % (user.username, control.DEFAULT_PASSWORD))
    response = client.get(view_url)

    return response.status_code

# class TestViewStatusCode:
#     def __init__(self, view_name=None, view_url=None, expected_status_code=200):
#         this.status_code = expected_status_code

#         if view_name and view_url:
#             raise Exception("set either view_name or view_url, not both.")

#         if view_name:
#             view_url = reverse(view_name)
#             pass

#         client = Client()
        
#     def run():
#         response = client.get(view_url)
#         return response.status_code == self.status_code






