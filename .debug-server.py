import http.server, os, socketserver, urllib.request

INGEST = "http://127.0.0.1:7410"
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class H(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if not self.path.startswith("/ingest/"):
            self.send_error(404)
            return
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        req = urllib.request.Request(INGEST + self.path, data=body, method="POST", headers={
            "Content-Type": "application/json",
            "X-Debug-Session-Id": self.headers.get("X-Debug-Session-Id", ""),
        })
        try:
            urllib.request.urlopen(req, timeout=3).read()
        except Exception:
            pass
        self.send_response(204)
        self.end_headers()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


socketserver.ThreadingTCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("0.0.0.0", 8765), H) as s:
    s.serve_forever()
