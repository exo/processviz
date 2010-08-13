# codegen.py
# Generates occam-pi code from a process network object model.
# (c) 2010 Jon Simpson <me@jonsimpson.co.uk>

class OccamGenerator (object):

    def __init__ (self, network):
        self._network = network
        self._outfile = None
        self._buffer = ""

    def _wl (self, line):
        if self._outfile is not None:
            self._outfile.write(line + '\n')
        else:
            self.buffer += line + '\n'

    def _gen (self):
        self._gen_modules()
        self._gen_processes()
        self._gen_tlp()

    def _gen_modules (self):
        modules = []
        for process in self._network.processes:
            if process.requires is not None:
                for module in process.requires:
                    if module not in modules:
                        modules.append(module)
        self._wl('-- Modules')
        if len(modules) > 0:
            for module in modules:
                self._wl('#INCLUDE "' + module + '.module"')
        self._wl('')

    def _gen_processes (self):
        self._wl("-- Processes")
        for process in self._network.processes:
            if process.code is not None:
                self._wl(process.code)
        self._wl('')

    def _gen_tlp (self, tlp_name='main'):
        network = self._network
        self._wl('PROC ' + tlp_name + ' ()')
        for channel in network.channels:
            self._wl('  CHAN ' + channel.datatype.upper() + ' ' + channel.name + ':')

        if len(network.processes) > 0:
            self._wl('  PAR')
            for process in network.processes:
                # Parameters
                parameter_list = ""
                for param in process.params:
                    if param.value:
                        parameter_list += param.value + ", "
                    else:
                        log.debug("Invalid code being generated - None still in param list")

                # Channels
                channel_connects = ""
                for input_chan in process.input_chans:
                    for channel in network.channels:
                        if channel.dest == input_chan:
                            channel_connects += channel.name + '?, '
                for output_chan in process.output_chans:
                    for channel in network.channels:
                        if channel.src == output_chan:
                            channel_connects += channel.name + '!, '
                channel_connects = channel_connects.rstrip(', ')

                # If there are no channel connections, strip the parameter list.
                if channel_connects == "":
                    parameter_list = parameter_list.rstrip(', ')

                self._wl('    %s (%s%s)' % (process.name, parameter_list, channel_connects))
        else:
            self._wl('  SKIP')

        self._wl(':')

    def to_file (self, filename):
        self._outfile = open(filename, 'wb')
        self._gen()
        self._outfile.close()

