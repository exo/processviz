import wx
from canvas import model

from canvas.util import AttrDict

class Network (model.Network):
    def __init__ (self, x=0, y=0):
        model.Network.__init__(self)
        self._x, self._y = x, y

        self.style = AttrDict ()
        self.style.min_w = 50
        self.style.min_h = 50
        self.style.background = (238,238,238)
        self.style.border = (221, 221, 221)
        

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
    bounds = property(get_bounds)
    
    def get_size (self):
        (x1, y1, x2, y2) = self.bounds
        return x2 - x1, y2 - y1
    size = property(get_size)
    
    def on_paint (self, gc):
        gc.PushState()
        gc.Translate(self.x, self.y)
        self.draw_background(gc)
        for p in self.processes:
            p.on_paint(gc)
        for c in self.channels:
            c.on_paint(gc)
        gc.PopState()

    def draw_background(self, gc):
        (w, h) = self.size
        path = gc.CreatePath()
        path.AddRectangle(0, 0, w, h)
        gc.SetPen(wx.Pen(colour=self.style.border, width=1))
        gc.SetBrush(gc.CreateBrush(wx.Brush(self.style.background)))
        gc.DrawPath(path)
    
    def hit_test (self, x, y):
        min_x, min_y, max_x, max_y = self.bounds
        # Compensate for transform.
        x, y = x - self.x, y - self.y
        if max_x > x > min_x and max_y > y > min_y:
            # Hit within process network
            for p in self.processes:
                hit_result = p.hit_test(x, y)
                if hit_result is not None:
                    # Sum transforms, in case of sub network.
                    (tx, ty) = hit_result.get('transform', (0,0))
                    hit_result['transform'] = (self.x+tx, self.y+ty)
                    return hit_result
        return None
