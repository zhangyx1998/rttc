class Transparent:
    """
    Hijacks _GenericAlias.__call__() so we can do stuff before and after the call
    """
    def __init__(self, cls: type):
        self.__proxy__ = cls
    
    def __call__(self, *args, **kwargs):
        return self.__proxy__(*args, **kwargs)
    
    def __getattr__(self, key):
        if key in ("__class__", "__proxy__"):
            return super().__getattr__(key)
        else:
            return getattr(self.__proxy__, key)
    
    def __setattr__(self, key, value):
        if key in ("__class__", "__proxy__"):
            super().__setattr__(key, value)
        else:
            setattr(self.__proxy__, key, value)

    def __repr__(self):
        return repr(self.__proxy__)

    def __str__(self):
        return str(self.__proxy__)
    
    def __setitem__(self, key, value):
        self.__proxy__[key] = value
    
    def __getitem__(self, key):
        return self.__class__(self.__proxy__[key])

    def __type__(self):
        return type(self.__proxy__)
