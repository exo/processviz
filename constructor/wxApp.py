# Imports.
import wx, wx.lib.ogl as ogl
import logging, logging.config

class wxApp(wx.App):
	def OnInit(self):
		# Import this after the wxApp has been created, as the config
		# object can then use the wx methods with impunity
		import poped
		ogl.OGLInitialize()
		frame = poped.Frame(
				parent=None, 
				title="POPEd", 
				size=(800, 600), 
				pos=(100,100))
		frame.Show()
		return True

# Setup Logging
logging.config.fileConfig('logging.conf')

# Start app.
app = wxApp(redirect=False)
app.MainLoop()
