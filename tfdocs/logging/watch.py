import logging
import socket
import pickle
from urllib.parse import urlparse, parse_qs
import struct
from rich import print
from rich.console import Console
from rich.logging import RichHandler
from logging import makeLogRecord


HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 1234         # Port to listen on (same as used in the logger)

from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    log_formatter = RichHandler()

    def do_GET(self):
        # Handle GET request
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, this is a simple HTTP server!")

    def do_POST(self):
        # Handle POST request
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length)  # Read the POST data
        print(f"Received POST data: {post_data.decode('utf-8')}")
        
        # Send a simple response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"POST request received!")

    # Override log_message to disable logging
    def log_message(self, format, *args):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Convert query parameters to a simple dict (values will be lists)
        query_dict = {key: value[0] if len(value) == 1 else value for key, value in query_params.items()}
        log_record = makeLogRecord(query_dict)
        log = logging.getLogger("log_watcher")
        log.log(
            level = int(log_record.levelno),
            msg = log_record.msg,
        )

def main(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=1234):
    FORMAT = "%(asctime)s %(levelname)s | %(message)s"
    logging.basicConfig(
        level="NOTSET",
        format=FORMAT,
        datefmt="[%X]",
    )
    log = logging.getLogger("log_watcher")
    log.addHandler(RichHandler())
    log.propagate = False

    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    log.info(f"Starting http server on localhost:{port}...")
    httpd.serve_forever()
