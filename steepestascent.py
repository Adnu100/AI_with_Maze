import sys
from maze import get_maze, main, SOLUTION_FOUND, SOLUTION_NOT_FOUND

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
    if len(sys.argv) != 2:
        sys.exit()
    m = get_maze(sys.argv[1])
    if not m:
        sys.exit()
    main(steepest_ascent_hill_climbing, m)
