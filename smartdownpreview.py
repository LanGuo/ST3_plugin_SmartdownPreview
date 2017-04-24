# Based on OpenInBrowser: https://bitbucket.org/bteryek/openinbrowser
# On save opens up a user defined URL
# To enable SmartDown rendering, opens up http://smartdown.site using the 'url=' feature, embed data in a data URI

import sublime, sublime_plugin, webbrowser, base64

class SmartdownpreviewCommand(sublime_plugin.TextCommand):  #sublime_plugin.EventListener):

	#def on_post_save(self, view):
	def run(self, edit):
		# saved file name, fullpath to the file being edited and saved
		self.savedFileName = self.view.file_name()
		if self.savedFileName.endswith('.md') or self.savedFileName.endswith('.mmd'):
			full_url = self.generate_url()

			preview = self.openUrl(full_url)
			if not preview:
				self.log('Smart down preview cannot be opened')

		else:
			self.log('This file is not SmartDown format!')
			pass
	

	def generate_url(self):
		# This is the base url for opening a smartdown preview on smartdown.site
		# This is hard coded!
		base_url = 'http://smartdown.site/?url=data:text/plain;charset=utf-8;base64,'
		data_uri = self.convert_current_file_to_uri()	
		url = base_url + data_uri	
		return url

	def convert_current_file_to_uri(self):
		current_file = self.savedFileName
		data_uri = base64.b64encode(open(current_file, "rb").read())
		#str = open(current_file, "rb").read()
		#data64 = u''.join(base64.encodestring(str).splitlines())
		#mimetype = 'text/plain'
		#return u'data:%s;base64,%s' %(mimetype, data64)
		return data_uri.decode('utf-8')

	def openUrl(self, url):
		self.log('Opening '+url)
		webbrowser.open(url, new=2, autoraise=False)

	def log(self, msg):
		print(msg)
