#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import yarl

from .. import authentication
from .. import utilities

logger = logging.getLogger(__name__)


class ThingiverseBase(object):
    def __init__(self):
        self._json = None

    def resolve(self):
        for key, value in self.json.items():
            try:
                setattr(self, key, utilities.classify(value))
            except AttributeError:
                logger.warning(
                    f'Attempted to set {key} on {self.__class__.__name__},'
                    f' but that is a reserved keyword.'
                )

        return self

    @property
    def json(self):
        return self._json


class ThingiverseAPIBase(ThingiverseBase):
    URL_FORMAT = yarl.URL('https://api.thingiverse.com')
    PER_PAGE = 100

    def __init__(self):
        super().__init__()
        self._session = None

    # @utilities.slowdown(to=5)
    @property
    def session(self):
        if self._session is None:
            self._session = authentication.now()
        return self._session

    @property
    def url(self):
        raise NotImplementedError(
            f'The {self.__class__.__name__} class needs to implement'
            f' the @property "url"'
        )

    @property
    @utilities.cached_json(key='url')
    def json(self):
        if self._json is None:
            url = self.url
            logger.info(f'Loading {self.__class__.__name__} from {url}')
            self._json = self.session.get(url).json()
        return self._json