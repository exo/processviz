# builder.py
# Entry point for Processes' network constructor
# (c) 2010 Jon Simpson <me@jonsimpson.co.uk>
import wx
import logging, logging.config
import os.path, sys

class ProcessesApp (wx.App):
    def OnInit(self):
        import constructor.processes as processes
        frame = processes.Frame(
                parent=None,
                title="Processes",
                size=(800, 600),
                pos=(100, 100)
        )
        frame.Show()
        return True
    logging.config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'constructor/logging.conf'))

app = ProcessesApp(redirect=False)
app.MainLoop()
