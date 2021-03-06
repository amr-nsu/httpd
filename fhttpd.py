import math
import time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from lib.fserial import SerialDevice
from lib.gps import GPS, wrap_to_pi

#DEVICE = '/dev/ttyUSB0'
DEVICE = '/dev/ttyS0'
BAUD = 19200
V = 0.39
W = 4.9

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
        self.go_pos()

    def get_file(self):
        if self.path.endswith(".html") or self.path.endswith(".js") or self.path.endswith(".svg") or self.path.endswith(".css"):
            try:
                f = open(curdir + sep + self.path)
                self.wfile.write(f.read())
                f.close()
            except IOError as e:
                self.send_error(404, str(e))

    def get_cmd(self):
        if not 'cmd' in self.path or 'cmd=go' in self.path:
            return
        request = self.path[-1]
        if request == 'C':
            response = "%.2f %.2f %.1f" % (HttpHandler.gps.x,HttpHandler.gps.y,HttpHandler.gps.q*180/math.pi)
        else:
            response = self.device.request(request)
        self.wfile.write(response)
        self.get_pos(request)

    def get_pos(self, request):
        if request not in ('F', 'B', 'R', 'L', 'S'):
            return
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

    def go_pos(self):
        if not 'cmd=go' in self.path:
            return
        r = self.path[8:]
        q = r.split('&')
        x = float(q[0][2:])
        y = float(q[1][2:])
        dt = 0.0001
        a = x - HttpHandler.gps.x
        b = y - HttpHandler.gps.y
        c = math.sqrt(a*a+b*b)
        alph = math.atan2(b, a)
 
        if wrap_to_pi(alph -HttpHandler.gps.q) > 0:
            direction = 'R'
            w = W
        else:
            direction = 'L'
            w = -W
        move = False 
        while (abs(HttpHandler.gps.q - alph) > 0.001):
            if not move:
                self.device.request(direction)
                move = True
            HttpHandler.gps.move(0, w, dt)
            time.sleep(dt)

        c_prev = c
        move = False
        while c > 0.001:
            if not move:
                self.device.request('F')
                move = True
            HttpHandler.gps.move(V, 0, dt)
            time.sleep(dt)
            a = x - HttpHandler.gps.x
            b = y - HttpHandler.gps.y
            c = math.sqrt(a*a+b*b)
            if c > c_prev:  # distance increase
                break
            c_prev = c
        self.device.request('S') 


if __name__ == '__main__':
    print('fhttpd started ...')
    server = HTTPServer(('', 8000), HttpHandler)
    server.serve_forever()
