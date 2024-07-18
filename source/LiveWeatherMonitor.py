from Observer import observer
from dataConverter import *
import time

class weatherLiveMonitor(observer):

	def __init__(self, client, location):
		self.client = client
		self.location = location
		self.latest_timestamp = 0
		self.limit = 10
		self.timestamp_record = []
		self.converter = dataConverter()

	def Update(self):
		pass
	
	def set_timestamp(self):
		self.latest_timestamp = time.time()

	def shorten_data_list(self, data):
		if len(data) > self.limit:
			data.pop(0)
			
