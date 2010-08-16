class ChanEnd (object):
    def __init__ (self, name, direction, datatype, generictype=None):
        self._name, self._direction = name, direction
        self._generictype, self._datatype = generictype, datatype

    def get_name (self):
        return self._name
    name = property(get_name)

    def get_direction (self):
        return self._direction
    direction = property(get_direction)

    def get_datatype (self):
        return self._datatype
    datatype = property(get_datatype)

    def get_generictype (self):
        return self._generictype
    generictype = property(get_generictype)
