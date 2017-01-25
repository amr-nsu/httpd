#!/usr/bin/env python2
import cgi
import serial
from random import random

DEBUG = True

form = cgi.FieldStorage()

print("Content-type: text/html\n")

def debug(request):
    response = 'n'
    if request == 'A':
        response = chr(80)
    if request in ('1', '2', '3', '4', '5', '6'):
        response = chr(int(random() * 255))
    if request in ('F', 'B', 'L', 'R', 'S'):
        response = request
    return response

def send_request(cmd):
    ser = serial.Serial("/dev/ttyS0", 115200, timeout=1)
    ser.write(cmd)
    response = ser.read()
    if not response:
        response = "NULL"
    print(response)

if "cmd" in form:
    cmd = form["cmd"].value
    if DEBUG:
        print(debug(cmd))
    else:
        try:
            send_request(cmd)
        except Exception as e:
            print(str(e))

