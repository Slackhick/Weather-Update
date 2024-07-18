from LiveWeatherMonitor import weatherLiveMonitor
from re import compile


class TemperatureLiveMonitor(weatherLiveMonitor):

	def __init__(self, client, location):
		super(TemperatureLiveMonitor, self).__init__(client, location)
		self.pattern = compile(r'Temperature')
		self.temperature_data = []
		return
	
	#Retrieve the current temperature for the location stored
	def get_live_temperature(self):
		retrieve_data = self.client.service.getWeather(self.location)

		if retrieve_data[1] is None:
			self.temperature_data.append(0)
		else:
			self.temperature_data.append(self.converter.convert_data('toCelcius', retrieve_data[1]))
		self.shorten_data_list(self.temperature_data)

		self.timestamp_record.append(retrieve_data[0].split()[1])
		self.shorten_data_list(self.timestamp_record)

		
	def Update(self):
		self.get_live_temperature()
		self.set_timestamp()
		return [self.temperature_data, self.timestamp_record]
