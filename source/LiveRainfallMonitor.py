from LiveWeatherMonitor import weatherLiveMonitor
from re import compile

class RainFallLiveMonitor(weatherLiveMonitor):

	def __init__(self, client, location):
		super(RainFallLiveMonitor, self).__init__(client, location)
		self.pattern = compile(r'Rainfall')
		self.rainfall_data = []
		return
	
	#Retrieve the current rainfall for the location stored
	def get_live_rainfall(self):
		retrieve_data = self.client.service.getWeather(self.location)

		if retrieve_data[2] is None:
			self.rainfall_data.append(0)
		else:
			self.rainfall_data.append(self.converter.convert_data('toMilimetre', retrieve_data[2]))
		self.shorten_data_list(self.rainfall_data)

		self.timestamp_record.append(retrieve_data[0].split()[1])
		self.shorten_data_list(self.timestamp_record)

		
	def Update(self):
		self.get_live_rainfall()
		self.set_timestamp()
		return [self.rainfall_data, self.timestamp_record]
