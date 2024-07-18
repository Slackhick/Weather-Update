'''
The converter for data of Live Weather Monitor
'''

class dataConverter:
	def __init__(self):
		self.converter_method_dict = {'toCelcius': self.to_celcius,
						'toMilimetre': self.to_milimetre}

	def to_celcius(self, number):
		return (float(number)) - 273.15

	def to_milimetre(self, number):
		return float(number) * 1000


	def convert_data(self, new_format, number):
		return self.converter_method_dict[new_format](number)

