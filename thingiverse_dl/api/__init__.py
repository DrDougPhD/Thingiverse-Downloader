#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import yarl

from .. import authentication
from .. import utilities

logger = logging.getLogger(__name__)


class ThingiverseBase(object):
    URL_FORMAT = yarl.URL('https://api.thingiverse.com')

    def __init__(self):
        logger.info('Thingiverse Base Class init')
        self._session = None
        self._json = None

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
    def json(self):
        if self._json is None:
            self._json = self.session.get(self.url).json()
        return self._json

    def resolve(self):
        for key, value in self.json.items():
            try:
                setattr(self, key, utilities.objectify(value))
            except AttributeError:
                logger.warning(
                    f'Attempted to set {key} on {self.__class__.__name__},'
                    f' but that is a reserved keyword.'
                )

        return self
