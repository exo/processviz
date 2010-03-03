import wx
import math
from canvas import model
from canvas.util import AttrDict

class Channel (model.Channel):
    def __init__ (self, name, datatype, src, dest):
        model.Channel.__init__(self, name, datatype, src, dest)

        # Channel style.
        self.style = AttrDict()
        s = self.style
        s.colour =      (150, 150, 150)
        s.radius =      10
        s.arrow_size =  (4, 4)
        s.cend_r = 4.5  # Source this from the channel end code later.

    def on_paint (self, gc):
        style = self.style
        src, dest = self.src, self.dest
        #diameter = 2*radius
        r = style.radius

        gc.SetPen(wx.Pen(colour=style.colour, width=1))
        path = gc.CreatePath()
        path.MoveToPoint(src.x + style.cend_r, src.y)

        #print "Dest: %s Src: %s" % (dest_y, src_y)
        if dest.x > src.x:
            # Left to right drawing.
            mid_x = src.x + (dest.x - src.x)/2
            if abs(dest.y - src.y) < r:
                path.AddLineToPoint(dest.x - r, dest.y)
            elif dest.y > src.y:
                # Is the target point lower than the source?
                path.AddLineToPoint((mid_x-r), src.y)
                center = (mid_x - r, src.y + r)
                path.AddArc(center, r, math.radians(270), math.radians(0))
                path.AddLineToPoint(mid_x, max(dest.y - r, src.y))
                center = (mid_x + r, dest.y - r)
                path.AddArc(center, r, math.radians(180), math.radians(90), False)
            else:
                path.AddLineToPoint((mid_x-r), src.y)
                center = (mid_x - r, src.y - r)
                path.AddArc(center, r, math.radians(90), math.radians(0), False)
                path.AddLineToPoint(mid_x, min(dest.y + r, src.y))
                center = (mid_x + r, dest.y + r)
                path.AddArc(center, r, math.radians(180), math.radians(270))

            path.AddLineToPoint(dest.x - style['cend_r'], dest.y)

        else:
            # Right to left drawing.
            offset = max((src.x - dest.x)/6, 2*r)
            outer_right_x = src.x + offset
            outer_left_x = dest.x - offset
            lower_y = max(src.y, dest.y) + offset

            path.AddLineToPoint(outer_right_x-r, src.y)
            center = (outer_right_x - r, src.y + r)
            path.AddArc(center, r, math.radians(270), math.radians(0))
            path.AddLineToPoint(outer_right_x, lower_y - r)
            center = (outer_right_x - r, lower_y - r)
            path.AddArc(center, r, math.radians(0), math.radians(90))
            path.AddLineToPoint(outer_left_x + r, lower_y)
            center = (outer_left_x + r, lower_y - r)
            path.AddArc(center, r, math.radians(90), math.radians(180))
            path.AddLineToPoint(outer_left_x, dest.y + r)
            center = (outer_left_x + r, dest.y + r)
            path.AddArc(center, r, math.radians(180), math.radians(270))
            path.AddLineToPoint(dest.x - style['cend_r'], dest.y)

        # Arrow head.
        arrow_size = style['arrow_size']
        path.AddLineToPoint(dest.x - style['cend_r'] - arrow_size[0], dest.y - arrow_size[1])
        path.MoveToPoint(dest.x - style['cend_r'], dest.y)
        path.AddLineToPoint(dest.x - style['cend_r'] - arrow_size[0], dest.y + arrow_size[1])
        gc.StrokePath(path)
