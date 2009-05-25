class ChanEnd (object):
	def __init__ (self, name, direction, datatype):
		self._name, self._direction, self._datatype = name, direction, datatype
	
	def get_name (self):
		return self._name
	name = property(get_name)
	
	def get_direction (self):
		return self._direction
	direction = property(get_direction)
	
	def get_datatype (self):
		return self._datatype
	datatype = property(get_datatype)