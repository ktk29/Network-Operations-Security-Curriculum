from http.server import HTTPServer, BaseHTTPRequestHandler

#type http://localhost:8000/ into your web browser to see it
#used port 8000 cause i'm cool
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Hello World! -- KT smashed it yet again</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


def run():
    server_address = ("localhost", 8000)
    server = HTTPServer(server_address, MyServer)
    server.serve_forever()


run()
