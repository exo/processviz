class Channel (object):
	def __init__ (self, name, datatype, src, dest):
		self._name, self._datatype = name, datatype 
		self._src, self._dest = src, dest
	
	def get_src (self): return self._src
	src = property (get_src)
	
	def get_dest (self): return self._dest
	dest = property (get_dest)