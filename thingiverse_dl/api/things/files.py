#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import pathlib

import humanfriendly

from .. import ThingiverseAPIBase
from .. import ThingiverseBase
from ... import utilities

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

    def download(self, within: pathlib.Path):
        within.mkdir(parents=True, exist_ok=True)
        destination = within/self.name
        utilities.download(url=self.public_url, to=destination)
        return destination

    def __str__(self):
        filesize = humanfriendly.format_size(self.size)
        return f'{self.name} ({filesize}): {self.download_url}'
