from __future__ import with_statement

import wx
import model
from chan_end import ChanEnd
from util import AttrDict, MeasuringContext

class Process (model.Process):
    def __init__ (self, x, y, name, params=None, input_chans=[], output_chans=[], sub_network=None):
        model.Process.__init__(self, name, params,input_chans, output_chans, sub_network)
        self._x, self._y = x, y
        
        # Process style, will end up in YAML at some point.
        self.style = AttrDict (
            top             = (202, 214, 234),
            bottom          = (172, 192, 216),
            bottom_hi       = (255,255,255),
            shadow          = True,
            shadow_colour   = (218, 230, 242),
            shadow_offset   = 3,
            border          = ( 76,  76,  85),
            text_colour     = ( 44,  48,  52),
            v_pad           = 10,               # Vertical padding
            h_pad           = 10,               # Horizontal padding
            lbl_pad         = 2,                # Label padding
            cend_r          = 4.5,              # Radius of channel end.
            main_label      = 13,               # Font size of main label
            end_pad         = 5,
            expander_size   = 6,                # Expander widget size.
            expander_offset = 7,
        )

    def get_x (self): return self._x
    def set_x (self, x): self._x = x
    x = property(get_x, set_x)

    def get_y (self): return self._y
    def set_y (self, y): self._y = y
    y = property(get_y, set_y)
    
    def get_bounds (self):
        (w, h) = self.size
        if self.style.shadow:
            w, h = w + self.style.shadow_offset, h + self.style.shadow_offset
        return (self.x, self.y, self.x + w, self.y + h)
    bounds = property(get_bounds)
    
    def get_size (self):
        (w, h) = self.get_name_size(self.name)
        chan_end_w, chan_end_h = self.max_chan_end_size()
        # Width either the label, or the max of the channel ends.
        w = max(w, ((2 * chan_end_w) + self.style.h_pad))
        # Height sum of label and maximum ends height
        h += max(len(self.input_chans),len(self.output_chans)) * chan_end_h + self.style.v_pad
        
        return (w, h)
    size = property(get_size)

    def get_name_size (self, name):
        # Calculate size of process name & add outer padding.
        # TODO: This blows up on OS X right now, but should work.
        # gc = wx.GraphicsContext.CreateMeasuringContext()
        with MeasuringContext() as gc:
            gc.SetFont(gc.CreateFont(wx.Font(pointSize=self.style.main_label, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), self.style.text_colour))
            (w, h) = gc.GetTextExtent(name)
        w += (self.style.h_pad * 2)
        h += (self.style.v_pad * 2)
        return (w, h)
    
    def max_chan_end_size (self):
        sizes = [c.size for c in (self.input_chans + self.output_chans)]
        max_w = max([s[0] for s in sizes])
        max_h = max([s[1] for s in sizes])
        return (max_w, max_h)

    def on_paint (self, gc):
        self.draw_outer(gc)
        self.draw_name(gc)
        if self.input_chans is not []:
            x = (self.x + self.style.h_pad)
            y = (self.y + self.size[1]) - self.style.v_pad
            for c in self.input_chans:
                y -= self.max_chan_end_size()[1]
                c.on_paint(gc, (x,y))

    def draw_outer (self, gc):
        style = self.style
        (w, h) = self.size
        if style.shadow:
            path = gc.CreatePath()
            path.AddRectangle(self.x + style.shadow_offset, self.y + style.shadow_offset, w, h)
            gc.SetPen(wx.Pen(colour=style.shadow_colour, width=0))
            gc.SetBrush(gc.CreateBrush(wx.Brush(style.shadow_colour)))
            gc.DrawPath(path)
        
        # Outer rect.
        path = gc.CreatePath()
        path.AddRectangle(self.x, self.y, w, h)
        gc.SetPen(wx.Pen(colour=style.border, width=1))
        brush = gc.CreateLinearGradientBrush(self.x, self.y, self.x, self.y + h, style.top, style.bottom)
        gc.SetBrush(brush)
        gc.DrawPath(path)
        #self._path = path - for hit testing.
        
    def draw_name (self, gc):
        style = self.style
        (w, h) = self.size
        font = gc.CreateFont(wx.Font(pointSize=style.main_label, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), style.text_colour)
        gc.SetFont(font)
        (text_w, text_h) = gc.GetTextExtent(self.name)
        text_x = (self.x + (w/2)) - (text_w / 2)
        text_y = self.y + style.v_pad
        gc.DrawText(self.name, text_x, text_y)
    
    def hit_test (self, x, y):
        min_x, min_y, max_x, max_y = self.bounds
        if max_x > x > min_x and max_y > y > min_y:
            # Hit within process
            return self, (x - self.x, y - self.y)
        return None

    def add_chan_ends (self, chan_ends):
        for c in chan_ends:
            self.add_chan_end(c[0], c[1], c[2])

    def add_chan_end (self, name, direction, datatype):
        if direction == 'input':
            self.input_chans.append(ChanEnd(self, name, direction, datatype))
        elif direction == 'output':
            self.output_chans.append(ChanEnd(self, name, direction, datatype))
        #TODO: Error out here if the type is unknown.
