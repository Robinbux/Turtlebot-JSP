import argparse


class Flags:
    find_parameters_automatically = False
    replace_old_parameters = False
    verbose = False
    show_matrix = False
    plot_graph = False

    def parse_arguments(args):
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', "--automatical", dest='a',
                            help="Automatically increase 'Eta', 'Alpha' and 'Beta', until no constraint is violated anymore.",
                            action='store_true')
        parser.add_argument('-r', "--replace", dest='r',
                            help="Replace old values in the yaml file, with the automatically chosen ones.",
                            action='store_true')
        parser.add_argument('-v', "--verbose", dest='v', help="More verbose output.", action='store_true')
        parser.add_argument('-m', "--matrix", dest='m', help="Show an interactive confusion matrix of the final Q.",
                            action='store_true')
        parser.add_argument('-s', "--simulated", dest='s', help="Use the simulated annealer", action='store_true')
        parser.add_argument('-q', "--quantum", dest='q', help="Use the D-Wave quantum computer", action='store_true')
        parser.add_argument('-i', "--inspect", dest='i', help="Use the D-Wave inspector", action='store_true')
        parser.add_argument('-p', "--plot", dest='p', help="Plot the graph", action='store_true')

        options, unknown = parser.parse_known_args(args=args) if args is not None else parser.parse_known_args()

        Flags.find_parameters_automatically = options.a
        Flags.replace_old_parameters = options.r
        Flags.verbose = options.v
        Flags.show_matrix = options.m
        Flags.plot_graph = options.p

    @staticmethod
    def verbose_print(string):
        """Print the string ony in verbose mode"""
        if Flags.verbose:
            print(string)
