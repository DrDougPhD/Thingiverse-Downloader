import logging
import urllib.parse
import webbrowser

from thingiverse_dl import config
from . import tempserver

logger = logging.getLogger(__name__)


def required(function):
    def wrapper(*args, **kwargs):
        logger.info(f'{function.__name__}(args={args}, kwargs={kwargs})')
        # Open a web browser to begin authentication process

        logger.info(config.secrets.client_id)
        # thingiverse = OAuth2Session(client_id=config.secrets.client_id)
        auth_url = AuthenticationURLBuilder(
            client_id=config.secrets.client_id,
            redirect_uri='http://localhost:8888/blah',
            response_type='code',
        )

        # Start a server to wait for user authentication and redirection from
        # Thingiverse to this app.
        server = tempserver.run(port=8888)
        webbrowser.open_new_tab(url=str(auth_url))
        logger.info(f'Opening {auth_url}')
        server.serve_forever()
        url = server.requested_url

        result = function(*args, **kwargs)
        logger.info(f'Returned value: {result}')
        return result
    return wrapper


class AuthenticationURLBuilder(object):
    URL = 'https://www.thingiverse.com/login/oauth/authorize'
    def __init__(self, **kwargs): # client_id, redirect_uri, response_type
        self.query = urllib.parse.urlencode(list(kwargs.items()))

    def __str__(self):
        return f'{self.URL}?{self.query}'