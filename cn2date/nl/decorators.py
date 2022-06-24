class SelectorMethod:
    tag: str = None

    def __init__(self, tag: str):
        self.tag = tag

    def __call__(self, fnc):
        fnc.__setattr__("__tag__", self.tag)
        return fnc
