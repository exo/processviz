class Process (object):
    def __init__ (self, name, params=[], input_chans=[], output_chans=[], parent=None, sub_network=None, code=None, requires=None, desc=""):
        self._name = name
        self._params = params
        self._input_chans = input_chans
        self._output_chans = output_chans
        self._sub_network = sub_network
        self._parent = parent
        self._par_count = 0
        self._code = code
        self._requires = requires
        self._desc = desc

    def get_name (self):
        return self._name

    def set_name (self, name):
        self._name = name

    name = property(get_name, set_name)

    def get_params (self):
        return self._params

    params = property(get_params)

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

    def get_code (self):
        return self._code

    code = property(get_code)

    def get_requires (self):
        return self._requires

    requires = property(get_requires)

    def get_desc (self):
        return self._desc

    desc = property(get_desc)

    def par_increment (self):
        self._par_count += 1
        return self._par_count

    def par_decrement (self):
        self._par_count -= 1
        return self._par_count

    def get_parent (self):
        return self._parent

    parent = property(get_parent)
