from Flags.Flags import Flags
from JSPConstraint.JSPConstraint import JSPConstraint
from JSPOptimization.JSPOptimization import JSPOptimization
from JSPSolver.JSPSolver import JSPSolver
from TurtlebotConstraint.TurtlebotConstraint import TurtlebotConstraint
from sampler.sampler import simulated_annealing
from utils import utils
from utils.utils import print_params, print_response


def main(args=None):
    params = utils.load_params()
    Flags.parse_arguments(args)

    nbr_of_constraint_success = 0
    total_number_of_tries = 0
    while nbr_of_constraint_success < 10 and total_number_of_tries < 1000:

        jsp_constraint = JSPConstraint(params["alpha"], params["beta"], params["gamma"])

        #jsp_constraint.plot_operations()
        #return


        jsp_constraint.add_constraints()

        jsp_optimization = JSPOptimization(params["delta"], params["epsilon"], params["zeta"])
        jsp_optimization.add_optimizations()

        turtlebot_constraint = TurtlebotConstraint(params["eta"], params["theta"], params["iota"], params["kappa"], params["my"])
        turtlebot_constraint.add_constraints()

        response = simulated_annealing(JSPSolver.QUBO)

        jsp_constraint_passed = True
        # Check JSP Constraint
        failed_constraint = jsp_constraint.validate_response(response)
        if failed_constraint == 'h1':
            Flags.verbose_print("Failed at h1. Increasing alpha")
            params["alpha"] += 1
            nbr_of_constraint_success = 0
            jsp_constraint_passed = False
        elif failed_constraint == 'h2':
            Flags.verbose_print("Failed at h2. Increasing beta")
            params["beta"] += 1
            nbr_of_constraint_success = 0
            jsp_constraint_passed = False
        elif failed_constraint == 'h3':
            Flags.verbose_print("Failed at h3. Increasing gamma")
            params["gamma"] += 1
            nbr_of_constraint_success = 0
            jsp_constraint_passed = False

        # Check Turtlebot Constraint
        if jsp_constraint_passed:
            failed_constraint = turtlebot_constraint.validate_response(response)
            if failed_constraint == 'h4':
                Flags.verbose_print("Failed at h4. Increasing eta")
                params["eta"] += 1
                nbr_of_constraint_success = 0
            elif failed_constraint == 'h5':
                Flags.verbose_print("Failed at h5. Increasing theta")
                params["theta"] += 1
                nbr_of_constraint_success = 0
            elif failed_constraint == 'h6':
                Flags.verbose_print("Failed at h6. Increasing iota")
                params["iota"] += 1
                nbr_of_constraint_success = 0
            elif failed_constraint == 'h7':
                Flags.verbose_print("Failed at h7. Increasing kappa")
                params["kappa"] += 1
                nbr_of_constraint_success = 0
            elif failed_constraint == 'h8':
                Flags.verbose_print("Failed at h8. Increasing my")
                params["my"] += 1
                nbr_of_constraint_success = 0

        print_params(params["alpha"], params["beta"], params["gamma"], params["eta"], params["theta"], params["iota"], params["kappa"], params["my"])

        nbr_of_constraint_success += 1
        total_number_of_tries += 1

    print_params(params["alpha"], params["beta"], params["gamma"], params["eta"], params["theta"], params["iota"], params["kappa"], params["my"])
    print_response(response)
    jsp_constraint.print_operation_results(response)
    jsp_constraint.plot_operations(response)
    jsp_constraint.plot_matrix()


if __name__ == "__main__":
    main()
