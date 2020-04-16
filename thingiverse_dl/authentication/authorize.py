#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import urllib.parse
import webbrowser

from thingiverse_dl import config
from . import tempserver

logger = logging.getLogger(__name__)


def me():
    # Open a web browser to begin authentication process
    auth_url = build_authentication_url(
        client_id=config.secrets.client_id,
        redirect_uri='http://localhost:8888/callback',
        response_type='code',
    )

    # Start a server to wait for user authentication and redirection from
    # Thingiverse to this app.
    with tempserver.create(port=8888) as server:
        webbrowser.open_new_tab(url=str(auth_url))
        logger.info(f'Opening {auth_url}')
        server.serve_forever()

    parsed_callback_url = urllib.parse.urlparse(server.requested_url)
    query = urllib.parse.parse_qs(parsed_callback_url.query)
    return query['code'].pop()


def build_authentication_url(**kwargs):
    url = 'https://www.thingiverse.com/login/oauth/authorize'
    query = urllib.parse.urlencode(list(kwargs.items()))
    return f'{url}?{query}'
