import simple, simulatedannealing, steepestascent
import maze
import run_simulation as run
import sys

if len(sys.argv) < 4:
    sys.exit()
m = maze.get_maze(sys.argv[1])
module = (simple, simulatedannealing, steepestascent)[int(sys.argv[2])]
c = int(sys.argv[3])
c = False if c == 0 else True
p = maze.main(module.RUN, m, to_print = False)
run.run_simulation(module.name, p, m, continuous = c)
