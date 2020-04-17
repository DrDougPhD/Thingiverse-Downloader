#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import logging
import time

import requests

from . import authenticate
from . import authorize
from ..utilities import Singleton

logger = logging.getLogger(__name__)


def now():
    return AuthenticatedSession()


class AuthenticatedSession(requests.Session,
                           metaclass=Singleton):
    MINIMUM_WAIT_TIME = datetime.timedelta(seconds=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Authorize this script to access a user's account
        authorization_code = authorize.me()

        # Obtain oath2 token for authentication
        authentication_token = authenticate.me(code=authorization_code)

        # Assign token to session
        authenticated_session = requests.Session()

        self.headers.update({
            'Authorization': f'Bearer {authentication_token}'
        })

        self._last_called_on = datetime.datetime.fromtimestamp(0)

    def request(self, *args, **kwargs):
        current_time = datetime.datetime.now()
        previous_time = self._last_called_on
        time_since_last_call = current_time - previous_time
        if time_since_last_call < self.MINIMUM_WAIT_TIME:
            logger.info(f'Waiting {time_since_last_call} until next call...')
            time.sleep(time_since_last_call.seconds)

        response = super().request(*args, **kwargs)

        self._last_called_on = datetime.datetime.now()

        return response