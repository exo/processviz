# param.py
# Display logic for parameters of a process.
# (c) 2010 Jon Simpson <me@jonsimpson.co.uk>

from __future__ import with_statement

import wx
from canvas import model
from canvas.util import AttrDict, MeasuringContext

class Param (model.Param):

    def __init__ (self, name, datatype, value=None, desc=""):
        model.Param.__init__(self, name, datatype, value, desc)
        self.x, self.y = 0, 0
        self.style = AttrDict()
        s = self.style
        s.font_size = 11    # Font size of parameter labels
        s.text_colour = ( 44,  48,  52)

    def get_label_text (self):
        return self.name + ':'

    def get_label_size (self):
        return self.get_text_size(self.get_label_text())

    def get_value_text (self):
        if self.value:
            return ' ' + self.value
        else:
            return ' None'

    def get_value_size(self):
        return self.get_text_size(self.get_value_text())

    def get_text (self):
        return self.get_label_text() + self.get_value_text()

    def get_text_size (self, text):
        with MeasuringContext() as gc:
            gc.SetFont(
                gc.CreateFont(
                    wx.Font(pointSize=self.style.font_size,
                            family=wx.FONTFAMILY_SWISS,
                            style=wx.FONTSTYLE_NORMAL,
                            weight=wx.FONTWEIGHT_NORMAL)
                , self.style.text_colour)
            )
        return gc.GetTextExtent(text)

    def get_size (self):
        return self.get_text_size(self.get_text())

    size = property(get_size)

    def on_paint (self, gc, location, max_label_width, max_width):
        self.x, self.y = location
        gc.SetFont(
            gc.CreateFont(
                wx.Font(pointSize=self.style.font_size,
                        family=wx.FONTFAMILY_SWISS,
                        style=wx.FONTSTYLE_NORMAL,
                        weight=wx.FONTWEIGHT_NORMAL)
            , self.style.text_colour)
        )

        text_w, text_h = self.size
        label_w, label_h = self.get_label_size()

        text_x = self.x - (max_width/2) + (max_label_width - label_w)
        text_y = self.y + text_h / 2
        gc.DrawText(self.get_label_text(), text_x, text_y)
        text_x = self.x - (max_width/2) + max_label_width
        gc.DrawText(self.get_value_text(), text_x, text_y)
