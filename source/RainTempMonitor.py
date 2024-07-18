from WeatherMonitor import weatherMonitor
from re import compile

class RainTempMonitor(weatherMonitor):
	def __init__(self, client, location):
		super(RainTempMonitor, self).__init__(client, location)
		self.pattern = compile(r'Rainfall (\d{1,2}\.\d|\-)\nTemperature (\d{1,2}\.\d|\-)')
		return

	def get_rain_temp(self):
		return self.client.service.getRainfall(self.location) +\
				 [self.client.service.getTemperature(self.location)[-1]]

	def Update(self):
		self.data = self.get_rain_temp()
		self.content = 'Rainfall %s\nTemperature %s' % (self.data[1], self.data[2])
		self.set_timestamp()
		return self.content
