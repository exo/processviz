class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
    def __getattribute__(self, attr):
        return self[attr]
    def __setattr__(self, attr, val):
        self[attr] = val