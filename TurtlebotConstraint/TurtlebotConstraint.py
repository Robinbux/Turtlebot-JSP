import numpy as np
from JSPSolver.JSPSolver import JSPSolver


class TurtlebotConstraint(JSPSolver):

    def __init__(self, eta, theta, iota, kappa, my):
        super().__init__()
        self.ETA = eta
        self.THETA = theta
        self.IOTA = iota
        self.KAPPA = kappa
        self.MY = my

    def add_constraints(self):
        self.__add_h4_constraint()
        #self.__add_h5_constraint()
        self.__add_h6_constraint()
        self.__add_h7_constraint()
        self.__add_h8_constraint()

    def validate_response(self, response):
        """Returns constraint, if not followed, None otherwise"""
        operation_results = self.convert_response_to_operation_results(response)
        quick_check = self.response_quick_check_must_fix_later(response)
        if quick_check == 'h4':
            return 'h4'
        if not self.__h4_constraint_is_fulfilled(operation_results): return 'h4'
        #if not self.__h5_constraint_is_fulfilled(operation_results): return 'h5'
        if not self.__h7_constraint_is_fulfilled(operation_results): return 'h7'
        if not self.__h8_constraint_is_fulfilled(operation_results): return 'h8'
        if not self.__h6_constraint_is_fulfilled(operation_results): return 'h6'
        return None

    #
    # h4 implementation
    #
    def __add_h4_constraint(self):
        for w in range(self.NUMBER_OF_WALKING_OPERATIONS):
            walking_operation_indexes = self.get_operation_indexes_for_walking_operation_w(w)
            for i in walking_operation_indexes:
                for t in range(self.UPPER_TIME_LIMIT):
                    self.fill_QUBO_with_indexes(i, t, i, t, self.ETA)
                    for t_prime in range(self.UPPER_TIME_LIMIT):
                        if t != t_prime:
                            self.fill_QUBO_with_indexes(i, t, i, t_prime, self.ETA)
                for i_prime in walking_operation_indexes:
                    if i_prime != i:
                        for t in range(self.UPPER_TIME_LIMIT):
                            for t_prime in range(self.UPPER_TIME_LIMIT):
                                self.fill_QUBO_with_indexes(i, t, i_prime, t_prime, self.ETA)
                for t in range(self.UPPER_TIME_LIMIT):
                    self.fill_QUBO_with_indexes(i, t, i, t, - 2*self.ETA)

    #
    # h5 implementation
    #
    def __add_h5_constraint(self):
        for b in range(self.NUMBER_OF_BOTS):
            walking_operation_indexes = self.get_walking_operation_indexes_for_bot_b(b)
            for i in walking_operation_indexes:
                for i_prime in walking_operation_indexes:
                    for t in range(self.UPPER_TIME_LIMIT):
                        for t_prime in range(self.UPPER_TIME_LIMIT):
                            if i != i_prime:
                                penalty =  max(t + self.get_operation_x(i)[1] - t_prime, 0) * self.THETA
                                self.fill_QUBO_with_indexes(i, t, i_prime, t_prime, penalty)

    #
    # h6 implementation
    #
    def __add_h6_constraint(self):
        for b in range(self.NUMBER_OF_BOTS):
            walking_operation_indexes = self.get_walking_operation_indexes_for_bot_b(b)
            for i in walking_operation_indexes:
                for i_prime in walking_operation_indexes:
                    if i != i_prime:
                        for t_prime in range(self.UPPER_TIME_LIMIT):
                            for t in range(t_prime + 1):
                                machine_end_i = self.get_operation_x(i)[3]
                                machine_start_i_prime = self.get_operation_x(i_prime)[2]
                                walktime_between_machines = self.WALKING_TIME[machine_end_i][machine_start_i_prime]
                                penalty = max(t + self.get_operation_x(i)[1] + walktime_between_machines - t_prime, 0)
                                self.fill_QUBO_with_indexes(i, t, i_prime, t_prime, penalty * self.IOTA)

    #
    # h7 implementation
    #
    def __add_h7_constraint(self):
        for i in range(self.NUMBER_OF_OPERATIONS):
            for i_prime in self.get_walking_operations_indexes_for_standard_operation_x(i):
                for t in range(self.UPPER_TIME_LIMIT):
                    for t_prime in range(self.UPPER_TIME_LIMIT):
                        penalty = max(t_prime + self.get_operation_x(i_prime)[1] - t, 0)
                        self.fill_QUBO_with_indexes(i, t, i_prime, t_prime, penalty * self.KAPPA)

    #
    # h8 implementation
    #
    def __add_h8_constraint(self):
        for w in range(self.NUMBER_OF_WALKING_OPERATIONS):
            for i in self.get_operation_indexes_for_walking_operation_w(w):
                for t in range(self.UPPER_TIME_LIMIT):
                    for t_prime in range(self.UPPER_TIME_LIMIT):
                        standard_op_idx = self.get_standard_operation_index_before_individual_walking_operation_w(i)
                        penalty = max(t_prime + self.get_operation_x(standard_op_idx)[1] - t, 0)
                        self.fill_QUBO_with_indexes(i, t, standard_op_idx, t_prime, penalty * self.MY)

    # AUTOMATIZATION
    # Check for h4
    def __h4_constraint_is_fulfilled(self, operation_results):
        for w in range(self.NUMBER_OF_WALKING_OPERATIONS):
            picked_ops = 0
            for o in self.get_operation_indexes_for_walking_operation_w(w):
                if o in operation_results:
                    picked_ops += 1
            if picked_ops != 1:
                return False
        return True

    # Check for h5
    def __h5_constraint_is_fulfilled(self, operation_results):
        for b in range(self.NUMBER_OF_BOTS):
            free_time_slots = np.zeros(self.UPPER_TIME_LIMIT)
            walking_operation_indexes = self.get_walking_operation_indexes_for_bot_b(b)
            for i in walking_operation_indexes:
                if i in operation_results:
                    processing_time = self.FLATTENED_OPERATIONS[i][1]
                    if 1 in free_time_slots[operation_results[i]: operation_results[i] + processing_time]:
                        return False
                    free_time_slots[operation_results[i]: operation_results[i] + processing_time] = 1
        return True

    # Check for h6
    def __h6_constraint_is_fulfilled(self, operation_results):
        for b in range(self.NUMBER_OF_BOTS):
            operation_time_slots = []
            walking_operation_indexes = self.get_walking_operation_indexes_for_bot_b(b)
            for i in walking_operation_indexes:
                if i in operation_results:
                    operation_time_slots.append((operation_results[i], i))
            # Sort by time
            operation_time_slots.sort(key=lambda x: x[0])
            for i in range(len(operation_time_slots) - 1):
                walking_op = self.get_operation_x(operation_time_slots[i][1])
                # operation_time_slots[i][1] # wann startet es?
                # walking_op[1] # wie lange braucht es?
                # walking_op[3] # wo ended es
                # self.get_operation_x(i+1)[2] # wo fängt das nächste an?
                # self.WALKING_TIME[walking_op[3]][self.get_operation_x(operation_time_slots[i+1][1])[2]] # Laufzeit
                # operation_time_slots[i+1][1] # Wann fängt das nächste an
                if operation_time_slots[i][1] + walking_op[1] + \
                        self.WALKING_TIME[walking_op[3]][self.get_operation_x(operation_time_slots[i+1][1])[2]] \
                        > operation_time_slots[i + 1][1]:
                    return False
        return True

    # Check for h7
    def __h7_constraint_is_fulfilled(self, operation_results):
        for i in range(self.NUMBER_OF_OPERATIONS):
            for w in self.get_walking_operations_indexes_for_standard_operation_x(i):
                if w in operation_results:
                    if operation_results[w] + self.get_operation_x(w)[1] > operation_results[i]:
                        return False
        return True

    # Check for h8
    def __h8_constraint_is_fulfilled(self, operation_results):
        for w in range (self.NUMBER_OF_OPERATIONS, len(self.FLATTENED_OPERATIONS)):
            if w in operation_results:
                i = self.get_standard_operation_index_before_individual_walking_operation_w(w)
                if operation_results[i] + self.get_operation_x(i)[1] > operation_results[w]:
                    return False
        return True
