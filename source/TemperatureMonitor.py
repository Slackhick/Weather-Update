from WeatherMonitor import weatherMonitor
from re import compile

class TemperatureMonitor(weatherMonitor):
	
	def __init__(self, client, location):
		super(TemperatureMonitor, self).__init__(client, location)
		self.pattern = compile(r'Temperature (\d{1,2}\.\d|\-)')
		return
		
	#Retrieve the current temperature of the current location
	def Update(self):
		self.data = self.get_temperature()
		self.content = 'Temperature %s' % self.data[-1]
		self.set_timestamp()
		return self.content

	def get_temperature(self):
		return self.client.service.getTemperature(self.location)
