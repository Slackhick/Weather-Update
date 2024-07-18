from LiveRainfallMonitor import *
from LiveTemperatureMonitor import *
from LiveRainTempMonitor import *

'''
format the data to input for the graph
'''
class dataFormatter:
	def __init__(self):
		self.switcher = {'RainTempLiveMonitor': self.format_rain_temp,
					'TemperatureLiveMonitor': self.format_temp,
					'RainFallLiveMonitor': self.format_rain}

	def format_data(self, obj, data):
		formatted_data = self.switcher[obj.__class__.__name__](data)
		return formatted_data

	def format_rain(self, data):
		return [data[0], [], data[1]]

	def format_temp(self, data):
		return [[], data[0], data[1]]

	def format_rain_temp(self, data):
		return data
