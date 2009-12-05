# wxPython
import wx, wx.lib.ogl as ogl, wx.lib.pubsub as pubsub

# Logging
import logging
log = logging.getLogger("popedLogger");

# Pickle
try:
	import cPickle as pickle
except ImportError:
	import pickle

# Project dependencies.


class ProcessDiagram (ogl.Diagram):
	def __init__ (self, parent, view=None):
		ogl.Diagram.__init__(self) #TODO: What's Python's equiv of super() ?
		canvas = ogl.ShapeCanvas(parent)
		self.processes = []
		
		# Canvas Init.
		self.SetCanvas(canvas)
		canvas.SetDiagram(self)
		canvas.SetBackgroundColour('WHITE')
		# TODO: Set width/height (400, 200)
		canvas.SetDropTarget(CanvasDropTarget(self))
		wx.EVT_MOUSE_EVENTS(canvas, self.OnMouseEvent)
		log.debug("Finished Canvas initialisation")
		
	def OnMouseEvent (self, event):
		# TODO: Could get event position here?
		self.GetCanvas().OnMouseEvent(event)
		
	def AddProcess (self, name, location, cin_ends, cout_ends):
		p = Process(name, location, cin_ends, cout_ends)
		p.AddToCanvas(self.GetCanvas())
		p.Show(True)
		self.processes.append(p)
		for channel_end in p.GetChannelEnds():
			channel_end.AddToCanvas(self.GetCanvas())
			channel_end.Show(True)

	def Update ():
		for process in self.processes:
			process.AddToCanvas(self.GetCanvas())
			for channel_end in process.GetChannelEnds():
				channel_end.AddToCanvas(self.GetCanvas())
	
	# TODO: Uses of this should probably be diagram.getView().MoveProcess()
	def MoveProcess (self, process, p_x, p_y):
		#self.view.MoveProcess(process, p_x, p_y)
		pass 

class Process (ogl.RectangleShape):
	def __init__ (self, name, location, cin_ends, cout_ends):
		# Dimensions & Location.
		width = 100
		max_chan_ends = max(len(cin_ends), len(cout_ends))
		height = 20 * max_chan_ends
		
		# Never make a 20 unit high process..
		if height == 20:
			height = 40

		# Init superclass.
		ogl.RectangleShape.__init__(self, width, height)

		# Appearance.
		self.SetPen(wx.BLACK_PEN)
		self.SetBrush(wx.WHITE_BRUSH)
		self.AddText(name)
		self.SetAttachmentMode(ogl.ATTACHMENT_MODE_EDGE)
		self.SetDraggable(True, True)

		self.x, self.y = location
		self.SetX(self.x)
		self.SetY(self.y)

		# Properties.
		self.cin_ends = cin_ends
		self.cout_ends = cout_ends
		self.width = width
		self.height = height
		
		self.channel_end_shapes = []
		self.CreateChannelEnds()
		log.info("Process name: %s x: %s y: %s w: %s h: %s cin: %s cout: %s" % (name, self.x, self.y, width, height, cin_ends, cout_ends))
		
	def OnDraw (self, dc):
		ogl.RectangleShape.OnDraw(self, dc)
		self.UpdateChannelEnds()
		
	def CreateChannelEnds(self):

		c_end_width = c_end_height = 20
		# Input starts at the left bottom corner.
		x_offset = ((self.width/2) - (c_end_width/2))
		y_offset = (self.height/2) - (c_end_height/2)
		
		log.debug ("Number of input channels: %s content: %s" % (len(self.cin_ends), self.cin_ends))
		for cin_end in self.cin_ends:
			self.channel_end_shapes.append(ChannelEnd(cin_end['name'], cin_end['type'], (self.GetX(), self.GetY()), (-x_offset, y_offset)))
			y_offset -= c_end_height
		
		# Output starts at the right bottom corner.
		x_offset = (self.width/2) - (c_end_width/2)
		y_offset = (self.height/2) - (c_end_height/2)
		
		log.debug ("Number of output channels: %s content: %s" % (len(self.cout_ends), self.cout_ends))
		for cout_end in self.cout_ends:
			self.channel_end_shapes.append(ChannelEnd(cout_end['name'], cout_end['type'], (self.x, self.y), (x_offset, y_offset)))
			y_offset -= c_end_height
 	
	def GetChannelEnds(self):
		return self.channel_end_shapes
	
	def UpdateChannelEnds(self):
		location = (self.GetX(), self.GetY())
		for c_end in self.channel_end_shapes:
			c_end.Update(location)
		log.debug("Updated channel end positions with process at %s, %s" % (self.x, self.y))

class ChannelEnd (ogl.RectangleShape):
	def __init__ (self, name, type, location, offset):
		width = height = 20
		ogl.RectangleShape.__init__(self, width, height)
		x_offset, y_offset = offset
		proc_x, proc_y = location
		
		# Properties
		self.name = name
		self.type = type
		
		self.SetPen(wx.Pen((150,150,150)))
		self.SetBrush(wx.Brush((200,200,200)))
		
		# Calculate location.
		self.x = proc_x + x_offset
		self.y = proc_y + y_offset
		
		# Store offsets (for recalculation)
		self.x_offset = x_offset
		self.y_offset = y_offset
		
		# Set location
		self.SetX(self.x)
		self.SetY(self.y)
		
		self.SetDraggable(True, False)
	
	def Update(self, location):
		# Calculate location.
		proc_x, proc_y = location
		old_x = self.x
		old_y = self.y
		self.x = proc_x + self.x_offset
		self.y = proc_y + self.y_offset
		
		# Set location
		self.SetX(self.x)
		self.SetY(self.y)
		
class BlockDropData(wx.PyDataObjectSimple):
	def __init__(self):
		wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('BlockData'))
	
	def GetDataSize(self):
		return len(self.data)

	def GetDataHere(self):
		return self.data
		
	def SetData(self, data):
		self.data = data
		return True

class CanvasDropTarget(wx.PyDropTarget):
	def __init__(self, diagram):
		wx.PyDropTarget.__init__(self)
		self.b = BlockDropData()
		self.SetDataObject(self.b)
		self.diagram = diagram

	def OnDrop (self, x, y):
		pass
	
	def OnEnter(self, x, y, d):
		return d
	
	def OnLeave(self):
		pass
		
	def OnDrop(self, x, y):
		pass
		
	def OnDragOver(self, x, y, d):
		return d
	
	def OnData (self, x, y, d):
		#print "OnData", x, y, d
		if self.GetData():
			data = self.b.GetDataHere()
			data = pickle.loads(data)
			#print type(data)
			
			self.diagram.AddProcess(data['name'], (x, y), data['input'], data['output'])
			self.diagram.GetCanvas().Refresh()
		log.debug("Completed OnData for Canvas droptarget.")
		return d
