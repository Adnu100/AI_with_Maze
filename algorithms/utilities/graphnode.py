class node:
    __slots__ = ['state', 'parent']

    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent

    def addnode(self, child):
        child.parent = self

    def addparent(self, parent):
        self.parent = parent

    def __eq__(self, another):
        if(isinstance(another, node)):
            return self.state == another.state
        elif(isinstance(another, tuple)):
            return self.state == another
        return False

    def __hash__(self):
        return hash(self.state)

