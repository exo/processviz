class Network (object):
    def __init__ (self):
        self._processes = []
        self._channels = []

    def get_processes (self):
        return self._processes

    processes = property(get_processes)

    def add_process (self, process):
        self._processes.append(process)

    def remove_process (self, process):
        chan_ends = process.get_input_chans() + process.get_output_chans()
        # Make a copy of self._channels, as we are modifying it in the for loop
        for chan in self._channels[:]:
            if chan.src in chan_ends or chan.dest in chan_ends:
                self.remove_channel(chan)
        self._processes.remove(process)

    def get_channels (self):
        return self._channels

    channels = property(get_channels)

    def add_channel (self, channel):
        self._channels.append(channel)

    def remove_channel (self, channel):
        self._channels.remove(channel)

    def structure (self):
        return dict(_type='Network', channels=self._channels, processes=[n.structure() for n in self._processes])

    def propogate_from_end (self, source_end):
        for process in self.processes:
            if source_end in (process.input_chans + process.output_chans):
                generic_ends = process.get_generic_chan_ends(source_end.generictype)
                for g in generic_ends:
                    print "Flipping datatype to %s from %s" % (g.datatype,source_end.datatype)
                    g.datatype = source_end.datatype
                    for c in self.channels:
                        n = None
                        if c.src is g:
                            n = c.dest
                        elif c.dest is g:
                            n = c.src
                        # If this end is set correctly, propogate from the other end.
                        if n is not None and n.datatype is not None:
                            self.propogate_from_end(n)
