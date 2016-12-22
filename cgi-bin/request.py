#!/usr/bin/env python2
import cgi
import serial

form = cgi.FieldStorage()

print("Content-type: text/html\n")

def send_request(cmd):
    ser = serial.Serial("/dev/ttyS0", 115200)
    ser.write(cmd)
    response = ser.read()
    print(response)

if "cmd" in form:
    cmd = form["cmd"].value
    try:
        send_request(cmd)
    except Exception as e:
        print(str(e))

