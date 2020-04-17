#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging

from .. import ThingiverseAPIBase
from .. import ThingiverseBase

logger = logging.getLogger(__name__)


def get(for_thing):
    return ThingiverseThingFiles(for_thing=for_thing)


class ThingiverseThingFiles(ThingiverseAPIBase):
    def __init__(self, for_thing):
        super().__init__()
        self.for_thing = for_thing

    @property
    def url(self):
        return self.for_thing.url/'files'

    def __iter__(self):
        for file in self.json:
            yield ThingiverseThingFile(api_response=file)


class ThingiverseThingFile(ThingiverseBase):
    def __init__(self, api_response):
        super().__init__()
        self._json = api_response
        self.resolve()

    def __str__(self):
        logger.info(json.dumps(self._json, indent=4))
        return ''
        # return f'Item "{self.name}" ({self.public_url}) by {self.creator.name}'

