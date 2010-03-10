from __future__ import with_statement

import wx
from canvas import model
from canvas.util import AttrDict, MeasuringContext

class Process (model.Process):
    def __init__ (self, x, y, name, params=[], input_chans=[], output_chans=[], parent=None, sub_network=None, code=None, requires=None):
        model.Process.__init__(self, name, params, input_chans, output_chans, parent, sub_network, code, requires)
        self._x, self._y = x, y
        self._selected = False

        # Process style, will end up in YAML at some point.
        self.style = AttrDict()
        s = self.style
        s.top             = (202, 214, 234)
        s.bottom          = (172, 192, 216)
        s.bottom_hi       = (255,255,255)
        s.shadow          = True
        s.shadow_colour   = (218, 230, 242)
        s.shadow_offset   = 3
        s.border          = ( 76,  76,  85)
        s.text_colour     = ( 44,  48,  52)
        s.v_pad           = 5                # Vertical padding
        s.h_pad           = 10               # Horizontal padding
        s.lbl_pad         = 2                # Label padding
        s.cend_r          = 4.5              # Radius of channel end.
        s.main_label      = 13               # Font size of main label
        s.params          = 11               # Font size of parameter labels
        s.end_pad         = 5
        s.expander_size   = 6                # Expander widget size.
        s.expander_offset = 7

    def get_selected (self):
        return self._selected

    def set_selected (self, selected):
        self._selected = selected

    selected = property (get_selected, set_selected)

    def get_x (self): return self._x
    def set_x (self, x):
        self._x = x
        if self._sub_network:
            self._sub_network.x = x+20

        # Update channel end positions.
        x = self.x
        y = self.y + self.size[1] - self.style.h_pad
        for c in self.input_chans:
            c.x, c.y = x, y
            y -= (self.max_chan_end_size()[1] + self.style.v_pad)
        x = self.x + self.size[0]
        y = self.y + self.size[1] - self.style.h_pad
        for c in self.output_chans:
            c.x, c.y = x, y
            y -= (self.max_chan_end_size()[1] + self.style.v_pad)

    x = property(get_x, set_x)

    def get_y (self): return self._y
    def set_y (self, y):
        self._y = y
        if self._sub_network:
            self._sub_network.y = y+20
    y = property(get_y, set_y)

    def get_bounds (self):
        (w, h) = self.size
        if self.style.shadow:
            w, h = w + self.style.shadow_offset, h + self.style.shadow_offset
        return (self.x, self.y, self.x + w, self.y + h)
    bounds = property(get_bounds)

    def get_size (self):
        (w, h) = self.get_name_size(self.name)
        style = self.style

        chan_end_w, chan_end_h = self.max_chan_end_size()
        param_w, param_h = self.max_param_size()

        # Content width is max chan label * 2 plus a unit of padding
        content_w = (2 * chan_end_w) + style.h_pad

        # Include parameter label width & padding, if we have params
        if len(self.params) > 0:
            content_w += param_w + (2 * style.h_pad)

        # Width either the name label, or the max of the content width
        w = max(w, content_w)

        # Height sum of label and the height of the max number of ends of either type.
        h += max(len(self.input_chans),len(self.output_chans)) * chan_end_h + style.v_pad

        # Add space for params, if we have them, plus top & bottom padding.
        if len(self.params) > 0:
            h += style.v_pad + (len(self.params) * param_h)

        # Width max of current width, or params plus padding.

        if len(self.params) > 0:
            w = max(w, (param_w + 2*style.h_pad))


        if self._sub_network:
            (net_w, net_h) = self._sub_network.get_size()
            w += net_w
            h += net_h

        return (w, h)
    size = property(get_size)

    def get_name_size (self, name):
        # Calculate size of process name & add outer padding.
        # TODO: This blows up on OS X right now, but should work.
        # gc = wx.GraphicsContext.CreateMeasuringContext()
        with MeasuringContext() as gc:
            gc.SetFont(gc.CreateFont(wx.Font(pointSize=self.style.main_label, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), self.style.text_colour))
            (w, h) = gc.GetTextExtent(name)
        w += (self.style.h_pad * 2)
        h += (self.style.v_pad * 2)
        return (w, h)

    def max_chan_end_size (self):
        if len(self.input_chans) + len(self.output_chans) > 0:
            sizes = [c.size for c in (self.input_chans + self.output_chans)]
            max_w = max([s[0] for s in sizes])
            max_h = max([s[1] for s in sizes])
            return (max_w, max_h)
        else:
            return (0,0)

    def max_param_size (self):
        if len(self.params) > 0:
            sizes = [p.size for p in self.params]
            max_w = max([s[0] for s in sizes])
            max_h = max([s[1] for s in sizes])
            return (max_w, max_h)
        else:
            return (0,0)

    def on_paint (self, gc):
        self.draw_outer(gc)
        (name_w, name_h) = self.draw_name(gc)

        # Parameters
        if self.params and len(self.params) > 0:
            sizes = [p.get_label_size() for p in self.params]
            max_label_w = max([s[0] for s in sizes])
            max_w, max_h = self.max_chan_end_size()
            self.draw_params(gc, name_h + self.style.v_pad, max_label_w, max_w)

        # Input channel ends
        if self.input_chans and len(self.input_chans) > 0:
            x = self.x
            y = self.y + self.size[1] - self.style.h_pad
            for c in self.input_chans:
                c.on_paint(gc, (x,y))
                y -= (self.max_chan_end_size()[1] + self.style.v_pad)

        # Output channel ends
        if self.output_chans and len(self.output_chans) > 0:
            x = self.x + self.size[0]
            y = self.y + self.size[1] - self.style.h_pad
            for c in self.output_chans:
                c.on_paint(gc, (x, y))
                y -= (self.max_chan_end_size()[1] + self.style.v_pad)

        # Sub network
        if self.sub_network:
           self.sub_network.on_paint(gc)

    def draw_outer (self, gc):
        style = self.style
        (w, h) = self.size
        if style.shadow:
            path = gc.CreatePath()
            path.AddRectangle(self.x + style.shadow_offset, self.y + style.shadow_offset, w, h)
            gc.SetPen(wx.Pen(colour=style.shadow_colour, width=0))
            gc.SetBrush(gc.CreateBrush(wx.Brush(style.shadow_colour)))
            gc.DrawPath(path)

        # Outer rect.
        path = gc.CreatePath()
        path.AddRectangle(self.x, self.y, w, h)
        gc.SetPen(wx.Pen(colour=style.border, width=1))
        if self.selected:
            brush = gc.CreateLinearGradientBrush(self.x, self.y, self.x, self.y + h, style.top, style.bottom_hi)
        else:
            brush = gc.CreateLinearGradientBrush(self.x, self.y, self.x, self.y + h, style.top, style.bottom)
        gc.SetBrush(brush)
        gc.DrawPath(path)
        #self._path = path - for hit testing.

    def draw_name (self, gc):
        """Draw the name label for this process"""
        style = self.style
        (w, h) = self.size
        font = gc.CreateFont(wx.Font(pointSize=style.main_label, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), style.text_colour)
        gc.SetFont(font)
        (text_w, text_h) = gc.GetTextExtent(self.name)
        text_x = (self.x + (w/2)) - (text_w / 2)
        text_y = self.y + style.v_pad
        gc.DrawText(self.name, text_x, text_y)
        return (text_w, text_h)

    def draw_params (self, gc, top_offset, max_label_w, max_w):
        (w, h) = self.size
        max_w, max_h = self.max_param_size()

        x = self.x + (w / 2)
        y = self.y + top_offset
        for param in self.params:
            param.on_paint(gc, (x, y), max_label_w,  max_w)
            y += max_h

    def hit_test (self, x, y):
        """Hit test the process and its channel ends for a given hit"""
        # Hit test channel ends.
        result = None
        for c in self.input_chans + self.output_chans:
            result = c.hit_test(x, y)
            if result is not None:
                return result

        # Hit test process.
        min_x, min_y, max_x, max_y = self.bounds
        if max_x > x > min_x and max_y > y > min_y:
            # Hit within process
            if self.sub_network:
                sub_result = self.sub_network.hit_test(x, y)
                if sub_result is not None:
                    return sub_result
            return dict(hit=self, offset=(x - self.x, y - self.y))
        return None

    def on_motion (self, event, transform, offset):
        """Move the process in response to mouse movements"""
        tmp_x = (event.X - transform[0]) - offset[0]
        tmp_y = (event.Y - transform[1]) - offset[1]
        if tmp_x < 0:
            self.x = 0
        else:
            self.x = tmp_x
        if tmp_y < 0:
            self.y = 0
        else:
            self.y = tmp_y

    def structure (self):
        if self._sub_network:
            return dict(_type="Process", name=self.name, sub_network=self._sub_network.structure())
        else:
            return dict(_type="Process", name=self.name, sub_network=None)

