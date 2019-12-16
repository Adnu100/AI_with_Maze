import sys
import argparse as ap
import heapq
try:
    try:
        from .utilities import run_simulation
        from .utilities.graphnode import node
        from .utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    except ImportError:
        from utilities import run_simulation
        from utilities.graphnode import node
        from utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    SDL = True
except ImportError:
    try:
        from .utilities.graphnode import node
        from .utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    except ImportError:
        from utilities.graphnode import node
        from utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    SDL = False

name = "A* algorithm"

class comparablenode(node):
    '''adding additional functionality (less than and greater than) to readymade node
    so that it can be comparable'''
    def __init__(self, state, parent = None):
        node.__init__(self, state, parent)

    def __lt__(self, another):
        if isinstance(another, node):
            return self.state < another.state
        else:
            raise TypeError("less than operation not supported between {} and {}".format(type(self), type(another)))

    def __gt__(self, another):
        if isinstance(another, node):
            return self.state > another.state
        else:
            raise TypeError("greater than operation not supported between {} and {}".format(type(self), type(another)))

class mylist:
    def __init__(self):
        self.q = []
        self.d = {}

    def put(self, elem):
        heapq.heappush(self.q, elem)
        self.d[elem[1]] = elem[0]

    def get(self):
        popelement = heapq.heappop(self.q)
        self.d.pop(popelement[1])
        return popelement

    def is_better_present_in_list(self, cost, state):
        if state in self.d:
            act_cost = self.d[state]
            if act_cost <= cost:
                return True
        return False
        
def makepath(n):
    path = []
    while n:
        path.append(n.state)
        n = n.parent
    path.reverse()
    return path

def astar(maze):
    startstate = maze.startstate
    goalstate = maze.goalstate
    OPEN = mylist()
    CLOSED = mylist()
    OPEN.put((0, comparablenode(maze.startstate)))
    while OPEN.q:
        g, q = OPEN.get()
        for state in maze.nextstate(q.state):
            if state == goalstate:
                n = comparablenode(state, q)
                return makepath(n), SOLUTION_FOUND
            h = 1
            f = g + h
            if OPEN.is_better_present_in_list(f, state):
                continue
            if CLOSED.is_better_present_in_list(f, state):
                continue
            OPEN.put((f, comparablenode(state, q)))
        CLOSED.put((g, q))
    return makepath(q), SOLUTION_NOT_FOUND #A-star finds the solution if present, so this line is unreachable

RUN = astar

if __name__ == '__main__':
    a = ap.ArgumentParser(prog = 'astar.py', description = 'A* algorithm implemented to solve a maze problem', epilog = 'Note: -c option is used with -s option')
    a.add_argument(dest = 'mazefile', help = 'the maze file containing maze to solve')
    a.add_argument('-s', '--simulate', dest = 'simulate', help = 'provide if you want the graphical simulation of the path found by algorithm in maze to be shown', action = 'store_true')
    a.add_argument('-c', '--continuous', dest = 'cont', help = 'if supplied, the simulation is continuous (mouse click not needed for each turn)', action = 'store_true')
    args = a.parse_args()
    m = get_maze(args.mazefile)
    if not m:
        print('error: invalid maze file provided', file = sys.stderr)
        sys.exit()
    if args.simulate:
        if SDL:
            run_simulation.run_simulation(name, main(RUN, m, to_print = False), m, continuous = args.cont)
        else:
            print("error: can't make simulation, PySDL2 not installed")
            print("printing path instead...")
            main(RUN, m, to_print = True)
    else:
        main(RUN, m, to_print = True)

