import simple
import maze
import run_simulation as run
import sys

if len(sys.argv) < 3:
    sys.exit()
m = maze.get_maze(sys.argv[1])
c = int(sys.argv[2])
c = False if c == 0 else True
p = maze.main(simple.RUN, m, to_print = False)
run.run_simulation(simple.name, p, m.startstate, m.l, continuous = c)
