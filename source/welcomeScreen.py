__author__ = 'thvu11'

import kivy
kivy.require('1.7.2')

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import escape_markup


class welcomeScreen(Screen):
	def __init__(self, **kwargs):
		super(welcomeScreen, self).__init__(**kwargs)

		# layout for the screen
		layout = BoxLayout(orientation = 'vertical')

		# title of application
		label = Label(text='[size=70]Weather Monitor[/size]', markup= True, size_hint_y = .5)

		# start button
		btn = Button(text='>>>', size_hint = (.2, .1), pos_hint={'right':.6})
		btn.bind(on_press=self.change_screen)
		
		layout.add_widget(label)
		layout.add_widget(btn)
		layout.add_widget(Label(text="", size_hint_y = .3))
		self.add_widget(layout)

	def change_screen(self, *args):
		#navigate to the monitor screen
		self.manager.current = 'monitor_screen'


