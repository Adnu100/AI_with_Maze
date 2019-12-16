SOLUTION_FOUND = 0x1
SOLUTION_NOT_FOUND = 0x2

class maze_t:
    '''maze data structure which holds the information of maze'''
    def __init__(self, data):
        '''initialises maze'''
        self.r = len(data)
        self.c = len(data[0])
        self.data = data
        self.startstate = (0, self.data[0].index(1))
        self.goalstate = (self.r - 1, self.data[self.r - 1].index(1))

    def __str__(self):
        '''gives the numeric representation of maze'''
        s = ""
        for i in self.data:
            s += str(i)
            s += "\n"
        return s 

    def nextstate(self, currentstate):
        '''gives the next states of maze'''
        if currentstate != self.startstate and self.data[currentstate[0] - 1][currentstate[1]] == 1:
            yield (currentstate[0] - 1, currentstate[1])
        if self.data[currentstate[0]][currentstate[1] + 1] == 1:
            yield (currentstate[0], currentstate[1] + 1)
        if currentstate != self.goalstate and self.data[currentstate[0] + 1][currentstate[1]] == 1:
            yield (currentstate[0] + 1, currentstate[1])
        if self.data[currentstate[0]][currentstate[1] - 1] == 1:
            yield (currentstate[0], currentstate[1] - 1)
    
    def value(self, state):
        '''heuristic function
        returns the value h(n) of a state'''
        return abs(self.goalstate[0] - state[0]) + abs(self.goalstate[1] - state[1])

    def is_better(self, s1, s2, toprint = False):
        '''function which tells if state s1 if better than state s2'''
        val1 = self.value(s1)
        val2 = self.value(s2)
        if val1 == val2:
            return s1[0] > s2[0]
        if toprint:
            print("{} : {} < {} : {}".format(s1, val1, s2, val2))
        return bool(val1 < val2)

def get_maze(filename):
    '''returns a maze from a filename'''
    try:
        f = open(filename, "r+")
        l = f.readlines()
        l = [i[:-1] for i in l]
        if len(set([len(i) for i in l])) != 1:
            raise Exception
        for i in l:
            s = set(i)
            if '*' in s:
                s.remove('*')
            if 'x' in s:
                s.remove('x')
            if 'X' in s:
                s.remove('X')
            if ' ' in s:
                s.remove(' ')
            if chr(9608) in s:
                s.remove(chr(9608))
            if len(s):
                raise Exception
        rows = len(l)
        columns = len(l[0])
        data = [[1 if i == ' ' else 0 for i in j] for j in l]
        if data[0].count(1) == 1 and data[len(data) - 1].count(1) == 1:
            return maze_t(data)
        else:
            raise Exception
    except:
        return None
    finally:
        try:
            f.close()
        except:
            pass

def direction(prev, cur):
    '''returns the direction of a state respective to its previous state'''
    if cur[0] > prev[0]:
        return "down"
    elif cur[0] < prev[0]:
        return "up"
    elif cur[1] > prev[1]:
        return "right"
    elif cur[1] < prev[1]:
        return "left"
    else:
        return "start"

def main(fun, maze, to_print = True):
    '''a function which returns a path in {up, down, left, right} format
    parameters
    fun :       the function which applied a specific algorithm to the maze 
                and returns the coordinates list indicating the path
                the function also needs to return another value whether solution is found or not
                along with the path
    maze :      the maze_t instance (the maze to be solved)
    to_print :  whether to print the result or not'''
    path, result = fun(maze)
    resolvedpath = []
    a = resolvedpath.append
    if result == SOLUTION_FOUND:
        if to_print:
            print("path to other end found")
        prev = path[0]
        for item in path:
            a(direction(prev, item))
            prev = item
        a("end")
    elif result == SOLUTION_NOT_FOUND:
        if to_print:
            print("path to other end not found")
            print("could reach upto:")
        prev = path[0]
        for item in path:
            a(direction(prev, item))
            prev = item
        a("end")
    if to_print:
        print(", ".join(resolvedpath))
    return resolvedpath

