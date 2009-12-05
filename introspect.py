import wx
from canvas.common import CanvasFrame
from canvas.display import ChanEnd, Network, Process

from logparser.parser import LogParserThread, EVT_LINE_AVAILABLE
from pprint import pprint

INS, AJW, START, END, CALL, OUTPUT, INPUT = 'INS AJW START END CALL OUTPUT INPUT'.split(' ')

class MyApp(wx.App):
    
    def OnInit (self):
        frame = CanvasFrame(parent=None)
        self.Bind(EVT_LINE_AVAILABLE, self.on_line)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        #self.setup_network()
        self._processes = {}
        self._shadowed_procs = {}
        self._line_no = 0

        # Log Parser.
        thread = LogParserThread(self, 'test_data/commstime.log')
        thread.start()

        # Setup top level process, don't know WS address yet (use 0)
        #l = self.lp.next()
        proc = Process(x=0, y=0, name="TLP")
        self._processes[0] = proc
        network = Network(x=0, y=0)
        network.add_process(proc)
        self._root_network = network
        self._first_proc = True

        # Add network to frame & show.
        frame.panel.network = network
        frame.Show(True)
        self._frame = frame
        return True

    def on_key_down (self, e):
        k = e.GetKeyCode()
        if k == wx.WXK_LEFT:
            print "Left key"
        e.Skip()

    def on_line(self, e):
        # First line of file determines address of main process.
        if self._first_proc:
            self._processes[e.line[1]] = self._processes[0]
            del self._processes[0]
            self._first_proc = False
        if e.line:
            l = e.line
            self._line_no += 1
            if l[0] == INS:
                # Instruction, store line number?
                address = l[1]
                if address in self._processes:
                    self._processes[address].src_pos = l[3]
                pass
            elif l[0] == INPUT:
                # Channel input.
                pass
            elif l[0] == OUTPUT:
                # Channel output.
                pass
            elif l[0] == START:
                parent_ws = l[1]

                # Get the parent proc.
                if parent_ws in self._shadowed_procs:
                    parent_proc = self._shadowed_procs[parent_ws]
                else:
                    parent_proc = self._processes[parent_ws]

                # Ensure a sub network exists.
                if parent_proc.sub_network is None:
                    parent_proc.sub_network = Network(x=parent_proc.x, y=parent_proc.y)

                # Start a new proc, shadow & preserve the outer proc
                if parent_proc.par_increment() == 1:
                    if parent_ws in self._shadowed_procs:
                        pprint(self._root_network.structure())
                        raise Exception("Shadowing a shadowed proc")
                    self._shadowed_procs[parent_ws] = parent_proc
                    parent_proc.ws = parent_ws
                    proc = Process(x=0, y=0, name="", parent=parent_proc)
                    parent_proc.par_increment() # Include shadowed process.
                    print "Start proc at %s, parent shadowed" % (parent_ws)
                    self._processes[parent_ws] = proc
                    parent_proc.sub_network.add_process(proc)
                    print "Added process %s to %s" % (parent_ws, parent_proc.name)

                # Add the newly started process.
                proc_ws = l[2]
                proc = Process(x=0, y=0, name="", parent=parent_proc)
                print "Start proc at %s, parent %s" % (proc_ws, parent_ws)
                self._processes[proc_ws] = proc
                parent_proc.sub_network.add_process(proc)
            elif l[0] == END:
                ws = l[1]
                print "End for %s" % l[1]
                proc = self._processes[ws]
                parent = proc.parent
                if parent.par_decrement() == 0:
                    # Unshadow
                    self._processes[parent.ws] = self._shadowed_procs[parent.ws]
                    del self._shadowed_procs[parent.ws]

                # Remove proc from display network.
                parent.sub_network.remove_process(proc)
                # Remove proc from ws tracking list.
                del self._processes[ws]

            elif l[0] == AJW:
                old_ws, new_ws = l[1], l[2]
                print "AJW: %s, %s" % (old_ws, new_ws)
                # Ordinary workspace adjustment.
                self._processes[new_ws] = self._processes[old_ws]
                del self._processes[old_ws]
            elif l[0] == CALL:
                ws, proc_name = l[1], l[2]
                print "Setting name of %s to %s" % (ws, proc_name)
                self._processes[ws].name = proc_name
            else:
                raise Exception("Unknown event type: %s" % l[0])
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