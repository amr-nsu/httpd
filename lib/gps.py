from math import sin, cos

class GPS:

    def __init__(self, x=0, y=0, q=0):
        self.x = x
        self.y = y
        self.q = q

    def move(self, v, w, dt):
        self.q = self.q + w * dt
        self.x = self.x + v * cos(self.q) * dt
        self.y = self.y + v * sin(self.q) * dt
        return self.x, self.y, self.q
