import wx
from display import Process, Network, ChanEnd
from util import AttrDict

# Pickle
try:
    import cPickle as pickle
except ImportError:
    import pickle

# Logging
import logging
log = logging.getLogger("popedLogger");

class CanvasFrame (wx.Frame):
    def __init__ (self, parent):
        wx.Frame.__init__(self, parent, -1, "Process Canvas", size=(800,600))
        self._panel = CanvasPanel(self)

    def get_panel(self): return self._panel
    panel = property(get_panel)

class CanvasPanel (wx.Panel):
    def __init__ (self, frame):
        wx.Panel.__init__(self, frame, -1)
        # Properties
        self._network = Network(x=0, y=0) # Root network.

        self._mouse_down = None

        # Events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)

        # Allow drop.
        self.SetDropTarget(CanvasDropTarget(self))

        self.style = AttrDict(
            background = (175, 175, 175)
        )

    def get_network(self): return self._network
    def set_network(self, n): self._network = n
    network = property(get_network, set_network)

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

class CanvasDropTarget(wx.PyDropTarget):
    def __init__(self, canvas):
        wx.PyDropTarget.__init__(self)
        self.drop_data = BlockDropData()
        self.SetDataObject(self.drop_data)
        self.canvas = canvas

    def OnDrop (self, x, y): pass
    def OnEnter(self, x, y, d): return d
    def OnLeave(self): pass
    def OnDrop(self, x, y): pass
    def OnDragOver(self, x, y, d): return d
    def OnData (self, x, y, d):
        #print "OnData", x, y, d
        if self.GetData():
            data = self.drop_data.GetDataHere()
            data = pickle.loads(data)
            print "The pickled data is %s" % data
            print "Name should be %s" % data['name']

            input_ends = []
            output_ends = []
            for c in data['input']:
                print "Chanend is %s" % c
                input_ends.append(ChanEnd(c['name'], 'input', c['type']))
            for c in data['output']:
                output_ends.append(ChanEnd(c['name'], 'output', c['type']))
            #print type(data)
            canvas = self.canvas
            p = Process (0, 0, data['name'], input_chans=input_ends, output_chans=output_ends)
            log.debug("Adding process: %s, %s, %s", data['name'], data['input'], data['output'])
            canvas.network.add_process(p)
            canvas.Refresh()
            #self.diagram.GetCanvas().Refresh()
        log.debug("Completed OnData for Canvas droptarget.")
        return d

class BlockDropData(wx.PyDataObjectSimple):
    def __init__(self):
        wx.PyDataObjectSimple.__init__(self, wx.CustomDataFormat('BlockData'))

    def GetDataSize(self):
        return len(self.data)

    def GetDataHere(self):
        return self.data

    def SetData(self, data):
        self.data = data
        return True
