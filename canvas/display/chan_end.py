from __future__ import with_statement
from util import AttrDict

import wx
import model

class ChanEnd (model.ChanEnd):
    
    def __init__ (self, name, direction, datatype):
        model.ChanEnd.__init(self, name, direction, datatype)
        self.style = AttrDict (
            fill            = (218, 230, 242),
            hilight         = (171,  75,  75),
            border          = ( 76,  76,  85),
            shadow_colour   = (218, 230, 242),
            shadow_offset   = 3,
            radius          = 4.5,                             
            text_size       = 11,
            text_color      = ( 44,  48,  52),
            w_pad           = (10),
            offset          = 1, # Relation of channel end to text?
        )

    def get_label_size (self):
        # Calculate size of channel end label inclusive of padding.
        # TODO: This blows up on OS X right now, but should work.
        # gc = wx.GraphicsContext.CreateMeasuringContext()
        style = self.style.end_style
        with MeasuringContext() as gc:
            gc.SetFont(gc.CreateFont(wx.Font(pointSize=style.text_size, family=wx.FONTFAMILY_SWISS, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL), self.style.text))
            (w, h) = gc.GetTextExtent(self.name)
        w += (self.style.h_pad * 2)
        h += (self.style.v_pad * 2)
        return (w, h)