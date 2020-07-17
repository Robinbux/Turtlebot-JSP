from Flags.Flags import Flags
from JSPConstraint.JSPConstraint import JSPConstraint
from JSPOptimization.JSPOptimization import JSPOptimization
from JSPSolver.JSPSolver import JSPSolver
from TurtlebotConstraint.TurtlebotConstraint import TurtlebotConstraint
from lagrange.Lagrange import Lagrange
from sampler.sampler import simulated_annealing
from utils import utils
from utils.utils import print_params, print_response


def main(args=None):
    Lagrange.load_params()
    Flags.parse_arguments(args)

    Flags.verbose_print("Starting...")

    nbr_of_constraint_success = 0
    total_number_of_tries = 0
    while nbr_of_constraint_success < 1 and total_number_of_tries < 1000:

        jsp_constraint = JSPConstraint()
        jsp_constraint.add_constraints()

        jsp_optimization = JSPOptimization()
        jsp_optimization.add_optimizations()

        turtlebot_constraint = TurtlebotConstraint()
        turtlebot_constraint.add_constraints()

        response = simulated_annealing(JSPSolver.QUBO)

        

        jsp_constraint_passed = True
        # Check JSP Constraint
        failed_constraint = jsp_constraint.validate_response(response)
        if failed_constraint == 'h1':
            Flags.verbose_print("Failed at h1. Increasing alpha")
            Lagrange.alpha += 1
            nbr_of_constraint_success = 0
            jsp_constraint_passed = False
        elif failed_constraint == 'h2':
            Flags.verbose_print("Failed at h2. Increasing beta")
            Lagrange.beta += 1
            nbr_of_constraint_success = 0
            jsp_constraint_passed = False
        elif failed_constraint == 'h3':
            Flags.verbose_print("Failed at h3. Increasing gamma")
            Lagrange.gamma += 1
            nbr_of_constraint_success = 0
            jsp_constraint_passed = False 

        # Check Turtlebot Constraint
        if jsp_constraint_passed:
            failed_constraint = turtlebot_constraint.validate_response(response)
            if failed_constraint == 'h4':
                Flags.verbose_print("Failed at h4. Increasing eta")
                Lagrange.eta += 1
                nbr_of_constraint_success = 0
            elif failed_constraint == 'h5':
                Flags.verbose_print("Failed at h5. Increasing theta")
                Lagrange.theta += 1
                nbr_of_constraint_success = 0
            elif failed_constraint == 'h6':
                Flags.verbose_print("Failed at h6. Increasing iota")
                Lagrange.iota += 1
                nbr_of_constraint_success = 0
            elif failed_constraint == 'h7':
                Flags.verbose_print("Failed at h7. Increasing kappa")
                Lagrange.kappa += 1
                nbr_of_constraint_success = 0
            elif failed_constraint == 'h8':
                Flags.verbose_print("Failed at h8. Increasing my")
                Lagrange.my += 1
                nbr_of_constraint_success = 0

        print_params()

        nbr_of_constraint_success += 1


        total_number_of_tries += 1

    print_params()
    print_response(response)
    jsp_constraint.print_operation_results(response)
    jsp_constraint.plot_operations(response)
    jsp_constraint.plot_matrix()


if __name__ == "__main__":
    main()
