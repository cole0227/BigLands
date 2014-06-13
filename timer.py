import time
from threading import Timer as Thread_Timer

import globals

class Timer(object):

    def __init__(self, period, delay=0, delay_action = None):

        self.time = period
        self.delay = delay
        self.delay_action = delay_action
        self.current = time.time()

    def attempt_action(self):

        if(self.test()):
            self.current = time.time()

            if(self.delay_action != None):

                if(self.delay>0):

                    Thread_Timer(self.delay, self.delay_action).start()

                else:
                    self.delay_action()

            return True

        return False

    def test(self):

        return (self.current + self.time <= time.time())

    def get(self):

        return time.time()-self.current

    def set(self, time):

        self.time = time

    def __str__(self):

        return str(self.current)+":"+str(self.delay)+":"+str(self.time)
