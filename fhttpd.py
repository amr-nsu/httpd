import math
import time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from lib.fserial import SerialDevice
from lib.gps import GPS

#DEVICE = '/dev/ttyUSB0'
DEVICE = '/dev/ttyS0'
BAUD = 115200
V = 0.17
W = 2.3

class HttpHandler(BaseHTTPRequestHandler):

    device = SerialDevice(DEVICE, BAUD)
    gps = GPS()
    t_prev = 0
    request_prev = 0

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
            if request == 'C':
                response = "%.2f %.2f %.1f" % (HttpHandler.gps.x,HttpHandler.gps.y,HttpHandler.gps.q*180/math.pi)
            else:
                response = self.device.request(request)
            self.wfile.write(response)
            self.get_pos(request)

    def get_pos(self, request):
        t = time.time()
        if HttpHandler.t_prev == 0:
            dt = 0
        else:
            dt = t - HttpHandler.t_prev
        HttpHandler.t_prev = t
        if HttpHandler.request_prev == 'F':
            HttpHandler.gps.move(V, 0, dt)
            print HttpHandler.gps.x, HttpHandler.gps.y, HttpHandler.gps.q

        if HttpHandler.request_prev == 'B':
            HttpHandler.gps.move(-V, 0, dt)
            print HttpHandler.gps.x, HttpHandler.gps.y, HttpHandler.gps.q

        if HttpHandler.request_prev == 'R':
            HttpHandler.gps.move(0, W, dt)
            print HttpHandler.gps.x, HttpHandler.gps.y, HttpHandler.gps.q

        if HttpHandler.request_prev == 'L':
            HttpHandler.gps.move(0, -W, dt)
            print HttpHandler.gps.x, HttpHandler.gps.y, HttpHandler.gps.q
        HttpHandler.request_prev = request




if __name__ == '__main__':
    print('fhttpd started ...')
    server = HTTPServer(('', 8000), HttpHandler)
    server.serve_forever()
