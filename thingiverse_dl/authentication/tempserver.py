import http.server
import logging
from typing import Tuple
from typing import Callable

logger = logging.getLogger(__name__)


def run(port=8888):
    server_address = ('', port)
    return StoppableHttpServer(server_address, SingleHTTPRequestHandler)


class SingleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        logger.warning('HTTP GET RECEIVED!')
        logger.info(self.path)
        self.send_response(200)
        self.end_headers()
        self.server.requested_url = self.path
        self.server.stop = True


class StoppableHttpServer(http.server.HTTPServer):
    def __init__(self, server_address: Tuple[str, int], RequestHandlerClass: Callable[..., http.server.BaseHTTPRequestHandler]):
        super().__init__(server_address, RequestHandlerClass)
        self.requested_url = None

    """http server that reacts to self.stop flag"""
    def serve_forever(self, **kwargs):
        """Handle one request at a time until stopped.
        :param **kwargs:
        """
        self.stop = False
        while not self.stop:
            self.handle_request()
