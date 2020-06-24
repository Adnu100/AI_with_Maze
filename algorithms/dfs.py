import sys
import argparse as ap
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

name = "Depth First Search"

class node:
    __slots__ = ['state', 'parent']

    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent

    def addnode(self, child):
        child.parent = self

def dfs(maze):
    startstate = maze.startstate
    goalstate = maze.goalstate
    l = []
    push = l.append
    pop = l.pop
    push(node(startstate))
    found = False
    visited = set()
    while not found:
        if not l:
            return [], SOLUTION_NOT_FOUND
        current = pop()
        for state in maze.nextstate(current.state):
            if state in visited:
                continue
            visited.add(state)
            push(node(state, current))
            if state == goalstate:
                found = True
                break
    n = pop()
    path = []
    while n:
        path.append(n.state)
        n = n.parent
    path.reverse()
    return path, SOLUTION_FOUND

RUN = dfs

if __name__ == '__main__':
    a = ap.ArgumentParser(
        prog = 'dfs.py', 
        description = 'depth first search algorithm implemented to solve a maze \
                problem', 
        epilog = 'Note: -c option is used with -s option'
    )
    a.add_argument(
        dest = 'mazefile', 
        help = 'the maze file containing maze to solve'
    )
    a.add_argument(
        '-s', 
        '--simulate', 
        dest = 'simulate', 
        help = 'provide if you want the graphical simulation of the path found by \
                algorithm in maze to be shown', 
        action = 'store_true')
    a.add_argument(
        '-c', 
        '--continuous', 
        dest = 'cont', 
        help = 'if supplied, the simulation is continuous (mouse click not \
                needed for each turn)', 
        action = 'store_true'
    )
    args = a.parse_args()
    m = get_maze(args.mazefile)
    if not m:
        print('error: invalid maze file provided', file = sys.stderr)
        sys.exit()
    if args.simulate:
        if SDL:
            run_simulation.run_simulation(
                name, 
                main(
                    RUN,
                    m, 
                    to_print = False
                ), 
                m, 
                continuous = args.cont
            )
        else:
            print("error: can't make simulation, PySDL2 not installed")
            print("printing path instead...")
            main(RUN, m, to_print = True)
    else:
        main(RUN, m, to_print = True)
