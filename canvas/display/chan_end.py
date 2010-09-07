from __future__ import with_statement
from canvas.util import AttrDict, MeasuringContext

import wx
from canvas import model

class ChanEnd (model.ChanEnd):
    
    def __init__ (self, name, direction, datatype, generictype=None):
        model.ChanEnd.__init__(self, name, direction, datatype, generictype)
        self.style = AttrDict()
        s = self.style
        s.fill            = (218, 230, 242)
        s.hilight         = (171,  75,  75)
        s.border          = ( 76,  76,  85)
        s.shadow          = True
        s.shadow_colour   = (218, 230, 242)
        s.shadow_offset   = 3
        s.radius          = 4.5
        s.text_size       = 11
        s.text_colour     = ( 44,  48,  52)
        s.pad             = 10
        s.offset          = 1 # Relation of channel end to text?

        self.x, self.y = 0, 0
        self._selected = False

    def get_selected (self):
        return self._selected

    def set_selected (self, selected):
        self._selected = selected

    selected = property (get_selected, set_selected)

    def get_bounds (self):
        """Return the bounding box (x0, y0, x1, y1), given the current position"""
        (w, h) = self.size
        x, y = self.x, self.y
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
    bounds = property (get_bounds)

    def hit_test (self, x, y):
        min_x, min_y, max_x, max_y = self.bounds
        if max_x > x > min_x and max_y > y > min_y:
            # Hit within channel end.
            return dict(hit=self, offset=(x - self.x, y - self.y))
        else:
            return None

    def draw_bounds (self, gc):
        """Debug function to draw a box showing the channel end's outline"""
        (x0, y0, x1, y1)= self.bounds
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
            (w, h) = gc.GetTextExtent(self.label)
        w += (style.pad * 2)
        return (w, h)

    def draw_label (self, gc):
        x, y = self.x, self.y
        if self.direction == 'input':
            x += self.style.pad
        elif self.direction == 'output':
            x -= self.get_label_size()[0] - self.style.pad
            #x -= self.style.pad + (self.get_label_size()[0]/2)
        font = gc.CreateFont(wx.Font(pointSize=self.style.text_size, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), self.style.text_colour)
        gc.SetFont(font)
        gc.DrawText(self.label, x, (y - self.get_label_size()[1]/2))
    
    def draw_end (self, gc):
        style, x, y = self.style, self.x, self.y
        if self.direction == 'output' and style.shadow:
            path = gc.CreatePath()
            path.AddCircle(x + style.shadow_offset, y + style.shadow_offset, style.radius)
            gc.SetPen(wx.Pen(colour=style.shadow_colour, width=0))
            gc.SetBrush(gc.CreateBrush(wx.Brush(style.shadow_colour)))
            gc.DrawPath(path)
        path = gc.CreatePath()
        path.AddCircle(x, y, self.style.radius)
        gc.SetPen(wx.Pen(colour=self.style.border, width=1))
        if self.selected:
            gc.SetBrush(gc.CreateBrush(wx.Brush(self.style.hilight)))
        else:
            gc.SetBrush(gc.CreateBrush(wx.Brush(self.style.fill)))
        gc.DrawPath(path)

    def get_size (self):
        return self.get_label_size()
    size = property(get_size)

    def on_paint (self, gc, location):
        self.x, self.y = location
        self.draw_label(gc)
        self.draw_end(gc)

    def on_motion (self, event, transform, offset):
        return

    def get_label (self):
        return "%s (%s)" % (self.name, self.datatype)

    label = property(get_label)
