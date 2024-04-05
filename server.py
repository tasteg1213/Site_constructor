import os
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler


class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.end_headers()


def run(
    server_class=HTTPServer,
    handler_class=CORSHTTPRequestHandler,
    port=8000,
    directory=None,
):
    if directory:  # Change the current working directory if directory is specified
        os.chdir(directory)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving HTTP on http://localhost:{port} from directory '{directory}'...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down the server...")
        httpd.server_close()  # Properly close the server
    except OSError as e:
        if e.errno == 48:  # Port is already in use
            print(f"OSError: Port {port} is already in use. Try a different port.")
    else:
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Server with CORS")
    parser.add_argument(
        "--dir", type=str, help="Directory to serve files from", default="."
    )
    parser.add_argument("--port", type=int, help="Port to serve HTTP on", default=8888)
    args = parser.parse_args()

    run(port=args.port, directory=args.dir)
