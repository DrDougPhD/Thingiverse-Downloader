import logging

import yarl

from .. import authentication
from .. import utilities

logger = logging.getLogger(__name__)


class ThingiverseBase(object):
    URL_PREFIX = yarl.URL('https://api.thingiverse.com')
    URL_BASE_FORMAT = ''

    def __init__(self):
        logger.info('Thingiverse Base Class init')
        self._session = None

    # @utilities.slowdown(to=5)
    @property
    def session(self):
        if self._session is None:
            self._session = authentication.now()
        return self._session

    @property
    def url_base(self):
        return self.URL_PREFIX/self.URL_BASE_FORMAT.format(self)

    @property
    def json(self):
        if self._json is None:
            self._json = self.resolve()
        return self._json

    def resolve(self):
        response = self.session.get(self.url_base)
        self._json = response.json()

        for key, value in self._json.items():
            setattr(self, key, utilities.objectify(value))

        return self._json
