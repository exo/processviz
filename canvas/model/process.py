class Process (object):
    def __init__ (self, name, params, input_chans, output_chans, sub_network):
        self._name = name
        self._input_chans = input_chans
        self._output_chans = output_chans
        self._sub_network = sub_network
        
    def get_name (self):
        return self._name

    def set_name (self, name):
        self._name = name

    name = property(get_name, set_name)

    def get_input_chans (self):
        return self._input_chans

    input_chans = property(get_input_chans)

    def get_output_chans (self):
        return self._output_chans
        
    output_chans = property(get_output_chans)
    
    def get_sub_network (self):
        return self._sub_network

    def set_sub_network (self, network):
        self._sub_network = network

    sub_network = property(get_sub_network, set_sub_network)
