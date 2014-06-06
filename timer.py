import time

import globals

class Timer(object):

    def __init__(self, period):

        self.time = period
        self.current = time.clock()

    def test(self):

        return (self.current + self.time >= time.clock())

    def get(self):

        return time.clock()-self.current

    def set(self, time):

        self.time = time

    def __str__(self):

        return str(self.current)+"/"+str(self.time)
