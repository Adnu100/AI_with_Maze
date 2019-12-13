class Queue: 
    '''faster implementation of queue rather than using list.append(x) and list.pop(0)'''
    class __node: 
        __slots__ = ['n', 'front'] 
        def __init__(self, num): 
            self.n = num 
            self.front = None 

    def __init__(self): 
        self.first = None 
        self.last = None 

    def add(self, num): 
        if self.first: 
            self.last.front = Queue.__node(num) 
            self.last = self.last.front 
        else: 
            self.first = self.last = Queue.__node(num) 

    def deq(self): 
        n = self.first 
        self.first = self.first.front 
        return n.n
    
    def peeklast(self):
        return self.last.n 

    def isempty(self): 
        return self.first == None 

    def isfull(self): 
        return False 

    def __str__(self): 
        s = '[' 
        n = self.first 
        if n: 
            s += str(n.n) 
            n = n.front 
            while n: 
                s += str(', %d' %(n.n)) 
                n = n.front 
        s += ']' 
        return s 

    def __repr__(self):
        return 'Queue(' + s.__str__()[1:-1] + ')'

