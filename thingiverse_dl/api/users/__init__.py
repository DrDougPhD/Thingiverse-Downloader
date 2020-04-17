#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REST API functions under the /users/* URL"""
import logging

from . import things
from .. import ThingiverseAPIBase

logger = logging.getLogger(__name__)


def get(username):
    return ThingiverseUser(username=username)


class ThingiverseUser(ThingiverseAPIBase):
    URL_FORMAT = ThingiverseAPIBase.URL_FORMAT/'users'

    def __init__(self, username):
        super().__init__()
        self._username = username

    @property
    def url(self):
        return self.URL_FORMAT/self._username

    @property
    def things(self):
        return things.get(for_user=self)

    def __str__(self):
        self.resolve()
        return f'{self.name} ({self.full_name}): {self.public_url}'
