#!/usr/bin/env python3
"""Static server for the pop-up storybook.

Serving (rather than file://) is required because the engine fetch()es JSON data,
which browsers block under the file:// origin. Binds localhost; expose with
`tailscale serve 8080` for the Pixel, or publish the folder to GitHub Pages later.

    python3 tools/serve.py            # http://127.0.0.1:8080
    python3 tools/serve.py 9000       # custom port
"""
import http.server, socketserver, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def end_headers(self):
        # no-cache during dev so edits to data/art show up on reload
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s - %s\n" % (self.address_string(), fmt % args))


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    print(f"Storybook serving {ROOT}")
    print(f"  -> http://127.0.0.1:{PORT}/   (Ctrl-C to stop)")
    print(f"  -> phone: tailscale serve {PORT}")
    with Server(("127.0.0.1", PORT), H) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
