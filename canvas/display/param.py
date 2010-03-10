# param.py
# Display logic for parameters of a process.
# (c) 2010 Jon Simpson <me@jonsimpson.co.uk>

from __future__ import with_statement

import wx
from canvas import model
from canvas.util import AttrDict, MeasuringContext

class Param (model.Param):

    def __init__ (self, name, datatype, value=None):
        model.Param.__init__(self, name, datatype, value)
        self.x, self.y = 0, 0
        self.style = AttrDict()
        s = self.style
        s.font_size = 11    # Font size of parameter labels
        s.text_colour = ( 44,  48,  52)

    def get_size (self):
        with MeasuringContext() as gc:
            gc.SetFont(
                gc.CreateFont(
                    wx.Font(pointSize=self.style.font_size,
                            family=wx.FONTFAMILY_SWISS,
                            style=wx.FONTSTYLE_NORMAL,
                            weight=wx.FONTWEIGHT_NORMAL)
                , self.style.text_colour)
            )
        return gc.GetTextExtent(self.name)

    size = property(get_size)

    def on_paint (self, gc, location):
        self.x, self.y = location
        gc.SetFont(
            gc.CreateFont(
                wx.Font(pointSize=self.style.font_size,
                        family=wx.FONTFAMILY_SWISS,
                        style=wx.FONTSTYLE_NORMAL,
                        weight=wx.FONTWEIGHT_NORMAL)
            , self.style.text_colour)
        )

        text_w, text_h = gc.GetTextExtent(self.name)
        text_x = self.x - text_w / 2
        text_y = self.y + text_h / 2
        gc.DrawText(self.name, text_x, text_y)

