#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import requests

from . import authorize
from . import authenticate
from .. import utilities

logger = logging.getLogger(__name__)


@utilities.singleton
class AuthenticationManager(object):
    def __init__(self, function):
        self.function = function
        self._session = None

    def __call__(self, *args, **kwargs):
        logger.info(f'{self.function.__name__}(args={args}, kwargs={kwargs})')
        logger.info(self)
        result = self.function(*args, **kwargs)
        return result

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


required = AuthenticationManager
