
import wx
import wx.lib.ogl as ogl
import logging, logging.config

class ConstructorApp (wx.App):
    def OnInit(self):
        import constructor.poped as poped
        ogl.OGLInitialize()
        frame = poped.Frame(
                parent=None,
                title="Constructor",
                size=(800, 600),
                pos=(100, 100)
        )
        frame.Show()
        return True
    # FIXME: Not platform independent.
    logging.config.fileConfig('constructor/logging.conf')

c = ConstructorApp(redirect=False)
c.MainLoop()