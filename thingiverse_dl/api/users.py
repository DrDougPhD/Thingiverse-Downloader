#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REST API functions under the /users/* URL"""
import requests
import logging

from . import ThingiverseBase

logger = logging.getLogger(__name__)


def get(username):
    return ThingiverseUser(username=username)


class ThingiverseUser(ThingiverseBase):
    def __init__(self, username):
        super().__init__()
        logger.info('ThingiverseUser init')
        self.username = username
        # response = requests.get(f'https://api.thingiverse.com/users/{username}')
        # print(response)
        # print(response.text)
        # print(response.json())

    @property
    def things(self):
        pass
