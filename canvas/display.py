#!/usr/bin/env python
import wx

from DisplayObjects import *

class SimpleFrame (wx.Frame):
    def __init__ (self, parent):
        wx.Frame.__init__(self, parent, -1, "Process Drawing Experiment", size=(800,600))
        self.panel = SimplePanel(self)

class SimplePanel (wx.Panel):
    def __init__ (self, frame):
        wx.Panel.__init__(self, frame, -1)

        # Event bindings
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)

        self._selected = None
        self._processes = []
        self._channels = []

        self._process_network = get_demo_network()

    def get_demo_network (self):
        # Sub network.
        chan_ends = [
            ChannelEndDisplay(0,0,'in', 'in', 'INT'),
            ChannelEndDisplay(0,0,'out', 'out', 'INT')
        ]

        a = ProcessDisplay(x=0, y=0, name="a", chan_ends=chan_ends, params=None)

        chan_ends = [
            ChannelEndDisplay(0,0,'in', 'in', 'INT'),
            ChannelEndDisplay(0,0,'out', 'out', 'INT')
        ]

        b = ProcessDisplay(x=100, y=0, name="b", chan_ends=chan_ends, params=None)

        chan_ends = [
            ChannelEndDisplay(0,0,'in', 'in', 'INT'),
            ChannelEndDisplay(0,0,'out', 'out', 'INT')
        ]

        c = ProcessDisplay(x=50, y=50, name="c", chan_ends=chan_ends, params=None)

        c_a = ChannelDisplay("c", "P.GRIPPER", c.chan_end('out'), a.chan_end('in'))
        a_b = ChannelDisplay("c", "P.GRIPPER", a.chan_end('out'), b.chan_end('in'))
        b_c = ChannelDisplay("c", "P.GRIPPER", b.chan_end('out'), c.chan_end('in'))

        sub_network = ProcessNetworkDisplay()
        sub_network.add_process(c)

        sub_network.add_process(a)
        sub_network.add_process(b)
        sub_network.add_channel(c_a)
        sub_network.add_channel(a_b)
        sub_network.add_channel(b_c)

        chan_ends = [
            ChannelEndDisplay(0,0,'in', 'in.1', 'INT'),
            ChannelEndDisplay(0,0,'in', 'in.1', 'INT'),
            ChannelEndDisplay(0,0,'in', 'in.1', 'INT'),
            ChannelEndDisplay(0,0,'in', 'in.2', 'P.GRIPPER'),
            ChannelEndDisplay(0,0,'out', 'out.1', 'BYTE'),
            ChannelEndDisplay(0,0,'out', 'out.2', 'P.BAH')
        ]

        delta = ProcessDisplay(x=250, y=50, name="delta", chan_ends=chan_ends, params=None)

        chan_ends = [
            ChannelEndDisplay(0,0,'in', 'robot.control', 'P.CTRL'),
            ChannelEndDisplay(0,0,'out', 'motors', 'P.MOTORS'),
            ChannelEndDisplay(0,0,'out', 'gripper', 'P.GRIPPER')
        ]

        robot_control = ProcessDisplay(x=10, y=150, name="robot.control", chan_ends=chan_ends, params=None, sub_network=sub_network)

        #c = DisplayChannel(robot_control, "gripper", delta, "in.2")

        c = ChannelDisplay("c", "P.GRIPPER", robot_control.chan_end('gripper'), delta.chan_end('in.2'))

        process_network = ProcessNetworkDisplay(x=100,y=100)
        process_network.add_process(delta)
        process_network.add_process(robot_control)
        process_network.add_channel(c)
        return process_network

    def on_paint (self,event):
        dc = wx.PaintDC(self)
        try:
            gc = wx.GraphicsContext.Create(dc)
        except NotImplementedError:
            print "GraphicsContext not supported here"
            return

        # Drawing
        self.draw_background(gc)
        self._process_network.on_paint(gc)

    def draw_background(self, gc):
        bg_colour = (255, 255, 255)
        (w, h) = self.GetSize()
        path = gc.CreatePath()
        path.AddRectangle(0, 0, w, h)
        brush = gc.CreateBrush(wx.Brush(bg_colour))
        gc.SetBrush(brush)
        gc.DrawPath(path)

    def on_left_down (self, event):
        self._selected = None
        result = self._process_network.hit_test(event.X, event.Y)
        if result is not None:
            #self._selected.on_left_down(event)
            self._selected = result
            self._clicked = (event.X, event.Y)
            result.toggle()

    def on_left_up (self, event):
        if self._selected:
            self._selected.toggle()
            self.Refresh()
            self._selected = None

    def on_motion (self, event):
        if self._selected is None:
            return
        process = self._selected
        clicked = (event.X, event.Y)
        process.x += clicked[0] - self._clicked[0]
        process.y += clicked[1] - self._clicked[1]
        self._process_network.update_size()
        self._clicked = clicked
        self.Refresh()

class MyApp(wx.App):
    def OnInit (self):
        frame = SimpleFrame(parent=None)
        frame.Show(True)
        return True

app = MyApp(redirect=False)
app.MainLoop()