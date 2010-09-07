# param.py
# Data model for a parameter of a process
# (c) 2010 Jon Simpson <me@jonsimpson.co.uk>

class Param (object):
    def __init__ (self, name, datatype, value=None, desc=""):
        self._name, self._datatype = name, datatype
        self._value, self._desc = value, desc

    def __repr__ (self):
        return "Param (name='%s', datatype='%s', value='%s', desc='%s')" % (self._name, self._datatype, self._value, self._desc)

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

    def get_desc (self):
        return self._desc

    desc = property (get_desc)

