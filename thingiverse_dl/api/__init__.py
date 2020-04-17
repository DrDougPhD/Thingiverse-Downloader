import datetime
import logging
import time

import requests

from ..authentication import authenticate
from ..authentication import authorize

logger = logging.getLogger(__name__)


class ThingiverseBase(object):
    URL_PREFIX = 'https://api.thingiverse.com'
    URL_BASE_FORMAT = '/'
    MINIMUM_WAIT_TIME = datetime.timedelta(seconds=5)

    def __init__(self):
        logger.info('Thingiverse Base Class init')
        self._session = None
        self._last_called_on = datetime.datetime.fromtimestamp(0)

    # @utilities.slowdown(to=5)
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

        self.wait()
        return self._session

    def wait(self):
        current_time = datetime.datetime.now()
        previous_time = self._last_called_on
        time_since_last_call = current_time - previous_time
        if time_since_last_call < self.MINIMUM_WAIT_TIME:
            logger.info(f'Waiting {time_since_last_call} until next call...')
            time.sleep(time_since_last_call.seconds)

        self._last_called_on = datetime.datetime.now()
        return

    @property
    def url_base(self):
        return f'{self.URL_PREFIX}{self.URL_BASE_FORMAT.format(self)}'
