import sys
from maze import main, get_maze, SOLUTION_FOUND, SOLUTION_NOT_FOUND

def simple_hill_climbing(maze):
    currentstate = maze.startstate
    goalstate = maze.goalstate
    path = [currentstate]
    while currentstate != goalstate:
        found = False
        for state in maze.nextstate(currentstate):
            if maze.is_better(state, currentstate):
                path.append(state)
                currentstate = state
                found = True
                break
        if found:
            continue
        return path, SOLUTION_NOT_FOUND
    return path, SOLUTION_FOUND

RUN = simple_hill_climbing

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit()
    m = get_maze(sys.argv[1])
    if not m:
        sys.exit()
    main(simple_hill_climbing, m)

