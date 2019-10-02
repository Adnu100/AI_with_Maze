import sys, random
from math import e
from maze import get_maze, main, SOLUTION_FOUND, SOLUTION_NOT_FOUND

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
    if len(sys.argv) != 2:
        sys.exit()
    m = get_maze(sys.argv[1])
    if not m:
        sys.exit()
    main(simulated_annealing, m)
