#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import requests
import urllib.parse

from thingiverse_dl import config

logger = logging.getLogger(__name__)


def me(code):
    response = requests.post(
        'https://www.thingiverse.com/login/oauth/access_token',
        data={
            'code': code,
            'client_id': config.secrets.client_id,
            'client_secret': config.secrets.client_secret,
        }
    )

    token_response = urllib.parse.parse_qs(response.text)
    return token_response['access_token'].pop()
