import http.server
import logging

logger = logging.getLogger(__name__)


def create(port=8888):
    return StoppableHTTPServer(port=port)


class StoppableHTTPServer(http.server.HTTPServer):
    """http server that reacts to self.stop flag"""
    def __init__(self, port):
        server_address = ('', port)
        super().__init__(server_address, SingleHTTPRequestHandler)
        self.requested_url = None

    def serve_forever(self, **kwargs):
        """Handle one request at a time until stopped.
        :param **kwargs:
        """
        self.stop = False
        while not self.stop:
            self.handle_request()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type in (KeyboardInterrupt, SystemExit):
            return False

        elif exc_type is not None:
            logger.exception("Something happened and I don't know "
                             "what to do")
            return False

        else:
            logger.info('Authentication code catching server terminating')
            return True


class SingleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        logger.warning('HTTP GET RECEIVED!')
        logger.info(self.path)
        self.server.requested_url = self.path

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.server.stop = True

        # Doesn't auto-close page just yet :/
        self.wfile.write(b'''
        <html>
            <head>
            </head>
            <body>
                <script type='text/javascript'>
                    window.onload = function() {
                        window.close();
                    };
                </script>
            </body>
        </html>
        ''')
