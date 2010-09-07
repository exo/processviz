class ChanEnd (object):
    def __init__ (self, name, direction, datatype, generictype=None):
        self._name, self._direction = name, direction
        self._generictype, self._datatype = generictype, datatype

    def __repr__ (self):
        return "ChanEnd (name='%s', direction='%s', datatype='%s', generictype='%s')" % (self._name, self._direction, self._datatype, self._generictype)

    def get_name (self):
        return self._name
    name = property(get_name)

    def get_direction (self):
        return self._direction
    direction = property(get_direction)

    def get_datatype (self):
        return self._datatype

    def set_datatype (self, datatype):
        self._datatype = datatype
    datatype = property(get_datatype, set_datatype)

    def get_generictype (self):
        return self._generictype
    generictype = property(get_generictype)
