import http.server
import controller

class HTTPHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()
    
    def do_GET(self):
        response_content, content_type = controller.GETResponse(self.path)
        self._set_headers(content_type)
        self.wfile.write(response_content)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        content = self.rfile.read(content_length).decode("utf-8")
        response = controller.POSTResponse(self.path,content)
        self._set_headers("text/html")
        self.wfile.write(str.encode(str(response)))

try:
    port=8080
    httpd = http.server.HTTPServer(('',port), HTTPHandler)
    print("Server started...port:",port)
    httpd.serve_forever()
except:
    print("Server stop running.")