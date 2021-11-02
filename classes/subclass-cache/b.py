from a import A

class B(A):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        value = getattr(self, 'value', None)
        if value:
            self.value = value
        else:
            self.value = 'classB_value'

