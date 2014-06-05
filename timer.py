import time

import globals

class Timer(object):

	def __init__(self, time):

		self.time = time
		self.current = time

	def update(self, delta):

		self.current -= delta

		return self.current

	def test(self):

		return (self.current <= 0)

	def retest(self):

		if(self.current <= 0):
			self.current = self.time

		return self.test()


	def reset(self):

		self.current = self.time

	def set(self, time):

		self.time = time

	def __str__(self):

		return str(self.current)+"/"+str(self.time)
