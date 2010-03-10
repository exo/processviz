# param.py
# Data model for a parameter of a process
# (c) 2010 Jon Simpson <me@jonsimpson.co.uk>

class Param (object):
    def __init__ (self, name, datatype, value=None):
        self._name, self._datatype, self._value = name, datatype, value

    def get_name (self):
        return self._name
    name = property(get_name)

    def get_datatype (self):
        return self._datatype

    datatype = property(get_datatype) 

    def get_value (self):
        return self._value

    def set_value (self, value):
        self._value = value

    value = property (get_value, set_value)

