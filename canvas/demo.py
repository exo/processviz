#!/usr/bin/env python

import wx
from display import Process, Network
from util import AttrDict

class CanvasFrame (wx.Frame):
    def __init__ (self, parent):
        wx.Frame.__init__(self, parent, -1, "Process Canvas", size=(800,600))
        self.panel = CanvasPanel(self)

class CanvasPanel (wx.Panel):
    def __init__ (self, frame):
        wx.Panel.__init__(self, frame, -1)
        # Properties
        self._network = None
        
        # Events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        #self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        #self.Bind(wx.EVT_MOTION, self.on_motion)
        
        # Sample network.
        delta = Process(x=250, y=50, name="delta", params=None)
        
        network = Network(x=100,y=100)
        network.add_process(delta)
        self._network = network
        
        self.style = AttrDict(
            background = (175, 175, 175)
        )
    
    def on_paint (self, event):
        dc = wx.PaintDC(self)
        try:
            gc = wx.GraphicsContext.Create(dc)
        except NotImplementedError:
            print "GraphicsContext not supported here"
            return
        # Drawing
        self.draw_background(gc)
        if self._network:
            self._network.on_paint(gc)
    
    def on_left_down (self, event):
        print "%s" % self._network.hit_test(event.X, event.Y)
    
    def draw_background(self, gc):
        (w, h) = self.GetSize()
        path = gc.CreatePath()
        path.AddRectangle(0, 0, w, h)
        brush = gc.CreateBrush(wx.Brush(self.style.background))
        gc.SetBrush(brush)
        gc.DrawPath(path)
            
class MyApp(wx.App):
    def OnInit (self):
        frame = CanvasFrame(parent=None)
        frame.Show(True)
        return True

app = MyApp(redirect=False)
app.MainLoop()