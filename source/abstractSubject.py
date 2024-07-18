__author__ = 'thvu11'

import kivy
kivy.require('1.7.2')

from kivy.uix.screenmanager import Screen
from Observer import observer
from WeatherMonitor import weatherMonitor
from LiveWeatherMonitor import weatherLiveMonitor

class abstractSubject(object):
	def __init__(self, location):
		super(abstractSubject, self).__init__()
		self._observer_list = {}
		self._live_observer_list = {}
		self.location = location
		self.information = []
		return

	'''
	add a new observer to observer list
	@param: new_observer - an Observer object
	@return: True if new_observer is Observer object otherwise False
	'''
	def attach(self, obs_name, new_observer):
		if isinstance(new_observer, weatherMonitor):
			self._observer_list[obs_name] = new_observer
			return True
		elif isinstance(new_observer, weatherLiveMonitor):
			self._live_observer_list[obs_name] = new_observer
			return True
		else:
			return False

	'''
	remove an observer from observer list
	@note: dont know if we need this one, just put it here for future expansion
	'''
	def dettach(self, obs_name):
		try:
			if "Live" not in obs_name:
				del self._observer_list[obs_name]
			else:
				del self._live_observer_list[obs_name]
			return True
		except KeyError as e:
			print(e)
			return False

	'''
	update information on all observers
	'''
	def notify(self, *args):
		# print(1)
		for obs in self._observer_list.values():
			tmp = obs.Update()
			self.information.append(tmp)
		
		for obs in self._live_observer_list.values():
			obs.Update()

		return self.information
		

	

