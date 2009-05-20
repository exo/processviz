class Network (object):
    def __init__ (self):
        self._processes = []
        self._channels = []

    def get_processes (self):
        return self._processes
   
    processes = property(get_processes)

    def add_process (self, process):
        self._processes.append(process)

    def get_channels (self):
        return self._channels

    channels = property(get_channels)

    def add_channel (self, channel):
        self._channels.append(channel)
