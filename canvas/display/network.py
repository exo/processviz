import model

class Network (model.Network):
    def __init__ (self, x=0, y=0):
        model.Network.__init__(self)
        (self._x, self._y) = (x, y)
    
    def get_x (self): return self._x
    def set_x (self, x): self._x = x
    x = property(get_x, set_x)

    def get_y (self): return self._y
    def set_y (self, y): self._y = y
    y = property(get_y, set_y)

    