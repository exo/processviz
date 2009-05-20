import wx

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
    def __getattribute__(self, attr):
        return self[attr]
    def __setattr__(self, attr, val):
        self[attr] = val

# This exists because wxPy as shipped on 10.5 lacks the ability to create
# measuring contexts properly. w & h hints.

class MeasuringContext(object):
    def __enter__ (self, w=640, h=480):
        self._dc = dc = wx.MemoryDC()
        dc.SelectObject(wx.EmptyBitmap(w, h, -1))
        try:
            gc = wx.GraphicsContext.Create(dc)
        except NotImplementedError:
            print "GraphicsContext not supported here"
        return gc
    
    def __exit__ (self, type, value, traceback):
        self._dc.SelectObject(wx.NullBitmap)

