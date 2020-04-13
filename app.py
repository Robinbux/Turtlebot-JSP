import sys
import numpy as np

from Flags.Flags import Flags
from JSPConstraint.JSPConstraint import JSPConstraint
from JSPOptimization.JSPOptimization import JSPOptimization
from JSPSolver.JSPSolver import JSPSolver
from sampler.sampler import simulated_annealing
from utils import utils
from utils.utils import print_params, print_response


def main(args=None):
    params = utils.load_params()
    Flags.parse_arguments(args)

    nbr_of_constraint_success = 0
    while nbr_of_constraint_success < 10:

        jsp_constraint = JSPConstraint(params["alpha"], params["beta"], params["gamma"])
        jsp_constraint.add_constraints()

        jsp_optimization = JSPOptimization(params["delta"], params["epsilon"], params["zeta"])
        jsp_optimization.add_optimizations()

        response = simulated_annealing(JSPSolver.QUBO)
        failed_constraint = jsp_constraint.validate_response(response)

        if failed_constraint == 'h1':
            Flags.verbose_print("Failed at h1. Increasing alpha")
            params["alpha"] += 1
            nbr_of_constraint_success = 0
        elif failed_constraint == 'h2':
            Flags.verbose_print("Failed at h2. Increasing beta")
            params["beta"] += 1
            nbr_of_constraint_success = 0
        elif failed_constraint == 'h3':
            Flags.verbose_print("Failed at h3. Increasing gamma")
            params["gamma"] += 1
            nbr_of_constraint_success = 0

        print_params(params["alpha"], params["beta"], params["gamma"])

        nbr_of_constraint_success += 1

    print_params(params["alpha"], params["beta"], params["gamma"])
    print_response(response)
    jsp_constraint.print_operation_results(response)
    jsp_constraint.plot_operations(response)


if __name__ == "__main__":
    main()
