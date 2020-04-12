import logging
import urllib.parse
import webbrowser
import requests

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
        code = query['code'].pop()

        logger.warning(f'Callback url: {code}')

        # Obtain token using code
        response = requests.post(
            'https://www.thingiverse.com/login/oauth/access_token',
             data={
                'code': code,
                'client_id': config.secrets.client_id,
                'client_secret': config.secrets.client_secret,
             }
        )

        token_response = urllib.parse.parse_qs(response.text)
        token = token_response['access_token'].pop()

        authenticated_session = requests.Session()
        authenticated_session.headers.update({
            'Authorization': f'Bearer {token}'
        })



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