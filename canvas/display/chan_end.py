from __future__ import with_statement
from util import AttrDict, MeasuringContext

import wx
import model

class ChanEnd (model.ChanEnd):
    
    def __init__ (self, name, direction, datatype):
        model.ChanEnd.__init__(self, name, direction, datatype)
        self.style = AttrDict (
            fill            = (218, 230, 242),
            hilight         = (171,  75,  75),
            border          = ( 76,  76,  85),
            shadow_colour   = (218, 230, 242),
            shadow_offset   = 3,
            radius          = 4.5,                             
            text_size       = 11,
            text_colour     = ( 44,  48,  52),
            pad             = 10,
            offset          = 1, # Relation of channel end to text?
        )

    def get_label_size (self):
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
