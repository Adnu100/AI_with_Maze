import sys
import argparse as ap
import algorithms
from algorithms.utilities.maze import get_maze, main
from algorithms.utilities import run_simulation

def get_parsed_arguments():
    a = ap.ArgumentParser(
            prog = 'run.py', 
            description = 'driver program implemented to solve a maze problem with any algorithm', 
            epilog = 'Note: -c option is used with -s option'
    )
    a.add_argument(
            '-l', 
            '--list',
            dest = 'show_list',
            help = 'shows the list of total algorithms which can be used for solving a particular maze', 
            action = 'store_true'
    )
    args, rem_args = a.parse_known_args()
    if args.show_list:
        return args
    a.add_argument(
            dest = 'mazefile', 
            help = 'the maze file containing maze to solve'
    )
    a.add_argument(
            '-s', 
            '--simulate', 
            dest = 'simulate', 
            help = 'provide if you want the graphical simulation of the path found by algorithm in maze to be shown', 
            action = 'store_true'
    )
    a.add_argument(
            '-c', 
            '--continuous', 
            dest = 'cont', 
            help = 'if supplied, the simulation is continuous (mouse click not needed for each turn)', 
            action = 'store_true'
    )
    a.add_argument(
            '-a', 
            '--algorithm', 
            dest = 'al', 
            type = int, 
            help = 'decide which method to use for solving the maze (for example, 1 for simple hill climbing) for a list of total methods use -l or --list option', 
            default = 1, 
            choices = list(range(1, algorithms.totals + 1))
    )
    a.parse_args(rem_args, namespace = args)
    return args

def run():
    args = get_parsed_arguments()
    if args.show_list:
        print("total algorithms:")
        for no, alg in enumerate(algorithms.all_list, 1):
            print("\t%d\t%s" %(no, alg.name))
    else:
        m = get_maze(args.mazefile)
        if not m:
            print('error: invalid maze file provided', file = sys.stderr)
            sys.exit()
        print("using %s algorithm on maze..." %algorithms.all_list[args.al - 1].name)
        if args.simulate:
            run_simulation.run_simulation(algorithms.all_list[args.al - 1].name, main(algorithms.all_list[args.al - 1].RUN, m, to_print = False), m, continuous = args.cont)
        else:
            print()
            main(algorithms.all_list[args.al - 1].RUN, m, to_print = True)

if __name__ == '__main__':
    run()


