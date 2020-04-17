#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REST API functions under the /users/* URL"""
import logging

from . import things
from .. import ThingiverseBase

logger = logging.getLogger(__name__)


def get(username):
    return ThingiverseUser(username=username)


class ThingiverseUser(ThingiverseBase):
    URL_FORMAT = ThingiverseBase.URL_FORMAT/'users'

    def __init__(self, username):
        super().__init__()
        logger.info(f'ThingiverseUser init: {username}')
        self._username = username

    @property
    def url(self):
        return self.URL_FORMAT/self._username

    @property
    def things(self):
        logger.info(f'Things of {self._username}...')
        user_things = things.get(for_user=self)
        return user_things

    def __str__(self):
        logger.info(self.url)
        user_info = self.json
        import json
        logger.info(json.dumps(user_info, indent=4))
        self.resolve()
        return f'{self.name} ({self.full_name}): {self.public_url}'
