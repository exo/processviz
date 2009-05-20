import wx
import model

from util import AttrDict

class Network (model.Network):
    def __init__ (self, x=0, y=0):
        model.Network.__init__(self)
        self._x, self._y = x, y
        
        self.style = AttrDict (
            min_w = 50,
            min_h = 50,
            background = (255,255,255),
            border = (172, 192, 216),
        )

    def get_x (self): return self._x
    def set_x (self, x): self._x = x
    x = property(get_x, set_x)

    def get_y (self): return self._y
    def set_y (self, y): self._y = y
    y = property(get_y, set_y)
    
    def get_bounds (self):
        bounds = [p.get_bounds() for p in self.processes]
        min_x = min([b[0] for b in bounds] + [0])
        min_y = min([b[1] for b in bounds] + [0])
        max_x = max([b[2] for b in bounds] + [self.style.min_w])
        max_y = max([b[3] for b in bounds] + [self.style.min_h])
        return (min_x, min_y, max_x, max_y)
    
    def get_size (self):
        (x1, y1, x2, y2) = self.get_bounds()
        return x2 - x1, y2 - y1
    
    def on_paint (self, gc):
        (w, h) = self.get_size()
        path = gc.CreatePath()
        path.AddRectangle(0, 0, w, h)
        gc.SetPen(wx.Pen(colour=self.style.border, width=1))
        gc.SetBrush(gc.CreateBrush(wx.Brush(self.style.background)))
        gc.DrawPath(path)
        print "w:%s h:%s" % (w,h)