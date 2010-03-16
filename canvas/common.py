import wx
from display import *
from util import AttrDict

# Pickle
try:
    import cPickle as pickle
except ImportError:
    import pickle

# Logging
import logging
log = logging.getLogger("Processes");

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
        self._selected = None
        self._chan_start_point = None
        self._filename = None
        self._chan_count = 0

        # Events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)

        # Allow drop.
        self.SetDropTarget(CanvasDropTarget(self))

        self.style = AttrDict()
        self.style.background = (255, 255, 255)

    def get_network(self): return self._network
    def set_network(self, n): self._network = n
    network = property(get_network, set_network)

    def get_filename (self):
        return self._filename

    def set_filename (self, filename):
        self._filename = filename
    filename = property(get_filename, set_filename)

    def on_paint (self, event):
        # PaintDC's aren't double buffered on Windows.
        if 'wxMSW' in wx.PlatformInfo:
            dc = wx.BufferedPaintDC(self)
        else:
            dc = wx.PaintDC(self)
        dc = wx.PaintDC(self)

        try:
            gc = wx.GraphicsContext.Create(dc)
        except NotImplementedError:
            log.debug("GraphicsContext not supported on this platform")
            return
        # Drawing
        self.draw_background(gc)
        if self._network:
            self._network.on_paint(gc)
        else:
            print "No network"

    def on_motion (self, event):
        if self._selected is not None:
            # Get all of the click data.
            hit = self._selected
            p = hit['hit']
            p.on_motion(event, hit['transform'], hit['offset'])
            self.Refresh()

    def on_left_down (self, event):
        selection = self._network.hit_test(event.X, event.Y)
        if selection is not None:
            self._selected = selection

        # Reset channel creation mode if we expected to find a channel end.
        if self._chan_start_point is not None:
            if self._selected is None or not isinstance(self._selected['hit'], ChanEnd):
                log.debug("Reset channel creation mode")
                self._chan_start_point.selected = False
                self._chan_start_point = None
                self.Refresh()

    def on_left_up (self, event):
        if self._selected:
            if isinstance(self._selected['hit'], ChanEnd):
                log.debug("Selected a channel end")
                if self._chan_start_point is not None:
                    types_match = self._chan_start_point.datatype == self._selected['hit'].datatype
                    different_directions = self._chan_start_point.direction != self._selected['hit'].direction
                    if types_match and different_directions:
                        # Types match, work out which way round the channel is.
                        log.debug("Creating a channel.")
                        if self._chan_start_point.direction == 'output':
                            src = self._chan_start_point
                            dest = self._selected['hit']
                        else:
                            src = self._selected['hit']
                            dest = self._chan_start_point
                        self._network.add_channel(Channel('c' + str(self._chan_count), src.datatype, src, dest))
                        self._chan_count += 1
                        self._chan_start_point.selected = False
                        self._chan_start_point = None
                        self.Refresh()
                    else:
                        # Types don't match, abort.
                        log.debug("Channel types don't match, or directions do. Cancelling selection")
                        self._chan_start_point.selected = False
                        self._chan_start_point = None
                        self.Refresh()
                else:
                    # No ends currently selected, start a chan creation op.
                    log.debug("In channel creation mode")
                    chanend = self._selected['hit']
                    self._chan_start_point = chanend
                    chanend.selected = True
                    self.Refresh()
            # Cancel out the current selection.
            self._selected = None

    def on_right_down(self, event):
        right_selected = self._network.hit_test(event.X, event.Y)
        if right_selected and isinstance(right_selected['hit'], Process):
            # Store, in case the menu is invoked.
            self._right_selected = right_selected

            # Only bind the first time.
            if not hasattr(self, 'context_properties'):
                self.context_properties = wx.NewId()
                self.Bind(wx.EVT_MENU, self.on_context_properties, id=self.context_properties)

            # Make the popup menu
            menu = wx.Menu()
            menu.Append(self.context_properties, "Properties")
            self.PopupMenu(menu)
            menu.Destroy()

            # Can reset here, as by the time the menu is destroyed, the menu event has happened.
            self._right_selected = None

    def on_context_properties(self, event):
        selected = self._right_selected['hit']
        print "Properties for %s requested" % selected
        pd = PropertiesDialog(selected)
        pd.ShowModal()
        pd.Destroy()
        self.Refresh()
        self._right_selected = None

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
        if self.GetData():
            data = self.drop_data.GetDataHere()
            data = pickle.loads(data)

            inputs = []
            if data['input']:
                for end in data['input']:
                    inputs.append(ChanEnd(end['name'], 'input', end['type']))

            outputs = []
            if data['output']:
                for end in data['output']:
                    outputs.append(ChanEnd(end['name'], 'output', end['type']))

            params = []
            if data['params']:
                for param in data['params']:
                    params.append(Param(param['name'], param['type'], value=None, desc=param['desc']))

            canvas = self.canvas
            p = Process (x, y, data['name'], params=params, input_chans=inputs, output_chans=outputs, code=data['code'], requires=data['requires'], desc=data['desc'])
            canvas.network.add_process(p)
            canvas.Refresh()
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

class ParameterValidator (wx.PyValidator):
    def __init__ (self, process, key):
        wx.PyValidator.__init__(self)
        self.process = process
        self.key = key

    def Clone (self):
        """ All validators must implement Clone """
        return ParameterValidator(self.process, self.key)

    def Validate (self, win):
        # validation goes here
        return True

    def TransferToWindow (self):
        textCtrl = self.GetWindow()
        for param in self.process.params:
            if param.name is self.key:
                textCtrl.SetValue(str(param.value))
        return True

    def TransferFromWindow (self):
        textCtrl = self.GetWindow()
        for param in self.process.params:
            if param.name is self.key:
                param.value = textCtrl.GetValue()
        return True

class PropertiesDialog (wx.Dialog):
    def __init__ (self, process):
        wx.Dialog.__init__(self, None, -1, "Process: %s" % process.name)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, -1, process.desc))
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
        fgs = wx.FlexGridSizer(3, 2, 5, 5)
        # Create the edit fields.
        for param in process.params:
            fgs.Add(wx.StaticText(self, -1, "%s (%s)" % (param.name, param.datatype)), 0, wx.ALIGN_RIGHT)
            field = wx.TextCtrl(self, validator=ParameterValidator(process, param.name))
            field.SetValue(str(param.value))
            fgs.Add(field, 0, wx.EXPAND)
        fgs.AddGrowableCol(1)
        sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)
        btns = wx.StdDialogButtonSizer()
        okay = wx.Button(self, wx.ID_OK)
        okay.SetDefault()
        btns.AddButton(okay)
        btns.AddButton(wx.Button(self, wx.ID_CANCEL))
        btns.Realize()
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
