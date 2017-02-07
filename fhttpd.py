from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from lib.fserial import SerialDevice

#DEVICE = '/dev/ttyUSB0'
DEVICE = '/dev/ttyS0'
BAUD = 115200


class HttpHandler(BaseHTTPRequestHandler):

    device = SerialDevice(DEVICE, BAUD)

    def do_GET(self):
        self.send_response(200)
#        self.send_header('Content-type','text/html')
        self.end_headers()
        self.get_file()
        self.get_cmd()

    def get_file(self):
        if self.path.endswith(".html") or self.path.endswith(".js") or self.path.endswith(".svg") or self.path.endswith(".css"):
            try:
                f = open(curdir + sep + self.path)
                self.wfile.write(f.read())
                f.close()
            except IOError as e:
                self.send_error(404, str(e))

    def get_cmd(self):
        if 'cmd' in self.path:
            request = self.path[-1]
            response = self.device.request(request)
            self.wfile.write(response)


if __name__ == '__main__':
    print('fhttpd started ...')
    server = HTTPServer(('', 8000), HttpHandler)
    server.serve_forever()
