
# DisplayObjects.py
# Visual representations extending each model object to make them draw-able.

import wx
import math

# Data models
from Model import *

class ProcessNetworkDisplay (ProcessNetwork):
	def __init__ (self, x=0, y=0):
		self._x, self._y = x, y
		self._style = {
			'padding'			: 5,		# Amount that the network diagram should be padded.
			'background'	: (255,255,255),
			'border'			: (172, 192, 216)
		}

		ProcessNetwork.__init__(self)
	
	def get_x (self): return self._x
	def set_x (self, x): self._x = x
	x = property(get_x, set_x)
	
	def get_y (self): return self._y
	def set_y (self, y): self._y = y
	y = property(get_y, set_y)
	
	def on_paint (self, gc):
		style = self._style
		#print "Translating to %s, %s" % (self._x, self._y)
		gc.PushState() # Save current translation
		
		gc.Translate(self.x, self.y) # Set new translation
		# TODO draw a background rounded rect at the borders.
		self.update_size()
		self.draw_background(gc)
		
		for process in self.processes:
			process.on_paint(gc)
		
		for channel in self.channels:
			channel.on_paint(gc)
		
		gc.PopState() # Restore last translation
		
	def draw_background (self, gc):
		style = self._style
		(w, h) = self.get_size()
		path = gc.CreatePath()
		path.AddRectangle(0, 0, w, h)
		gc.SetPen(wx.Pen(colour=style['border'], width=1))
		gc.SetBrush(gc.CreateBrush(wx.Brush(style['background'])))
		gc.DrawPath(path)
		
	def hit_test (self, x, y):
		for process in self.processes:
			result = process.hit_test(x - self._x, y - self._y)
			if result is not None:
				return result
		return None

	def get_bounds (self):
		style = self._style
		if len(self.processes) > 1:
			p = self.processes[0]
			# Start searching from these values.
			x1, x2 = p.x, p.x + p.width
			y1, y2 = p.y, p.y + p.height
			
			for p in self.processes:
				x1, x2 = min(x1, p.x), max(x2, p.x + p.width)
				y1, y2 = min(y1, p.y), max(y2, p.y + p.height)
						
		print "Bounds: %s,%s to %s,%s" % (x1, y1, x2, y2)
		
		# Update co-ords
		return (x1, y1, x2, y2)
		
	def get_size (self):
		style = self._style
		(x1, y1, x2, y2) = self.get_bounds()
		
		# Width.
		if x1 < 0:
			if x2 < 0:
				w = abs(x1 - x2)
			else:
				w = abs(x1) + x2
		else:
			w = x2 - x1
		
		# Height
		if y1 < 0:
			if y2 < 0:
				h = abs(y1 - y2)
			else:
				h = abs(y1) + y2
		else:
			h = y2 - y1
		#print "Size is: %s,%s" % (w,h)
		return (w + (2*style['padding']),h+(2*style['padding']))
	
	def update_size (self):
		(x1, y1, x2, y2) = self.get_bounds()
 		print "Setting origin to: %s, %s" % (x1, y1)
		#self._x, self._y = x1, y1
		
		# TODO: Make sure we deal with negative coords to get an absolute bound.
		
class ChannelEndDisplay (ChannelEnd):
	def __init__ (self, x, y, direction, name, datatype):
		ChannelEnd.__init__(self, direction, name, datatype)
		# Process style, will end up in YAML at some point.
		self._style = {
		'shadow'	: (218, 230, 242),
		'fill'		: (218, 230, 242),
		'hilight' : (171, 75, 75),
		's_offset': 5,
		'border'	: ( 76,  76,  85),
		'cend_r'	: 4.5,								# Radius of channel end.
		'chan_label' : 11,							# Font size of chan label
		'text'		: ( 44,  48,  52),		# Text color for chan label
		'h_pad'		: 10,									# Horizontal padding
		'end_offset'  : 1,									# Relation of channel end to text.
		
		}
		
		self._x, self._y = x, y
		self._w, self._h = 0, 0
				
		# Path for hit testing.
		self._path = None
	
	# x, y coordinate property things.
	def get_x (self): return self._x
	def set_x (self, x): self._x = x
	x = property (get_x, set_x)
	
	def get_y (self): return self._y
	def set_y (self, y): self._y = y
	y = property (get_y, set_y)
	
	def get_size (self): return self._w, self._h
 	def set_size (self, w, h): self._w, self._h = w, h
	size = property (get_size, set_size)
	
	def get_h (self): return self._h
	h = property (get_h)
	
	def update_size (self, gc):
		# This wouldn't be neccessary if we could use the static context.
		style = self._style
		font = gc.CreateFont(wx.Font(pointSize=style['chan_label'], family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), style['text'])
		gc.SetFont(font)
		label_w, label_h = gc.GetTextExtent(self.name)
		self.set_size(label_w, label_h)

	def on_paint (self, gc):
		# Label
		self.update_size(gc)
		
		style = self._style
		x, y = self._x, self._y
		w, h = self._w, self._h
		
		if self.direction == 'in':
			label_x = x + style['h_pad']
			label_y = y - (h/2)
		
		elif self.direction == 'out':
			label_x = x - w - style['h_pad']
			label_y = y - (h/2)
				
		gc.DrawText(self.name, label_x, label_y)		
		
		# Shadow?.
		if self.direction == 'out':
			path = gc.CreatePath()
			path.AddCircle(x + style['s_offset'], y + style['s_offset'] + style['end_offset'], style['cend_r'])
			gc.SetPen(wx.Pen(colour=style['shadow'], width=0))
			gc.SetBrush(gc.CreateBrush(wx.Brush(style['shadow'])))
			gc.DrawPath(path)

		# Figure.
		path = gc.CreatePath()
		path.AddCircle(x, y+style['end_offset'], style['cend_r'])
		gc.SetPen(wx.Pen(colour=style['border'], width=1))
		gc.SetBrush(gc.CreateBrush(wx.Brush(style['fill'])))
		gc.DrawPath(path)
		self._path = path
	
	def hit_test (self, x, y):
		if self._path.Contains(x, y):
			return self
		return None
	
	def toggle (self):
		style = self._style
		style['fill'], style['hilight'] = style['hilight'], style['fill']
	
class ProcessDisplay (Process):
	def __init__ (self, x, y, name, params, chan_ends, sub_network=None):
		Process.__init__(self, name, params, chan_ends, sub_network)
		
		# Process style, will end up in YAML at some point.
		self._proc_style = {
		'top'			: (202, 214, 234),
		'bottom'	: (172, 192, 216),
		'bottom_hi' : (255,255,255),
		'shadow'	: (218, 230, 242),
		's_offset': 5,
		'border'	: ( 76,  76,  85),
		'text'		: ( 44,  48,  52),
		'v_pad' 	: 10,									# Vertical padding
		'h_pad'		: 10,									# Horizontal padding
		'lbl_pad' : 2,									# Label padding
		'cend_r'	: 4.5,								# Radius of channel end.
		'main_label' : 13,							# Font size of main label
		'end_pad'	: 5,
		'expander_size' : 6,						# Expander widget size.
		'expander_offset' : 7
		}
		
		# Geometry
		(self._x, self._y) = (x, y)
		(self._width, self._height) = (0, 0)
		
		# Hierarchy
		self.is_expanded = False

	# x, y coordinate property things.
	def get_x (self): return self._x
	def set_x (self, x): self._x = x
	x = property (get_x, set_x)

	def get_y (self): return self._y
	def set_y (self, y): self._y = y
	y = property (get_y, set_y)
	
	# Width & Height.
	def get_width (self): return self._width
	width = property (get_width)
	
	def get_height (self): return self._height
	height = property (get_height)
	
	def on_paint(self, gc):

		(self._width, self._height) = self.calculate_size(gc)
		self.draw_shadow(gc)
		self.draw_outline(gc)
		self.draw_name(gc)
		self.draw_expander(gc)
		if self.sub_network is not None:
			self.sub_network.on_paint(gc)		
		self.draw_channel_ends(gc)
		
	
	def calculate_size (self, gc):
		style = self._proc_style
		# Calculate size of process name & add outer padding.
		gc.SetFont(gc.CreateFont(wx.Font(pointSize=style['main_label'], family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), style['text']))
		(name_w, name_h) = gc.GetTextExtent(self.name)
		w = name_w + self._proc_style['h_pad']*2
		h = name_h +  self._proc_style['v_pad']

		# Calculate size of channel labels for input & output.
		max_in_w, max_in_h = self.max_chan_label_size(gc, self.input_chan_ends)
		max_out_w, max_out_h = self.max_chan_label_size(gc, self.output_chan_ends)
		
		# Add padding (edges & separation)
		target_w = max_in_w + max_out_w + (3 * self._proc_style['h_pad'])
		
		# Generate a max height for each channel 'row' with padding.
		max_chans =  max(len(self.input_chan_ends), len(self.output_chan_ends))
		
		input_chans_height = output_chans_height = 0
		for chan_end in self.input_chan_ends:
			input_chans_height += chan_end.h + style['end_pad']
		for chan_end in self.output_chan_ends:
			output_chans_height += chan_end.h + style['end_pad']
		
		chan_height = max(input_chans_height, output_chans_height) + style['v_pad'] + style['end_pad']

		# Max of either the label width, or combined label widths
		w = max(w, target_w)
		# Name height plus appropriate number of channel rows.
		h += chan_height
		
		# Now add a space for the sub-network, if appropriate.
		if self.sub_network is not None:
			sub_w, sub_h = self.sub_network.get_size()
			w, h = max(w, sub_w + 2*style['h_pad']), name_h + sub_h +chan_height + 2*style['h_pad']
			
			self.sub_network.x = self.x + style['h_pad']
			self.sub_network.y = self.y + name_h + (style['v_pad'] * 2)
			
		return (w, h)
		
		
	def draw_expander (self, gc):
		pass
	
	def max_chan_label_size(self, gc, chan_ends):
		max_w = max_h = 0
		for chan_end in chan_ends:
			chan_end.update_size(gc)
			(w, h) = chan_end.get_size()
			max_w, max_h = max(max_w, w), max(max_h, h)
		return max_w, max_h

	def draw_shadow (self, gc):
		path = gc.CreatePath()
		path.AddRectangle(self._x + self._proc_style['s_offset'], self._y + self._proc_style['s_offset'], self._width, self._height)
		gc.SetPen(wx.Pen(colour=self._proc_style['shadow'], width=0))
		gc.SetBrush(gc.CreateBrush(wx.Brush(self._proc_style['shadow'])))
		gc.DrawPath(path)
	
	def draw_outline (self, gc):
		path = gc.CreatePath()
		path.AddRectangle(self._x, self._y, self._width, self._height)
		gc.SetPen(wx.Pen(colour=self._proc_style['border'], width=1))
		brush = gc.CreateLinearGradientBrush(self._x, self._y, self._x, self._y + self._height, self._proc_style['top'], self._proc_style['bottom'])
		gc.SetBrush(brush)
		gc.DrawPath(path)
		self._path = path
		
	def draw_name (self, gc):
		font = gc.CreateFont(wx.Font(pointSize=self._proc_style['main_label'], family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), self._proc_style['text'])
		gc.SetFont(font)
		(text_w, text_h) = gc.GetTextExtent(self._name)
		text_x = (self._x + (self._width/2)) - (text_w / 2)
		text_y = self._y + self._proc_style['v_pad']
		gc.DrawText(self._name, text_x, text_y)
		
	def draw_channel_ends (self, gc):
		style = self._proc_style
		x, y = self._x, self._y
		w, h = self._width, self._height
		
		# Inputs
		end_x = x 
		end_y = (y + h) - (style['v_pad'] + style['end_pad'])
				
		for chan_end in self.input_chan_ends:
			chan_end.x, chan_end.y = end_x, end_y
			end_y -= chan_end.size[1] + style['end_pad']
			chan_end.on_paint(gc)
		
		# Outputs
		end_x = (x + w)
		end_y = (y + h) - (style['v_pad'] + style['end_pad'])
			
		for chan_end in self.output_chan_ends:
			chan_end.x, chan_end.y = end_x, end_y
			end_y -= chan_end.size[1] +  + style['end_pad']
			chan_end.on_paint(gc)

	def hit_test(self, x, y):
		# Sub processes
		if self.sub_network is not None:
			result = self.sub_network.hit_test(x, y)
			if result is not None:
				return result

		# First channel ends.
		for chan_end in self.chan_ends:
			result = chan_end.hit_test(x, y)
			if result is not None:
				return chan_end
		
		# Now ourselves.
		result = self._path.Contains(x, y)
		if result:
			return self
		return None
		
	def get_channel_location(self, channel_name):
		for name in self._channels_in:
			if name == channel_name:
				return (self._channels_in[name]['x'] - self._proc_style['cend_r'], self._channels_in[name]['y'])
		for name in self._channels_out:
			if name == channel_name:
				return (self._channels_out[name]['x'] + self._proc_style['cend_r'], self._channels_out[name]['y'])
		#print "Channel location for %s not found in %s or %s!" % (name, self._channels_in, self._channels_out)
		return (0, 0)
	
	def toggle (self):
		self._proc_style['bottom'], self._proc_style['bottom_hi'] =  self._proc_style['bottom_hi'], self._proc_style['bottom']

class ChannelDisplay (Channel):
	def __init__ (self, name, datatype, src, dest):
		Channel.__init__(self, name, datatype, src, dest)
		self._style = {
		'colour'			: (150, 150, 150),
		'radius'			: 10,
		'arrow_size'	: (4, 4),
		'cend_r'			: 4.5 		# Source this from the channel end code later.
		}

	def on_paint (self, gc):
		style = self._style
		src, dest = self.src, self.dest
		#diameter = 2*radius
		r = style['radius']
		
		gc.SetPen(wx.Pen(colour=style['colour'], width=1))
		path = gc.CreatePath()
		path.MoveToPoint(src.x + style['cend_r'], src.y)

		#print "Dest: %s Src: %s" % (dest_y, src_y)
		if dest.x > src.x:
			# Left to right drawing.
			mid_x = src.x + (dest.x - src.x)/2
			if abs(dest.y - src.y) < r:
				path.AddLineToPoint(dest.x - r, dest.y)
			elif dest.y > src.y:
				# Is the target point lower than the source?
				path.AddLineToPoint((mid_x-r), src.y)
				center = (mid_x - r, src.y + r)
				path.AddArc(center, r, math.radians(270), math.radians(0))
				path.AddLineToPoint(mid_x, max(dest.y - (2*r), src.y))
				center = (mid_x + r, dest.y - r)
				path.AddArc(center, r, math.radians(180), math.radians(90), False)
			else:
				path.AddLineToPoint((mid_x-r), src.y)
				center = (mid_x - r, src.y - r)
				path.AddArc(center, r, math.radians(90), math.radians(0), False)
				path.AddLineToPoint(mid_x, min(dest.y + (2*r), src.y))
				center = (mid_x + r, dest.y + r)
				path.AddArc(center, r, math.radians(180), math.radians(270))
				
			path.AddLineToPoint(dest.x - style['cend_r'], dest.y)	
		
		else:
			# Right to left drawing.
			offset = max((src.x - dest.x)/6, 2*r)
			outer_right_x = src.x + offset
			outer_left_x = dest.x - offset
			lower_y = max(src.y, dest.y) + offset
						
			path.AddLineToPoint(outer_right_x-r, src.y)
			center = (outer_right_x - r, src.y + r)
			path.AddArc(center, r, math.radians(270), math.radians(0))
			path.AddLineToPoint(outer_right_x, lower_y - r)
			center = (outer_right_x - r, lower_y - r)
			path.AddArc(center, r, math.radians(0), math.radians(90))
			path.AddLineToPoint(outer_left_x + r, lower_y)
			center = (outer_left_x + r, lower_y - r)
			path.AddArc(center, r, math.radians(90), math.radians(180))
			path.AddLineToPoint(outer_left_x, dest.y + r)
			center = (outer_left_x + r, dest.y + r)
			path.AddArc(center, r, math.radians(180), math.radians(270))
			path.AddLineToPoint(dest.x - style['cend_r'], dest.y)

		# Arrow head.
		arrow_size = style['arrow_size']
		path.AddLineToPoint(dest.x - style['cend_r'] - arrow_size[0], dest.y - arrow_size[1])
		path.MoveToPoint(dest.x - style['cend_r'], dest.y)
		path.AddLineToPoint(dest.x - style['cend_r'] - arrow_size[0], dest.y + arrow_size[1])
		gc.StrokePath(path)
