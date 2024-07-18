import kivy
kivy.require('1.7.2')

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.uix.popup import Popup

import zeep
from functools import partial
from re import search

from WeatherMonitor import weatherMonitor
from LiveRainfallMonitor import *
from LiveTemperatureMonitor import *
from LiveRainTempMonitor import *
from concreteSubject import *
from customGraph import *
from templateScreen import *
from dataFormatter import *

class workLiveScreen(templateScreen):
	
	def __init__(self, **kwargs):
		super(workLiveScreen, self).__init__(**kwargs)
		self.monitor_choice = ['Live Rainfall', 'Live Temperature', 'Live Rain and Temperature']
		self.monitor_object_type = {'Live Rain and Temperature': RainTempLiveMonitor, 'Live Rainfall': RainFallLiveMonitor, 'Live Temperature': TemperatureLiveMonitor}
		
		self.url = 'http://viper.infotech.monash.edu.au:8180/axis2/services/MelbourneWeatherTimeLapse?wsdl'
		self.client = zeep.Client(wsdl=self.url)
		self.location_list = self.client.service.getLocations()
		self.btn_holding_graph = None
		self.formatter = dataFormatter()

		# add options for choices of monitor type
		self.mainbutton_monitor_type.text = self.monitor_choice[2]
		for choice in self.monitor_choice:
			btn = Button(text=choice, size_hint_y=None, height=40)
			btn.bind(on_release=lambda btn: self.dropdown_monitor_type.select(btn.text))
			self.dropdown_monitor_type.add_widget(btn)
		
		# add options for location selection dropdown list
		self.mainbutton.text = self.location_list[0]
		for loc in self.location_list:
			btn = Button(text=loc, size_hint_y=None, height=40)
			btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
			self.dropdown.add_widget(btn)

		# modifying the title of navigation button
		self.navigate_btn.text = "Switch to Concrete"
		
		# pop up contains graph display
		self.graph = customGraph()
		self.popup_content = BoxLayout(orientation='vertical')
		self.popup_content.add_widget(self.graph.graph_canvas)
		self.remove_btn = Button(text='remove monitor', size_hint=(.2, .1))
		self.remove_btn.bind(on_press= self.remove)
		self.popup_content.add_widget(self.remove_btn)
		self.popup = Popup(title= 'Graph', content=self.popup_content, auto_dismiss=True, size_hint=(.8, .8))
		self.popup.dismiss()
		self.popup.bind(on_dismiss= self.reset_graph_state)

		# interval update schedule
		Clock.schedule_interval(self.interval_update, 20)

	def reset_graph_state(self, *args):
		self.btn_holding_graph = None
		# print self.btn_holding_graph

	def remove(self, *args):
		self.layout_line.remove_widget(self.btn_holding_graph)
		location = self.btn_holding_graph.text.split('\n')[1]
		# print location
		for item in self.monitor_button_dict[location]:
			if item == self.btn_holding_graph:
				del item
				break
		if not self.monitor_button_dict[location]:
			del self.monitor_button_dict[location]
			del templateScreen.subject_dict[location]
		self.btn_holding_graph = None
		self.popup.dismiss()

	'''
	override navigation function
	'''
	def navigation(self, *args):
		self.manager.current = 'monitor_screen'

	def add_location(self, *args):
		location = self.mainbutton.text
		monitor_type = self.mainbutton_monitor_type.text
		# location is created first time
		if location not in templateScreen.subject_dict.keys(): 
			# create new monitor
			new_monitor = self.monitor_object_type[monitor_type](self.client, location)
			# create new subject
			new_subject = concreteSubject(location)
			new_subject.attach(monitor_type, new_monitor)
			new_subject.count += 1
			data = self.formatter.format_data(new_monitor, new_monitor.Update())
			
			templateScreen.subject_dict[location] = new_subject
			# desc = self.format_button_content(location, data)

			new_btn = Button(id=str(new_subject.count),text=monitor_type + '\n' + location + '\n' + data[2][-1] , size_hint_y = None)
			new_btn.bind(on_press= partial(self.open_popup, location, new_btn))

			self.monitor_button_dict[location] = []
			self.button_dict_storage(new_btn, location)
			self.layout_line.add_widget(new_btn)
	
		else:
			subject = templateScreen.subject_dict[location]
			if monitor_type not in subject._live_observer_list.keys():				
				subject.count += 1
		
				new_btn = Button(id=str(subject.count),text='', size_hint_y = None)
				new_btn.bind(on_press=self.open_popup)

				new_monitor = self.monitor_object_type[monitor_type](self.client, location)
				data = self.formatter.format_data(new_monitor, new_monitor.Update())
				subject.attach(monitor_type, new_monitor)
				new_btn = Button(id=str(subject.count),text=monitor_type + '\n' + location + '\n' + data[2][-1] , size_hint_y = None)
				new_btn.bind(on_press= partial(self.open_popup, location, new_btn))
				self.button_dict_storage(new_btn, location)
				self.layout_line.add_widget(new_btn)


	def open_popup(self, location, button, *args):
		subject = templateScreen.subject_dict[location]
		monitor = None
		self.btn_holding_graph = button
		btn_title = button.text
		# find the correct monitor from the subject
		for item in subject._live_observer_list.values():
			if item.pattern.search(btn_title):
				monitor = item
				break
		# update the data
		data = monitor.Update()
		self.graph.update_data(data)
		self.popup.title = "Live weather from %s"% location
		self.popup.open()
		return
	
	def interval_update(self, *args):
		for location, subject in templateScreen.subject_dict.items():
			for obs_name, obs in subject._live_observer_list.items():
				data = obs.Update()
				for btn_object in self.monitor_button_dict[location]:
					btn_object.text = obs_name + '\n' + location + '\n' + data[2][-1]
					if btn_object == self.btn_holding_graph:
						self.graph.update_data(data)
				
