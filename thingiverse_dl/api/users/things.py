#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging

from .. import ThingiverseAPIBase
from .. import ThingiverseBase

logger = logging.getLogger(__name__)


def get(for_user):
    things = ThingiverseUserThings(for_user=for_user)
    while things.are_available():
        things_page = things.next()
        for thing in things_page:
            yield thing


class ThingiverseUserThings(ThingiverseAPIBase):
    def __init__(self, for_user):
        super().__init__()
        self.for_user = for_user
        self.page = 0
        self.page_contents = None

    @property
    def url(self):
        query_attrs = {
            'per_page': self.PER_PAGE,
        }
        if self.page > 0:
            query_attrs['page'] = self.page
        url = (self.for_user.url/'things').with_query(query_attrs)
        return url

    def are_available(self):
        self.page_contents = list(self)
        self._json = None
        return len(self.page_contents) > 0

    def next(self):
        self.page += 1
        return self.page_contents

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

