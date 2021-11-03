class A(object):
    def __new__(cls, *args, **kwargs):
        if getattr(cls, 'instanced', None):
            return cls.instanced
        else:
            setattr(cls, 'instanced', object.__new__(cls))
            return cls.instanced

    def __init__(self, *args, **kwargs):
        self._value = None

    @property
    def value(self):
        print('\nGetting parent value')
        return self._value

    @value.setter
    def value(self, value):
        print('\nSetting parent value ' + value)
        self._value = value
