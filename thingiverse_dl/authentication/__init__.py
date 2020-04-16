#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import requests

from . import authorize
from . import authenticate

logger = logging.getLogger(__name__)


def required(function):
    def wrapper(*args, **kwargs):
        logger.info(f'{function.__name__}(args={args}, kwargs={kwargs})')
        # Authorize this script to access a user's account
        authorization_code = authorize.me()

        # Obtain oath2 token for authentication
        authentication_token = authenticate.me(code=authorization_code)

        # Assign token to session
        authenticated_session = requests.Session()
        authenticated_session.headers.update({
            'Authorization': f'Bearer {authentication_token}'
        })

        result = function(*args, **kwargs)
        logger.info(f'Returned value: {result}')
        return result
    return wrapper
