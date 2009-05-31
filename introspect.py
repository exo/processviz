import wx
from canvas.demo import CanvasFrame
from canvas.display import ChanEnd, Network, Process

from logparser.parser import LogParser

INS, AJW, START, CALL, OUTPUT, INPUT = 'INS AJW START CALL OUTPUT INPUT'.split(' ')

class MyApp(wx.App):
    
    def OnInit (self):
        frame = CanvasFrame(parent=None)
        frame.Bind(wx.EVT_IDLE, self.on_idle)
        #self.setup_network()
        self._processes = {}
        self._shadowed_procs = {}

        # Log Parser.
        self.lp = LogParser('commstime.log')

        # Setup top level process
        l = self.lp.next()
        proc = Process(x=0, y=0, name="TLP")
        print "Initial is %s" % id(proc)
        self._processes[l[1]] = proc
        network = Network(x=0, y=0)
        network.add_process(proc)

        # Add network to frame & show.
        frame.network = network
        frame.Show(True)
        self._frame = frame
        return True

    def on_idle(self, e):
        l = self.lp.next()
        if l:
            if l[0] == START:
                parent_proc_ws = l[1]
                if parent_proc_ws in self._shadowed_procs:
                    parent_proc = self._shadowed_procs[parent_proc_ws]
                else:
                    parent_proc = self._processes[parent_proc_ws]
                par_count = parent_proc.par_increment()
                print "parent proc ws: %s par count: %s" % (parent_proc_ws, par_count)

                # We'll need to add a sub network, make sure it exists.
                if parent_proc.sub_network is None:
                    parent_proc.sub_network = Network(x=parent_proc.x, y=parent_proc.y)

                # Shadow & preserve the outer proc, use a new process.
                if par_count == 0:
                    if parent_proc_ws in self._shadowed_procs:
                        raise Exception("Shadowing a shadowed proc - Reimplement me!")
                    self._shadowed_procs[parent_proc_ws] = parent_proc
                    proc = Process(x=0, y=0, name="")
                    self._processes[parent_proc_ws] = proc
                    parent_proc.sub_network.add_process(proc)

                # Add the newly started process.
                proc_ws = l[2]
                proc = Process(x=0, y=0, name="")
                self._processes[proc_ws] = proc
                parent_proc.sub_network.add_process(proc)

            elif l[0] == AJW:
                old_ws, new_ws = l[1], l[2]
                print "AJW: %s, %s" % (old_ws, new_ws)
                self._processes[new_ws] = self._processes[old_ws]
                del self._processes[old_ws]
            elif l[0] == CALL:
                ws, proc_name = l[1], l[2]
                print "Setting name of %s to %s" % (ws, proc_name)
                self._processes[ws].name = proc_name
            self._frame.Refresh()

    def setup_network (self):
        delta = Process(x=250, y=50, name="delta", input_chans=[ChanEnd('in.0', 'input', 'INT'), ChanEnd('in.1', 'input', 'INT')], output_chans=[ChanEnd('out', 'output', 'INT')])

        integrate = Process(x=100, y=100, name="integrate", input_chans=[ChanEnd('in', 'input', 'BOOL')], output_chans=[ChanEnd('out', 'output', 'BOOL')])
        network = Network(x=100,y=100)
        network.add_process(delta)
        network.add_process(integrate)
        self._frame.network = network

app = MyApp(redirect=False)
app.MainLoop()