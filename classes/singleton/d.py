from c import C

class D(C):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.value = None

