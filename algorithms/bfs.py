import sys
import argparse as ap
try:
    try:
        from .utilities import run_simulation
        from .utilities import myqueue as queue
        from .utilities.graphnode import node
        from .utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    except ImportError:
        from utilities import run_simulation
        from utilities import myqueue as queue
        from utilities.graphnode import node
        from utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    SDL = True
except ImportError:
    try:
        from .utilities import myqueue as queue
        from .utilities.graphnode import node
        from .utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    except ImportError:
        from utilities import myqueue as queue
        from utilities.graphnode import node
        from utilities.maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND
    SDL = False

name = "Breadth First Search"

def bfs(maze):
    path = []
    startstate = maze.startstate
    goalstate = maze.goalstate
    found = False
    q = queue.Queue()
    q.add(node(startstate))
    visited = set()
    while not found:
        current = q.deq()
        visited.add(current.state)
        for state in maze.nextstate(current.state):
            if state in visited:
                continue
            q.add(node(state, current))
            visited.add(state)
            if state == goalstate:
                found = True
                break
    n = q.peeklast()
    path = []
    while n:
        path.append(n.state)
        n = n.parent
    path.reverse()
    if found:
        return path, SOLUTION_FOUND
    return path, SOLUTION_NOT_FOUND

RUN = bfs

if __name__ == '__main__':
    a = ap.ArgumentParser(
        prog = 'bfs.py', 
        description = 'breadth first search algorithm implemented to solve a maze \
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
