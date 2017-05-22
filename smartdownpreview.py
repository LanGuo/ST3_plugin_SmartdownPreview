# Author: Lan Guo, Dan Keith
# Plug-in for sublime text 3, opens up a user defined URL for preview Smartdown content
# To enable SmartDown rendering, opens up http://smartdown.site using the 'url=' feature, embed data in a data URI

import sublime
import sublime_plugin
import webbrowser
import base64
import os
import pdb
from string import Template

useLocal = False

if useLocal:
	smartdownSiteURL = 'http://127.0.0.1:8080/lib/'
	smartdownModulePrefix = smartdownSiteURL
else:
	smartdownSiteURL = 'https://smartdown.site/'
	smartdownModulePrefix = 'https://smartdown.site/lib/'

class SmartdownpreviewCommand(sublime_plugin.TextCommand):  #sublime_plugin.EventListener):

	# if outputMode is 'html', save out an html file; if outputMode is 'dataURI', open a browser for preview using smartdown.site
	outputMode = 'html' #'dataURI'

	# Template location is within the same package, this is hard coded!
	html_template = os.path.join(os.path.expanduser("~"), 'Library', 'Application Support', 'Sublime Text 3', 'Packages', 'SmartDownPreview', 'smartdown_template.html')
	#this html template contains placeholder for title and content

	#def on_post_save(self, view):
	def run(self, edit):
		# saved file name, fullpath to the file being edited and saved
		self.currentFilePath = self.view.file_name()
		if self.currentFilePath.endswith('.md') or self.currentFilePath.endswith('.mmd'):
			#full_url = self.generate_url()
			#preview = self.openUrl(full_url)
			currentFileName = os.path.basename(self.currentFilePath)
			content = open(self.currentFilePath, "r", encoding='utf-8').read()
			self.previewFilePath = os.path.join(os.path.expanduser("~"), 'tmp')
			if not os.path.exists(self.previewFilePath):
				os.mkdir(self.previewFilePath)
			previewFileFullPath = os.path.join(self.previewFilePath, "{}.html".format(currentFileName))
			html_string = self.generate_html(
									title=currentFileName,
									content=content,
									smartdownSiteURL=smartdownSiteURL,
									smartdownModulePrefix=smartdownModulePrefix)
			self.save_tmp_file(html_string, outFilePath=previewFileFullPath)
			full_url = 'file://' + previewFileFullPath
			self.openUrl(full_url)

		else:
			self.log('This file is not SmartDown format!')
			pass

	def generate_html(self, title, content, smartdownSiteURL, smartdownModulePrefix):
		'''
		Generates an html file from template and current file content, saves it locally.
		'''
		html_template = open(self.html_template, "r").read()
		preview_html = Template(html_template).substitute(
							title=title,
							content=content,
							smartdownSiteURL=smartdownSiteURL,
							smartdownModulePrefix=smartdownModulePrefix)

		#pdb.set_trace()
		# Replace title and content in template with actual file we're editing
		# preview_html = html_template.replace('$title', title)
		# preview_html = preview_html.replace('$content', content)
		# preview_html = preview_html.replace('$smartdownSiteURL', smartdownSiteURL)
		# preview_html = preview_html.replace('$smartdownModulePrefix', smartdownModulePrefix)
		return preview_html

	def save_tmp_file(self, string, outFilePath):
		with open(outFilePath, 'w', encoding='utf-8') as outFile:
			outFile.write(string)


	def generate_url(self):
		# This is the base url for opening a smartdown preview on smartdown.site
		# This is hard coded!
		base_url = 'http://smartdown.site/?url=data:text/plain;charset=utf-8;base64,'
		data_uri = self.convert_current_file_to_uri()
		url = base_url + data_uri
		return url

	def convert_current_file_to_uri(self):
		current_file = self.currentFilePath
		data_uri = base64.b64encode(open(current_file, "rb").read())
		#str = open(current_file, "rb").read()
		#data64 = u''.join(base64.encodestring(str).splitlines())
		#mimetype = 'text/plain'
		#return u'data:%s;base64,%s' %(mimetype, data64)
		return data_uri.decode('utf-8')

	def openUrl(self, url):
		self.log('Opening '+url)
		webbrowser.open(url, new=0, autoraise=False)

	def log(self, msg):
		print(msg)
