from WeatherMonitor import weatherMonitor
from re import compile

class RainFallMonitor(weatherMonitor):

	def __init__(self, client, location):
		super(RainFallMonitor, self).__init__(client, location)
		self.pattern = compile(r'Rainfall (\d{1,2}\.\d|\-)')
		return
	
	#Retrieve the current rainfall for the location stored
	def get_rainfall(self):
		 return self.client.service.getRainfall(self.location)
	
	def Update(self):
		self.data = self.get_rainfall()
		self.content ='Rainfall %s' % self.data[-1]
		self.set_timestamp()
		return self.content
