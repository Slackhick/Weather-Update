__author__ = 'thvu11'

import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager

from welcomeScreen import welcomeScreen
from displayScreen import workScreen
from liveDisplayScreen import workLiveScreen


'''
App class contains a manager of all screens using in the monitor
for every new screen, it has to be added into screen manager widget in order to
traverse between screens
'''
class App(App):

	def build(self):
		
		screen_manager = ScreenManager()
		
		welcome_screen = welcomeScreen(name='welcome_screen')
		monitor_screen = workScreen(name='monitor_screen')
		monitor_live_screen = workLiveScreen(name='monitor_live_screen')

		screen_manager.add_widget(welcome_screen)
		screen_manager.add_widget(monitor_screen)
		screen_manager.add_widget(monitor_live_screen)
		
		# c = controller()
		return screen_manager
	
'''
running in command line: python -B driver.py
'''
if __name__ == '__main__':
	App().run()
