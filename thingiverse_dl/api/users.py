#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REST API functions under the /users/* URL"""
import requests


def get(username):
    return ThingiverseUser(username=username)


class ThingiverseUser(object):
    def __init__(self, username):
        self.username = username
        response = requests.get(f'https://api.thingiverse.com/users/{username}')
        print(response)
        print(response.text)
        print(response.json())

    @property
    def things(self):
        pass
