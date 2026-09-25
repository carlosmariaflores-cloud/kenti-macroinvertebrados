import http.server, json, sys, os
ROOT=sys.argv[1]; PORT=int(sys.argv[2])
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def log_message(s,*a): pass
    def _j(s,o,code=200):
        b=json.dumps(o).encode(); s.send_response(code); s.send_header("Content-Type","application/json"); s.end_headers(); s.wfile.write(b)
    def do_GET(s):
        if s.path.startswith("/api/datos"): s.send_response(204); s.end_headers(); return
        if s.path.startswith("/api/info"): return s._j({"app":"kenti-macroinvertebrados","version":"0.4"})
        if s.path.startswith("/api/"): return s._j({"ok":True})
        return super().do_GET()
    def do_PUT(s):
        n=int(s.headers.get("Content-Length",0)); s.rfile.read(n); s._j({"ok":True})
    do_POST=do_PUT
http.server.ThreadingHTTPServer(("127.0.0.1",PORT),H).serve_forever()
