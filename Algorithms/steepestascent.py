import sys
import argparse as ap
import run_simulation
from maze import get_maze, main, SOLUTION_FOUND, SOLUTION_NOT_FOUND

name = "steepest ascent hill climbing"

def steepest_ascent_hill_climbing(maze):
    currentstate = maze.startstate
    goalstate = maze.goalstate
    path = [currentstate]
    SUCC = currentstate
    while currentstate != goalstate:
        prevstate = currentstate
        for state in maze.nextstate(currentstate):
            if state == goalstate:
                path.append(state)
                return path, SOLUTION_FOUND
            elif maze.is_better(state, SUCC):
                SUCC = state
            if maze.is_better(SUCC, currentstate):
                currentstate = SUCC
        if currentstate == prevstate:
            return path, SOLUTION_NOT_FOUND
        path.append(currentstate)
    return path, SOLUTION_FOUND

RUN = steepest_ascent_hill_climbing

if __name__ == '__main__':
    a = ap.ArgumentParser(prog = 'steepestascent.py', description = 'simple hill climbing algorithm implemented to solve a maze problem', epilog = 'Note: -c option is used with -s option')
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

