from Observer import observer
import time

class weatherMonitor(observer):

	def __init__(self, client, location):
		self.client = client
		self.location = location
		self.latest_timestamp = 0
		self.data =[]
		self.content = ''

	def Update(self):
		pass
	
	def set_timestamp(self):
		self.latest_timestamp = time.time()
