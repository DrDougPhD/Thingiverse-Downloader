#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REST API functions under the /things/* URL"""
import logging

from . import files
from .. import ThingiverseAPIBase

logger = logging.getLogger(__name__)


def get(id):
    return ThingiverseThing(id=id)


class ThingiverseThing(ThingiverseAPIBase):
    URL_FORMAT = ThingiverseAPIBase.URL_FORMAT/'things'

    def __init__(self, id):
        super().__init__()
        self._id = id

    @property
    def url(self):
        return self.URL_FORMAT/str(self._id)

    @property
    def files(self):
        thing_files = files.get(for_thing=self)
        return thing_files

    def __str__(self):
        logger.info(self.url)
        user_info = self.json
        import json
        logger.info(json.dumps(user_info, indent=4))
        self.resolve()
        # return 'One Single Thing'
        return f'Item "{self.name}" by {self.creator.name}: {self.public_url}'
