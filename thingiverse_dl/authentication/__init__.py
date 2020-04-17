#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from . import authenticate
from . import authorize
from ..utilities import DelayedNetworkRequest
from ..utilities import Singleton

logger = logging.getLogger(__name__)


def now():
    return AuthenticatedSession()


class AuthenticatedSession(DelayedNetworkRequest,
                           metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Authorize this script to access a user's account
        authorization_code = authorize.me()

        # Obtain oath2 token for authentication
        authentication_token = authenticate.me(code=authorization_code)

        self.headers.update({
            'Authorization': f'Bearer {authentication_token}'
        })
