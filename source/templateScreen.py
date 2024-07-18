import kivy
kivy.require('1.7.2')

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen


class templateScreen(Screen):
	subject_dict = {}
	def __init__(self, **kwargs):
		super(templateScreen, self).__init__(**kwargs)
		self.monitor_button_dict = dict()
		# display space
		self.layout_line = GridLayout(cols = 3, spacing = 20, padding = 20, size_hint_y = None)
		self.layout_line.bind(minimum_height=self.layout_line.setter('height'))

		self.scroll = ScrollView(size_hint=(1, 1.5))
		self.scroll.add_widget(self.layout_line)
		
		self.work_space = BoxLayout(orientation='vertical')
		self.work_space.add_widget(self.scroll)

		# button menu
		self.button_menu = BoxLayout(orientation='horizontal', size_hint_y = .2, spacing=10, padding=10)

		# drop down list for monitor type set up
		self.dropdown_monitor_type = DropDown()
		self.mainbutton_monitor_type = Button(text='Monitor type')
		self.mainbutton_monitor_type.bind(on_release=self.dropdown_monitor_type.open)
		self.dropdown_monitor_type.bind(on_select=lambda instance, x: setattr(self.mainbutton_monitor_type, 'text', x))

		# drop down list for location selection set up
		self.dropdown = DropDown()
		self.mainbutton = Button(text="location list insert")
		self.mainbutton.bind(on_release=self.dropdown.open)
		self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))

		# add button
		self.add_btn = Button(text="Add", background_color = (0, 0, 255, 1))
		self.add_btn.bind(on_press = self.add_location)

		# navigating button
		self.navigate_btn = Button(text="Switch to [destination]", background_color = (0, 0, 1, 255))
		self.navigate_btn.bind(on_press= self.navigation)

		# push all buttons into button menu
		self.button_menu.add_widget(self.add_btn)
		self.button_menu.add_widget(self.mainbutton_monitor_type)
		self.button_menu.add_widget(self.mainbutton)
		self.button_menu.add_widget(self.navigate_btn)

		# add button menu into work space layout
		self.work_space.add_widget(self.button_menu)

		# add work space layout to the screen
		self.add_widget(self.work_space)

	'''
	needs to override in child class
	choose the destination to navigate 
	'''
	def navigation(self, *args):
		pass

	def add_location(self, *args):
		pass

	def interval_update(self, *args):
		pass

	def button_dict_storage(self, btn_object, location):
		if location not in self.monitor_button_dict.keys():
			self.monitor_button_dict[location] = []
		self.monitor_button_dict[location].append(btn_object)



