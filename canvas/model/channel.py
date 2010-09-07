class Channel (object):
    def __init__ (self, name, datatype, src, dest):
        self._name, self._datatype = name, datatype
        self._src, self._dest = src, dest

    def __repr__ (self):
        return "Channel (name='%s', datatype='%s', src='%s', dest='%s')" % (self._name, self._datatype, self._src, self._dest)

    def get_src (self):
        return self._src

    src = property (get_src)

    def get_dest (self):
        return self._dest

    dest = property (get_dest)

    def get_datatype (self):
        return self._datatype

    datatype = property(get_datatype)

    def get_name (self):
        return self._name

    name = property(get_name)

    def get_ends (self):
        return [self.src, self.dest]

    ends = property(get_ends)
