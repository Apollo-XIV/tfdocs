import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from logging import makeLogRecord
from rich.logging import RichHandler
from rich import print


HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 1234         # Port to listen on (same as used in the logger)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Custom HTTP Request Handler with enhanced logging using Rich."""
    
    def do_GET(self):
        """Handle GET requests and send a simple HTML response."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, this is a simple HTTP server!")

    def do_POST(self):
        """Handle POST requests, print received data, and send a response."""
        content_length = int(self.headers['Content-Length'])  # Get data length
        post_data = self.rfile.read(content_length)  # Read the POST data
        print(f"Received POST data: {post_data.decode('utf-8')}")
        self._send_html_response(b"POST request received!")

    def log_message(self, format, *args):
        """Override the default logging behavior to log using Rich."""
        query_dict = self._parse_query_params()
        log_record = makeLogRecord(query_dict)
        logger = logging.getLogger("log_watcher")
        logger.log(level=int(log_record.levelno), msg=log_record.msg)

    def _parse_query_params(self):
        """Helper function to parse query parameters into a dictionary."""
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        return {key: value[0] if len(value) == 1 else value for key, value in query_params.items()}

def setup_logging():
    """Set up Rich logging for the server."""
    format_str = "%(asctime)s %(levelname)s | %(message)s"
    logging.basicConfig(
        level="NOTSET",
        format=format_str,
        datefmt="[%X]",
    )
    log = logging.getLogger("log_watcher")
    log.addHandler(RichHandler(log_time_format="[%X]"))
    log.propagate = False
    return log


def main(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=1234):
    """Main function to set up and start the HTTP server."""
    log = setup_logging()
    server_address = (HOST, port)
    httpd = server_class(server_address, handler_class)
    log.info(f"Listening for logs on {HOST}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
