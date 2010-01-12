from __future__ import with_statement
from canvas.util import AttrDict, MeasuringContext

import wx
from canvas import model

import logging
log = logging.getLogger("popedLogger");

class ChanEnd (model.ChanEnd):
    
    def __init__ (self, name, direction, datatype):
        model.ChanEnd.__init__(self, name, direction, datatype)
        self.style = AttrDict (
            fill            = (218, 230, 242),
            hilight         = (171,  75,  75),
            border          = ( 76,  76,  85),
            shadow          = True,
            shadow_colour   = (218, 230, 242),
            shadow_offset   = 3,
            radius          = 4.5,                             
            text_size       = 11,
            text_colour     = ( 44,  48,  52),
            pad             = 10,
            offset          = 1, # Relation of channel end to text?
        )

    def get_bounds (self, x, y):
        """Return the bounding box (x0, y0, x1, y1), given the current position"""
        (w, h) = self.size
        style = self.style
        if self.direction == 'input':
            x0 = x - style.radius
            y0 = y - style.radius
            x1, y1 = x + w, y + (h/2)
            if style.shadow:
                x0 -= style.shadow_offset
                y0 -= style.shadow_offset
        elif self.direction == 'output':
            x0 = x - w
            y0 = y - (h/2)
            x1, y1 = x + style.radius, y + style.radius
            if style.shadow:
                x1 += style.shadow_offset
                y1 += style.shadow_offset
        return (x0, y0, x1, y1)

    def draw_bounds (self, gc, x, y):
        """Debug function to draw a box showing the channel end's outline"""
        (x0, y0, x1, y1)= self.get_bounds(x, y)
        w, h = x1 - x0, y1 - y0
        p = gc.CreatePath()
        p.AddRectangle(x0, y0, w, h)
        gc.SetPen(wx.Pen(colour=(0,0,0), width=1))
        gc.DrawPath(p)

    def get_size (self):
        (w, h) = self.get_label_size()
        w += self.style.pad     # Compensate for padding between label & end.
        w += (self.style.radius*2)
        h = max(h, (self.style.radius*2))   # Biggest of text height, end diameter
        return (w, h)
    size = property(get_size)

    def get_label_size (self):
        """Return the size (w, h) of this channel's text label"""
        # Calculate size of channel end label inclusive of padding.
        # TODO: This blows up on OS X right now, but should work.
        # gc = wx.GraphicsContext.CreateMeasuringContext()
        style = self.style
        with MeasuringContext() as gc:
            gc.SetFont(gc.CreateFont(wx.Font(pointSize=style.text_size, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), style.text_colour))
            (w, h) = gc.GetTextExtent(self.name)
        w += (style.pad * 2)
        return (w, h)

    def draw_label (self, gc, x, y):
        if self.direction == 'input':
            x += self.style.pad
        elif self.direction == 'output':
            x -= self.get_label_size()[0] - self.style.pad
            #x -= self.style.pad + (self.get_label_size()[0]/2)
        font = gc.CreateFont(wx.Font(pointSize=self.style.text_size, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), self.style.text_colour)
        gc.SetFont(font)
        gc.DrawText(self.name, x, (y - self.get_label_size()[1]/2))
    
    def draw_end (self, gc, x, y):
        style = self.style
        if self.direction == 'output' and style.shadow:
            path = gc.CreatePath()
            path.AddCircle(x + style.shadow_offset, y + style.shadow_offset, style.radius)
            gc.SetPen(wx.Pen(colour=style.shadow_colour, width=0))
            gc.SetBrush(gc.CreateBrush(wx.Brush(style.shadow_colour)))
            gc.DrawPath(path)
        path = gc.CreatePath()
        path.AddCircle(x, y, self.style.radius)
        gc.SetPen(wx.Pen(colour=self.style.border, width=1))
        gc.SetBrush(gc.CreateBrush(wx.Brush(self.style.fill)))
        gc.DrawPath(path)

    def get_size (self):
        return self.get_label_size()
    size = property(get_size)

    def on_paint (self, gc, location):
        (x, y) = location
        self.draw_label(gc, x, y)
        self.draw_end(gc, x, y)
