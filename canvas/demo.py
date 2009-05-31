#!/usr/bin/env python

import wx
from display import Process, Network, ChanEnd
from util import AttrDict

class CanvasFrame (wx.Frame):
    def __init__ (self, parent):
        wx.Frame.__init__(self, parent, -1, "Process Canvas", size=(800,600))
        self.panel = CanvasPanel(self)

    def get_network(self): return self.panel._network
    def set_network(self, n):
        print "Set network"
        self.panel._network = n
    network = property(get_network, set_network)

class CanvasPanel (wx.Panel):
    def __init__ (self, frame):
        wx.Panel.__init__(self, frame, -1)
        # Properties
        self._network = None
        self._mouse_down = None
        
        # Events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        
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
        else:
            print "No network"
    
    def on_motion (self, event):
        if self._mouse_down is not None:
            # Get all of the click data.
            hit = self._mouse_down
            p = hit['hit']
            tmp_x = (event.X - hit['transform'][0]) - hit['offset'][0]
            tmp_y = (event.Y - hit['transform'][1]) - hit['offset'][1]
            if tmp_x < 0:
                p.x = 0
            else: 
                p.x = tmp_x
            if tmp_y < 0:
                p.y = 0
            else:
                p.y = tmp_y
            self.Refresh()

    def on_left_down (self, event):
        selection = self._network.hit_test(event.X, event.Y)
        if selection is not None:
            self._mouse_down = selection
    
    def on_left_up (self, event):
        if self._mouse_down:
            self._mouse_down = None
    
    def draw_background(self, gc):
        (w, h) = self.GetSize()
        path = gc.CreatePath()
        path.AddRectangle(0, 0, w, h)
        brush = gc.CreateBrush(wx.Brush(self.style.background))
        gc.SetBrush(brush)
        gc.DrawPath(path)

# Demo main.
# Sample network.
#delta = Process(x=250, y=50, name="delta", input_chans=[ChanEnd('in.0', 'input', 'INT'), ChanEnd('in.1', 'input', 'INT')], output_chans=[ChanEnd('out', 'output', 'INT')])

#integrate = Process(x=100, y=100, name="integrate", input_chans=[ChanEnd('in', 'input', 'BOOL')], output_chans=[ChanEnd('out', 'output', 'BOOL')])
#network = Network(x=100,y=100)
#network.add_process(delta)
#network.add_process(integrate)
#self._network = network
