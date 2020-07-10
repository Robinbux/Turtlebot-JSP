from JSPSolver.JSPSolver import JSPSolver
from lagrange.Lagrange import Lagrange


class JSPOptimization(JSPSolver):

    def __init__(self):
        super().__init__()

    def add_optimizations(self):
        self.__minimize_spaces_on_machine_level()
        self.__minimize_spaces_on_job_level()
        self.__optimize_time()

    #
    # Space Minimization -- Machine level
    #
    def __minimize_spaces_on_machine_level(self):
        for m in range(self.NUMBER_OF_MACHINES):
            operation_indexes_m = self.get_operation_indexes_for_machine_m(m)
            for i in range(len(operation_indexes_m)):
                for i_prime in range(len(operation_indexes_m)):
                    for t_prime in range(self.UPPER_TIME_LIMIT):
                        for t in range(t_prime):
                            if i_prime == i:
                                continue
                            penalty = (t_prime - (t + self.get_operation_x(operation_indexes_m[i])[1]))**2
                            self.fill_QUBO_with_indexes(operation_indexes_m[i], t, operation_indexes_m[i_prime],
                                                        t_prime, Lagrange.delta * penalty)

    #
    # Space Minimization -- Job level
    #
    def __minimize_spaces_on_job_level(self):
        for j in range(len(self.JOBS_DATA)):
            for i in self.get_operation_indexes_for_job_j(j)[:-1]:
                for t in range(self.UPPER_TIME_LIMIT):
                    for t_prime in range(self.UPPER_TIME_LIMIT):
                        penalty = (t_prime - (t + self.get_operation_x(i)[1]))**2
                        self.fill_QUBO_with_indexes(i, t, i + 1, t_prime, Lagrange.epsilon * penalty)

    #
    # General time optimization
    #
    def __optimize_time(self):
        for i in range(self.NUMBER_OF_OPERATIONS):
            for t in range(self.UPPER_TIME_LIMIT):
                self.fill_QUBO_with_indexes(i, t, i, t, Lagrange.zeta * (t + self.get_operation_x(i)[1]))