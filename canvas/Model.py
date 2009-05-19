
# Model.py
# Data model for Process Networks.

class ProcessNetwork (object):
	def __init__ (self):
		self._processes = []
		self._channels = []
		
	def get_processes (self): return self._processes
	processes = property(get_processes)
	
	def add_process (self, process): self._processes.append(process)
		
	def get_channels (self): return self._channels
	channels = property(get_channels)
	
	def add_channel (self, channel): self._channels.append(channel)
		
class Process (object):
	def __init__ (self, name, params, chan_ends, sub_network):
		self._name = name
		self._chan_ends = chan_ends
		self._sub_network = sub_network
		
	def get_name (self):
		return self._name

	name = property(get_name)

	def get_chan_ends (self):
		return self._chan_ends 
		
	chan_ends = property(get_chan_ends)
	
	def chan_end (self, name):
		for chan_end in self._chan_ends:
			if chan_end.name == name:
				return chan_end
		return None
	
	def chan_ends_by_direction (self, direction):
		chan_ends = []
		for chan_end in self._chan_ends:
			if chan_end.direction == direction:
				chan_ends.append(chan_end)
		return chan_ends
		
	def get_input_chan_ends (self):
		return self.chan_ends_by_direction('in')

	input_chan_ends = property(get_input_chan_ends)
	
	def get_output_chan_ends (self):
		return self.chan_ends_by_direction('out')

	output_chan_ends = property(get_output_chan_ends)
	
	def get_sub_network (self):
		return self._sub_network
	
	sub_network = property(get_sub_network)

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

class Channel (object):
	def __init__ (self, name, datatype, src, dest):
		self._name, self._datatype = name, datatype 
		self._src, self._dest = src, dest
	
	def get_src (self): return self._src
	src = property (get_src)
	
	def get_dest (self): return self._dest
	dest = property (get_dest)