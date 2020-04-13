import numpy as np
from JSPSolver.JSPSolver import JSPSolver


class TurtlebotConstraint(JSPSolver):

    def __init__(self, eta, theta, iota):
        super().__init__()
        self.ETA = eta
        self.THETA = theta
        self.IOTA = iota

    def add_constraints(self):
        self.__add_h4_constraint()
        self.__add_h5_constraint()
        self.__add_h6_constraint()

    #
    # h4 implementation
    #
    def __add_h4_constraint(self):
        for i in range(self.NUMBER_OF_OPERATIONS):
            for u in range(self.UPPER_TIME_LIMIT):
                for t in range(u):
                    self.fill_QUBO_with_indexes(i, t, i, u, self.ALPHA * 2)
            for t in range(self.UPPER_TIME_LIMIT):
                self.fill_QUBO_with_indexes(i, t, i, t, -self.ALPHA)

    #
    # h5 implementation
    #
    def __add_h5_constraint(self):
        def Rm_condition_fulfilled(i, t, k, t_prime, M):
            return i != k and 0 <= t and t_prime <= M and 0 <= t_prime - t < self.get_operation_x(i)[1]

        for m in range(self.NUMBER_OF_MACHINES):
            operation_indexes_m = self.get_operation_indexes_for_machine_m(m)
            for i in operation_indexes_m:
                for i_prime in operation_indexes_m:
                    for t in range(self.UPPER_TIME_LIMIT):
                        for t_prime in range(self.UPPER_TIME_LIMIT):
                            if Rm_condition_fulfilled(i, t, i_prime, t_prime, self.UPPER_TIME_LIMIT):
                                self.fill_QUBO_with_indexes(i, t, i_prime, t_prime, self.BETA)

    #
    # h6 implementation
    #
    def __add_h6_constraint(self):
        nbr_jobs = len(self.JOBS_DATA)
        for j in range(nbr_jobs):
            for i in self.get_operation_indexes_for_job_j(j)[:-1]:
                for t in range(self.UPPER_TIME_LIMIT):
                    for t_prime in range(self.UPPER_TIME_LIMIT):
                        if (t + self.get_operation_x(i)[1]) > t_prime:
                            self.fill_QUBO_with_indexes(i, t, i + 1, t_prime, self.GAMMA)
