class ChannelEnd (object):
	def __init__ (self, direction, name, datatype):
		self._direction, self._name, self._datatype = direction, name, datatype
	
	def get_name (self):
		return self._name
	name = property(get_name)
	
	def get_direction (self):
		return self._direction
	direction = property(get_direction)
	
	def get_datatype (self):
		return self._datatype
	datatype = property(get_datatype)