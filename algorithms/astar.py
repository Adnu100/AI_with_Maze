import sys
import argparse as ap
import heapq
try:
    try:
        from .utilities import run_simulation
        from .utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    except ImportError:
        from utilities import run_simulation
        from utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    SDL = True
except ImportError:
    try:
        from .utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    except ImportError:
        from utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    SDL = False

name = "A*"

class mylist:
    def __init__(self):
        self.q = []

    def put(self, elem):
        heapq.heappush(self.q, elem)

    def get(self):
        return heapq.heappop(self.q)

    def is_better_present_in_list(self, cost, state):
        for act_cost, act_state in self.q:
            if act_state == state:
                if act_cost <= cost:
                    return True
                else:
                    return False
class node:
    def __init__(self, state, prev = None):
        self.state = state
        self.prev = prev

    def __eq__(self, another):
        if(isinstance(another, node)):
            return self.state == another.state
        elif(isinstance(another, tuple)):
            return self.state == another
        return False

class path_t:
    def __init__(self, startstate):
        self.l = [node(startstate)]

    def add(self, state, parent):
        for i in self.l:
            if i == parent:
                parent = i
                break
        self.l.append(node(state, parent))

    def makepath(self):
        n = self.l[-1]
        path = []
        while(n):
            path.append(n.state)
            n = n.prev
        path.reverse()
        return path

def listcheck(l, f, q):
    return l.is_better_present_in_list(f, q)

def astar(maze):
    path = path_t(maze.startstate)
    OPEN = mylist()
    CLOSED = mylist()
    OPEN.put((0, maze.startstate))
    goalstate = maze.goalstate
    while OPEN.q:
        g, q = OPEN.get()
        for state in maze.nextstate(q):
            if state == goalstate:
                path.add(state, q)
                return path.makepath(), SOLUTION_FOUND
            h = 1
            f = g + h
            if listcheck(OPEN, f, state):
                continue
            if listcheck(CLOSED, f, state):
                continue
            path.add(state, q)
            OPEN.put((f, state))
        CLOSED.put((g, q))
    return path.makepath(), SOLUTION_NOT_FOUND #A-star finds the solution if present, so

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

