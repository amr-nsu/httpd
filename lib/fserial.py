import serial
import time
import os

class SerialDevice:

    def __init__(self, device, baud):
        self.serial = serial.Serial(device, baud, timeout=1)

    def send_request(self, request):
        self.serial.write('%s\n' % request)
        response = self.serial.readline()[:-1]
        if not response:
            response = 'NULL'
        elif request in ('A', '1', '2', '3', '4', '5', '6'):
            response = ord(response)
        return response

    def request(self, request):
        try:
            return self.send_request(request)
        except Exception as e:
            return str(e)
