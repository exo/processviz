import sys
import os.path
from os.path import join, split

# See also:
#   http://www.wxpython.org/docs/api/wx.ConfigBase-class.html

def up(amnt, path):
	"""
	Remove some 'amnt' of path components from a path
	"""
	while amnt:
		path = split(path)[0]
		amnt -= 1
	return path	

class Conf(object):
	def __init__(self):
		self.base = up(1, os.path.abspath(sys.argv[0]))

	@property
	def templatePath(self):
		return join(self.base, 'constructor/resources')
	@property
	def systemBlockPath(self):
		return join(self.base, 'constructor/blocks')

class MacAppConfig(Conf):
	def __init__(self):
		pass
	@property
	def base(self):
		import wx
		sp = wx.StandardPaths.Get()
		return sp.GetResourcesDir()
	@property
	def templatePath(self):
		return join(self.base, 'resources')
	@property
	def systemBlockPath(self):
		return join(self.base, 'blocks')

class WinConfig(Conf):
	pass

Config = Conf()
if hasattr(sys, 'frozen'):
	if sys.frozen == 'macosx_app':
		Config = MacAppConfig()
	elif sys.frozen == 'windows_exe':
		Config = WinConfig()
	else:
		raise Exception('Wow! Unknown sys.frozen type')
