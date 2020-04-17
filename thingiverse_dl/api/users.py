#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REST API functions under the /users/* URL"""
import logging

from . import ThingiverseBase

logger = logging.getLogger(__name__)


def get(username):
    return ThingiverseUser(username=username)


class ThingiverseUser(ThingiverseBase):
    URL_BASE_FORMAT = '/users/{0.username}'

    def __init__(self, username):
        super().__init__()
        logger.info(f'ThingiverseUser init: {username}')
        self.username = username
        # response = requests.get(f'https://api.thingiverse.com/users/{username}')
        # print(response)
        # print(response.text)
        # print(response.json())

    def resolve(self):
        response = self.session.get(self.url_base)
        payload = response.json()
        return payload

    @property
    def things(self):
        return f'Things of {self.username}'

    def __str__(self):
        logger.info(self.url_base)
        user_info = self.resolve()
        return ''