import numpy as np
from JSPSolver.JSPSolver import JSPSolver


class JSPConstraint(JSPSolver):

    def __init__(self, alpha, beta, gamma):
        super().__init__()
        self.ALPHA = alpha
        self.BETA = beta
        self.GAMMA = gamma

    def add_constraints(self):
        self.__add_h1_constraint()
        self.__add_h2_constraint()
        self.__add_h3_constraint()

    def validate_response(self, response):
        """Returns constraint, if not followed, None otherwise"""
        operation_results = self.convert_response_to_operation_results(response)
        quick_check = self.response_quick_check_must_fix_later(response)
        if quick_check == 'h1':
            return 'h1'
        if not self.__h1_constraint_is_fulfilled(operation_results):
            return 'h1'
        if not self.__h2_constraint_is_fulfilled(operation_results):
            return 'h2'
        if not self.__h3_constraint_is_fulfilled(operation_results):
            return 'h3'
        return None

    #
    # h1 implementation
    #
    def __add_h1_constraint(self):
        for i in range(self.NUMBER_OF_OPERATIONS):
            for u in range(self.UPPER_TIME_LIMIT):
                for t in range(u):
                    self.fill_QUBO_with_indexes(i, t, i, u, self.ALPHA * 2)
            for t in range(self.UPPER_TIME_LIMIT):
                self.fill_QUBO_with_indexes(i, t, i, t, -self.ALPHA)

    #
    # h2 implementation
    #
    def __add_h2_constraint(self):
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
    # h3 implementation
    #
    def __add_h3_constraint(self):
        nbr_jobs = len(self.JOBS_DATA)
        for j in range(nbr_jobs):
            for i in self.get_operation_indexes_for_job_j(j)[:-1]:
                for t in range(self.UPPER_TIME_LIMIT):
                    for t_prime in range(self.UPPER_TIME_LIMIT):
                        if (t + self.get_operation_x(i)[1]) > t_prime:
                            self.fill_QUBO_with_indexes(i, t, i + 1, t_prime, self.GAMMA)

    # AUTOMATIZATION
    # Check for h1
    def __h1_constraint_is_fulfilled(self, operation_results):
        for i in range(self.NUMBER_OF_OPERATIONS):
            if i not in operation_results:
                return False
        return True

    # Check for h2
    def __h2_constraint_is_fulfilled(self, operation_results):
        for m in range(self.NUMBER_OF_MACHINES):
            arr = np.zeros((self.UPPER_TIME_LIMIT + 3,), dtype=np.int)
            for o in self.get_operation_indexes_for_machine_m(m):
                for i in range(operation_results[o], operation_results[o] + self.get_operation_x(o)[1]):
                    if arr[i] == 1:
                        return False
                    arr[i] = 1
        return True

    # Check for h3
    def __h3_constraint_is_fulfilled(self, operation_results):
        for j in range(len(self.JOBS_DATA)):
            for i in self.get_operation_indexes_for_job_j(j)[:-1]:
                if operation_results[i] + self.get_operation_x(i)[1] > operation_results[i + 1]:
                    return False
        return True
