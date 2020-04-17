#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging

from .. import ThingiverseBase

logger = logging.getLogger(__name__)


def get(for_user):
    return ThingiverseUserThings(for_user=for_user)


class ThingiverseUserThings(ThingiverseBase):
    def __init__(self, for_user):
        super().__init__()
        self.for_user = for_user

    @property
    def url(self):
        return self.for_user.url/'things'

    def __iter__(self):
        for thing in self.json:
            yield ThingiverseUserThing(thing_api_response=thing)

class ThingiverseUserThing(object):
    def __init__(self, thing_api_response):
        logger.info(json.dumps(thing_api_response, indent=4))
