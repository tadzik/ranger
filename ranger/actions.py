from ranger.shared import EnvironmentAware, SettingsAware

class Actions(EnvironmentAware, SettingsAware):
	def search_forward(self):
		if self.env.pwd:
			if self.env.pwd.search(self.env.last_search):
				self.env.cf = self.env.pwd.pointed_file

	def search_backward(self):
		if self.env.pwd:
			if self.env.pwd.search(self.env.last_search, -1):
				self.env.cf = self.env.pwd.pointed_file

	def interrupt(self):
		import time
		self.env.key_clear()
		try:
			time.sleep(0.2)
		except KeyboardInterrupt:
			raise SystemExit()

	def resize(self):
		self.ui.update_size()

	def exit(self):
		raise SystemExit()

	def enter_dir(self, path):
		self.env.enter_dir(path)

	def enter_bookmark(self, key):
		from ranger.container.bookmarks import NonexistantBookmark
		try:
			destination = self.bookmarks[key]
			current_path = self.env.pwd.path
			if destination != current_path:
				self.bookmarks.enter(key)
				self.bookmarks.remember(current_path)
		except NonexistantBookmark:
			pass

	def set_bookmark(self, key):
		self.bookmarks[key] = self.env.pwd.path

	def unset_bookmark(self, key):
		self.bookmarks.delete(key)

	def move_left(self):
		self.env.enter_dir('..')
	
	def move_right(self, mode = 0):
		cf = self.env.cf
		if not self.env.enter_dir(cf):
			self.execute_file(cf, mode = mode)

	def history_go(self, relative):
		self.env.history_go(relative)
	
	def handle_mouse(self):
		self.ui.handle_mouse()

	def execute_file(self, files, app = '', flags = '', mode = 0):
		if type(files) not in (list, tuple):
			files = [files]

		self.apps.get(app)(
				mainfile = files[0],
				files = files,
				flags = flags,
				mode = mode,
				fm = self,
				stdin = None,
				apps = self.apps)
	
	def edit_file(self):
		if self.env.cf is None:
			return
		self.execute_file(self.env.cf, app = 'editor')

	def open_console(self, mode = ':'):
		if hasattr(self.ui, 'open_console'):
			self.ui.open_console(mode)

	def move_pointer(self, relative = 0, absolute = None):
		self.env.cf = self.env.pwd.move_pointer(relative, absolute)

	def move_pointer_by_pages(self, relative):
		self.env.cf = self.env.pwd.move_pointer(
				relative = int(relative * self.env.termsize[0]))

	def scroll(self, relative):
		if hasattr(self.ui, 'scroll'):
			self.ui.scroll(relative)
			self.env.cf = self.env.pwd.pointed_file

	def redraw(self):
		self.ui.redraw()

	def reset(self):
		old_path = self.env.pwd.path
		self.env.directories = {}
		self.enter_dir(old_path)

	def toggle_boolean_option(self, string):
		if isinstance(self.env.settings[string], bool):
			self.env.settings[string] ^= True
