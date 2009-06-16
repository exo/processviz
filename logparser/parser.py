import wx
import threading
import time
import wx.lib.newevent

INS, AJW, START, END, CALL, OUTPUT, INPUT = 'INS AJW START END CALL OUTPUT INPUT'.split(' ')

# This creates a new Event class and a EVT binder function
(DataAvailableEvent, EVT_LINE_AVAILABLE) = wx.lib.newevent.NewEvent()

class LogParserThread (threading.Thread):
    def __init__ (self, window, path):
        threading.Thread.__init__(self)
        self.lp = LogParser(path)
        self.window = window

    def run(self):
        line = self.lp.next()
        while line:
            evt = DataAvailableEvent(line = line)
            wx.PostEvent(self.window, evt)
            line = self.lp.next()
            time.sleep(1)
        self.lp.close()

class LogParser (object):
    def __init__ (self, path):
        self.fp = open(path, 'r')
            
    def next (self):
        line = self.fp.readline()
        if line:
            return self.parse(line)
        else:
            return None

    def parse (self, line):
        d = line.strip().split(' ')
        address, cmd = int(d[0], 16), d[1]
        if cmd == '@':
            # Instruction executed.
            filename, line_no = d[2].split(':')
            return [INS, address, filename, int(line_no)]
        elif cmd == '=>':
            # Rename process
            new_address = int(d[2], 16)
            return [AJW, address, new_address]
        elif cmd == 'start':
            # Start process
            new_address = int(d[2], 16)
            return [START, address, new_address]
        elif cmd == 'end':
            # End process
            return [END, address]
        elif cmd == 'call':
            # Call
            return [CALL, address, d[2]]
        elif cmd == 'output':
            channel = int(d[2], 16)
            return [OUTPUT, address, channel]
        elif cmd == 'input':
            channel = int(d[2], 16)
            return [INPUT, address, channel]
        else:
            raise Exception("Unknown op type '%s'" % cmd)

    def close (self):
        self.fp.close()
