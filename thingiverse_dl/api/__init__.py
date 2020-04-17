import logging

import requests

from ..authentication import authenticate
from ..authentication import authorize

logger = logging.getLogger(__name__)


class ThingiverseBase(object):
    URL_PREFIX = 'https://api.thingiverse.com'
    URL_BASE_FORMAT = '/'

    def __init__(self):
        logger.info('Thingiverse Base Class init')
        self._session = None

    @property
    def session(self):
        if self._session is None:
            # Authorize this script to access a user's account
            authorization_code = authorize.me()

            # Obtain oath2 token for authentication
            authentication_token = authenticate.me(code=authorization_code)

            # Assign token to session
            authenticated_session = requests.Session()
            authenticated_session.headers.update({
                'Authorization': f'Bearer {authentication_token}'
            })
            self._session = authenticated_session
        return self._session

    @property
    def url_base(self):
        return f'{self.URL_PREFIX}{self.URL_BASE_FORMAT.format(self)}'
