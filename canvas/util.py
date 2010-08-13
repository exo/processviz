import wx

# This AttrDict implementation doesn't support Pickling.
#class AttrDict(dict):
#    def __init__(self, *args, **kwargs):
#        dict.__init__(self, *args, **kwargs)
#    def __getattribute__(self, attr):
#        return self[attr]
#    def __setattr__(self, attr, val):
#        self[attr] = val

# This one does, but lacks the neat init syntax.
class AttrDict(dict):
    def __init__(self, *args):
        self.__dict__ = self

# This exists because wxPy as shipped on 10.5 lacks the ability to create
# measuring contexts properly. w & h hints.

class MeasuringContext(object):
    def __enter__ (self, w=640, h=480):
        self._dc = dc = wx.MemoryDC()
        dc.SelectObject(wx.EmptyBitmap(w, h, -1))
        try:
            gc = wx.GraphicsContext.Create(dc)
        except NotImplementedError:
            log.error("GraphicsContext not supported here")
        return gc
    
    def __exit__ (self, type, value, traceback):
        self._dc.SelectObject(wx.NullBitmap)

