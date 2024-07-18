__author__ = 'thvu11'


import kivy
kivy.require('1.7.2')

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

import zeep
import time
from functools import partial
from re import search

from WeatherMonitor import weatherMonitor
from RainfallMonitor import *
from TemperatureMonitor import *
from RainTempMonitor import *
from concreteSubject import *
from templateScreen import *

class workScreen(templateScreen):
	
	def __init__(self, **kwargs):
		super(workScreen, self).__init__(**kwargs)
		self.monitor_choice = ['Rain', 'Temperature', 'Rain and Temperature']
		self.monitor_object_type = {'Rain and Temperature': RainTempMonitor, 'Rain': RainFallMonitor, 'Temperature': TemperatureMonitor}
		# retrieve the locations from the server
		self.url = 'http://viper.infotech.monash.edu.au:8180/axis2/services/MelbourneWeather2?wsdl'
		self.client = zeep.Client(wsdl=self.url)
		self.location_list = self.client.service.getLocations()
		
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
		self.navigate_btn.text = "Switch to Live"
		
		
		# interval update schedule
		Clock.schedule_interval(self.interval_update, 300)

	
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
			data = location + '\n' + new_monitor.Update()
			
			templateScreen.subject_dict[location] = new_subject
			# desc = self.format_button_content(location, data)

			new_btn = Button(id=str(new_subject.count),text=data , size_hint_y = None)
			new_btn.bind(on_press= partial(self.remove_monitor, location, str(new_subject.count)))
			self.monitor_button_dict[location] = []
			self.button_dict_storage(new_btn, location)
			
			self.layout_line.add_widget(new_btn)
		else:
			# same location is requested -> create a new button object
			subject = templateScreen.subject_dict[location]
			subject.count += 1
			
			new_btn = Button(id=str(subject.count),text='', size_hint_y = None)
			new_btn.bind(on_press=partial(self.remove_monitor, location, str(subject.count)))

			# same monitor type -> get data from the monitor
			if monitor_type in subject._observer_list.keys():
				if time.time() - subject._observer_list[monitor_type].latest_timestamp >= 300:
					data = subject._observer_list[monitor_type].Update()
					new_btn.text = location + '\n' + data
					self.update_multiple_button(location, subject, monitor_type, data)
				else:
					new_btn.text = location + '\n' + subject._observer_list[monitor_type].content
					# print 'get latest update'
				self.button_dict_storage(new_btn, location)
				self.layout_line.add_widget(new_btn)
			else:
				# different monitor type -> attach new monitor to subject + get data
				new_monitor = self.monitor_object_type[monitor_type](self.client, location)
				subject.attach(monitor_type, new_monitor)
				new_btn.text = location + '\n' + subject._observer_list[monitor_type].Update()
				self.button_dict_storage(new_btn, location)
				self.layout_line.add_widget(new_btn)
	

	def update_multiple_button(self, location, subject, monitor_type, data):
		for btn_object in self.monitor_button_dict[location]:
			if subject._observer_list[monitor_type].pattern.search(btn_object.text):
				# print btn_object.id + 'updated'
				btn_object.text = location + '\n' + data

	def remove_monitor(self, location, index, *args):
		# each button has a unique ID -> traverse through the list and delete chosen ID
		for btn_object in self.monitor_button_dict[location]:
			if btn_object.id == index:
				self.layout_line.remove_widget(btn_object)
				# print btn_object.id
				del btn_object
				break
		# no button for the subject = delete subject
		if not self.monitor_button_dict[location]:
			del self.monitor_button_dict[location]
			del templateScreen.subject_dict[location]
		return

	def interval_update(self, *args):
		# print 'success'
		start_time = time.time()
		for location, subject in templateScreen.subject_dict.items():
			for obs_name, obs in subject._observer_list.items():
				if start_time - obs.latest_timestamp >= 300:
					data = obs.Update()
					self.update_multiple_button(location, subject, obs_name, data)

	'''
	override navigation function
	'''
	def navigation(self, *args):
		self.manager.current = 'monitor_live_screen'




