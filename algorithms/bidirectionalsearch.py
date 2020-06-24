import sys
import argparse as ap
SDL = True
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

name = "bidirectional search"

def makepath(commonstate, l1, l2):
    s1, s2 = None, None
    for i in l1:
        if i.state == commonstate:
            s1 = i
            break
    for i in l2:
        if i.state == commonstate:
            s2 = i
            break
    s2 = s2.parent
    front = []
    while s1:
        front.append(s1.state)
        s1 = s1.parent
    front.reverse()
    back = []
    while s2:
        back.append(s2.state)
        s2 = s2.parent
    front.extend(back)
    return front

statefun = lambda i: i.state

def bidirectional_both_bfs(maze):
    startstate = maze.startstate
    goalstate = maze.goalstate
    dir1states = {startstate, }
    l1 = [node(startstate)]
    dir2states = {goalstate, }
    l2 = [node(goalstate)]
    visited1, visited2 = set(), set()
    while True:
        l1 = [
            node(state, prevstate) 
            for prevstate in l1 
            for state in maze.nextstate(prevstate.state) 
            if state not in visited1
        ]
        visited1.update(map(statefun, l1))
        if not l1:
            break
        dir1states.clear()
        dir1states.update(l1)
        common = dir1states.intersection(dir2states)
        if common:
            return makepath(common.pop(), l1, l2), SOLUTION_FOUND
        l2 = [
            node(state, prevstate) 
            for prevstate in l2 
            for state in maze.nextstate(prevstate.state) 
            if state not in visited2
        ]
        visited2.update(map(statefun, l2))
        dir2states.clear()
        dir2states.update(l2)
        common = dir1states.intersection(dir2states)
        if common:
            return makepath(common.pop(), l1, l2), SOLUTION_FOUND
    current = l1.pop()
    path = []
    while current:
        path.append(current.state)
        current = current.parent
    path.reverse()
    return path, SOLUTION_NOT_FOUND

RUN = bidirectional_both_bfs

if __name__ == '__main__':
    a = ap.ArgumentParser(
        prog = 'bidirectionalsearch.py', 
        description = 'bidirectional search algorithm implemented to solve a maze \
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
