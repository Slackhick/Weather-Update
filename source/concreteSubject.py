import kivy
kivy.require('1.7.2')

from abstractSubject import abstractSubject

class concreteSubject(abstractSubject):
	def __init__(self, location):
		super(concreteSubject, self).__init__(location)
		self.state = 'waiting'
		self.count = 0

	'''
	return the current state of the monitor
	'''
	def getState(self):
		return self.state

	'''
	set the current state of the monitor and perform update on all observers
	@param: message - a string represeting the new state
	'''
	def setState(self, message):
		self.state = message
		return self.notify()

