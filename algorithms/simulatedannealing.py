import sys, random
import argparse as ap
from math import e
try:
    from .utilities import run_simulation
    from .utilities.maze import get_maze, main, SOLUTION_FOUND, SOLUTION_NOT_FOUND
except ImportError:
    from utilities import run_simulation
    from utilities.maze import get_maze, main, SOLUTION_FOUND, SOLUTION_NOT_FOUND

name = "simulated annealing"

delta_E = lambda E1, E2: E1 - E2

def probability(dE, T):
    k = 1e-2
    exp = - (dE / (k * T))
    return e ** exp

def simulated_annealing(maze):
    currentstate = maze.startstate
    goalstate = maze.goalstate
    path = [currentstate]
    BEST_SO_FAR = currentstate
    testpath = []
    T = 200
    prev = None
    while currentstate != goalstate:
        found = False
        E1 = maze.value(currentstate)
        P = True
        for state in maze.nextstate(currentstate):
            if P:
                P = False
            if state == prev:
                continue
            E2 = maze.value(state)
            if state == goalstate:
                path.append(state)
                return path, SOLUTION_FOUND
            if maze.is_better(state, currentstate):
                path.extend(testpath)
                path.append(state)
                testpath = []
                prev = currentstate
                BEST_SO_FAR = currentstate = state
                found = True
                break
            else:
                p = probability(delta_E(E2, E1), T)
                if p < random.random():
                    found = True
                    testpath.append(state)
                    prev = currentstate
                    currentstate = state
                    break
        if not found:
            return path, SOLUTION_NOT_FOUND
        T = 0.9 * T
    return path, SOLUTION_FOUND

RUN = simulated_annealing

if __name__ == '__main__':
    a = ap.ArgumentParser(prog = 'simulatedannealing.py', description = 'simple hill climbing algorithm implemented to solve a maze problem', epilog = 'Note: -c option is used with -s option')
    a.add_argument(dest = 'mazefile', help = 'the maze file containing maze to solve')
    a.add_argument('-s', '--simulate', dest = 'simulate', help = 'provide if you want the graphical simulation of the path found by algorithm in maze to be shown', action = 'store_true')
    a.add_argument('-c', '--continuous', dest = 'cont', help = 'if supplied, the simulation is continuous (mouse click not needed for each turn)', action = 'store_true')
    args = a.parse_args()
    m = get_maze(args.mazefile)
    if not m:
        print('error: invalid maze file provided', file = sys.stderr)
        sys.exit()
    if args.simulate:
        run_simulation.run_simulation(name, main(RUN, m, to_print = False), m, continuous = args.cont)
    else:
        main(RUN, m, to_print = True)

