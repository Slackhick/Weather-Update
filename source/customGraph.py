__author__ = 'thvu11'


import kivy
kivy.require('1.7.2')

from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex as rgb

class customGraph:
	def __init__(self):
		self.graph_theme = {
                'label_options': {
                    'color': rgb('444444'),  # color of tick labels and titles
                    'bold': True},
                'background_color': rgb('b8b7bb'),  # back ground color of canvas
                'tick_color': rgb('808080'),  # ticks and grid
                'border_color': rgb('808080')}  # border drawn around each graph
		self.graph_canvas = BoxLayout(orientation='vertical', padding=5)
		self.graph_rain = Graph(ylabel = "rainfall(mm/s)", 
					y_grid_label=True, x_grid_label=True,
					xmin=0, xmax=10, ymin=0, ymax=5000,
					x_ticks_major=5, y_ticks_major=2500, 
					x_ticks_minor=1, y_ticks_minor = 100,
					x_grid=True, y_grid=True, padding=5, **self.graph_theme)

		self.graph_temp = Graph(ylabel = "temperature (C)", 
					y_grid_label=True, x_grid_label=True,
					xmin=0, xmax=10, ymin=0, ymax=50,
					x_ticks_major=5, y_ticks_major=25, 
					x_ticks_minor=1, y_ticks_minor = 5,
					x_grid=True, y_grid=True, padding=5, **self.graph_theme)

		self.plot_rain = MeshLinePlot(color=[0, 0, 1, 1])
		self.plot_temp = MeshLinePlot(color=[1, 0, 0, 1])
		

	def update_data(self, data):
		for item in data:
			print item		
		
		try:
			self.graph_rain.remove_plot(self.plot_rain)
			self.graph_canvas.remove_widget(self.graph_rain)
		except:
			pass
		
		try:
			self.graph_temp.remove_plot(self.plot_temp)
			self.graph_canvas.remove_widget(self.graph_temp)
		except:
			pass


		if data[0]:
			max_value = max(data[0])
			self.resize_graph(self.graph_rain, max_value)
			self.plot_rain.points = [(float(x), float(y)) for x, y in enumerate(data[0])]
			self.graph_rain.add_plot(self.plot_rain)
			self.graph_canvas.add_widget(self.graph_rain)
		if data[1]:		
			self.plot_temp.points = [(float(x), float(y)) for x, y in enumerate(data[1])]
			self.graph_temp.add_plot(self.plot_temp)
			self.graph_canvas.add_widget(self.graph_temp)

	def resize_graph(self, graph, value):
		# print "value" + str(self.graph_rain.ymax)
		self.graph_rain.ymax = int(value) + 10
		self.graph_rain.y_ticks_major = int(self.graph_rain.ymax / 2)

	def get_graph(self):
		return self.graph_canvas

