#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging

from .. import ThingiverseAPIBase
from .. import ThingiverseBase

logger = logging.getLogger(__name__)


def get(for_user):
    return list(ThingiverseUserThings(for_user=for_user))


class ThingiverseUserThings(ThingiverseAPIBase):
    def __init__(self, for_user):
        super().__init__()
        self.for_user = for_user

    @property
    def url(self):
        return self.for_user.url/'things'

    def __iter__(self):
        for thing in self.json:
            yield ThingiverseUserThing(thing_api_response=thing)


class ThingiverseUserThing(ThingiverseBase):
    def __init__(self, thing_api_response):
        super().__init__()
        self._json = thing_api_response
        self.resolve()

    def __str__(self):
        logger.info(json.dumps(self._json, indent=4))
        return f'Item "{self.name}" ({self.public_url}) by {self.creator.name}'

