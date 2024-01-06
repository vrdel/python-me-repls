from a import A

class B(A):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.cvalue = None

    @property
    def cvalue(self):
        print('\nGetting child value')
        return self._cvalue

    @cvalue.setter
    def cvalue(self, value):
        print('\nSetting child value ' + value)
        self._cvalue = value


