class node:
    '''implementation of a node in graph
    each node represents a state and has a parent
    this node is hashable and can be compared with other node'''
    __slots__ = ['state', 'parent']

    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent

    def addnode(self, child):
        '''make this node as a parent of another node (child)'''
        child.parent = self

    def addparent(self, parent):
        '''change the parent node of the current node'''
        self.parent = parent

    def __eq__(self, another):
        if isinstance(another, node):
            return self.state == another.state
        if isinstance(another, tuple):
            return self.state == another
        return False

    def __hash__(self):
        return hash(self.state)
