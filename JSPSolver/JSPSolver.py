import numpy as np
import plotly.figure_factory as ff

from Flags.Flags import Flags


class JSPSolver:
    """Manually set jobs for testing purposes"""

    QUBO = np.zeros((0, 0))
    qubo_initialized = False

    def __init__(self):
        # Jobs
        #self.JOBS_DATA = [  # task = (machine_id, processing_time).
        #    [(0, 1), (1, 1)],  # Job0
        #    [(1, 1), (0, 1)],  # Job1
        #]

        # Machine walking times
        #self.WALKING_TIME = [
        #    [0, 1],
        #    [1, 0]
        #]

        self.JOBS_DATA = [  # task = (machine_id, processing_time).
            [(0, 2), (1, 1)],  # Job0
            [(0, 1), (2, 1), (0, 2)]  # Job1
        ]

        self.WALKING_TIME = [
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0]
         ]

        self.NUMBER_OF_OPERATIONS = self.__get_number_of_operations()
        self.NUMBER_OF_MACHINES = self.__get_number_of_machines()
        self.NUMBER_OF_BOTS = 2
        self.NUMBER_OF_WALKING_OPERATIONS = self.__get_number_of_walking_operations()
        self.NUMBER_OF_INDIVIDUAL_WALKING_OPERATIONS = self.NUMBER_OF_WALKING_OPERATIONS * self.NUMBER_OF_BOTS
        self.UPPER_TIME_LIMIT = 8
        self.MAX_WALK_TIME = self.__get_max_walk_time()

        self.FLATTENED_OPERATIONS = self.__merge_operations()

        if not JSPSolver.qubo_initialized:
            QUBO_LENGTH = self.UPPER_TIME_LIMIT * (self.NUMBER_OF_OPERATIONS + self.NUMBER_OF_INDIVIDUAL_WALKING_OPERATIONS)
            JSPSolver.QUBO = np.zeros((QUBO_LENGTH, QUBO_LENGTH))
            JSPSolver.qubo_initialized = True

    def get_operation_x(self, x):
        return self.FLATTENED_OPERATIONS[x]

    def get_operation_indexes_for_machine_m(self, m):
        indexes = []
        op_idx = 0
        for j in self.JOBS_DATA:
            for o in j:
                if o[0] == m:
                    indexes.append(op_idx)
                op_idx += 1
        return indexes

    def get_operation_indexes_for_job_j(self, j):
        op_idx = 0
        for i in range(j):
            op_idx += len(self.JOBS_DATA[i])
        return list(range(op_idx, op_idx + len(self.JOBS_DATA[j])))

    def fill_QUBO_with_indexes(self, i, t, i_prime, t_prime, value):
        index_a = self.__convert_two_indices_to_one(i, t)
        index_b = self.__convert_two_indices_to_one(i_prime, t_prime)
        if index_a > index_b:
            index_a, index_b = index_b, index_a
        JSPSolver.QUBO[index_a][index_b] += value

    def response_quick_check_must_fix_later(self, response):
        operation_results = {}
        for k, v in response.first[0].items():
            if v == 1:
                res = self.convert_one_index_to_two(k)
                if res[0] in operation_results:
                    if res[0] >= self.NUMBER_OF_OPERATIONS:  # TODO: Find a more elegant solution, but I'm tired now
                        return 'h4'
                    return 'h1'
                operation_results[res[0]] = res[1]
        return None

    def convert_response_to_operation_results(self, response):
        operation_results = {}
        for k, v in response.first[0].items():
            if v == 1:
                res = self.convert_one_index_to_two(k)
                operation_results[res[0]] = res[1]
        return operation_results

    def plot_operations(self, response):
        if not Flags.plot_graph:
            return
        operation_results = self.convert_response_to_operation_results(response)
        df = []

        for j in range(len(self.JOBS_DATA)):
            for o in self.get_operation_indexes_for_job_j(j):
                operation = self.get_operation_x(o)
                df.append(
                    dict(Task=f"Machine-{operation[0]}  ", Start=operation_results[o],
                         Finish=operation_results[o] + operation[1],
                         Resource=f"Job-{j}"))

        colors = {'Job-0': 'rgb(76,59,77)',
                  'Job-1': 'rgb(165,56,96)',
                  'Job-2': 'rgb(97,201,168)',
                  'Job-3': 'rgb(255,238,219)'}

        fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                              group_tasks=True, bar_width=0.3, title='Solution')

        fig.layout.xaxis = dict(
            automargin=True,
            dtick=1,
            title_text="Time t")

        fig.layout.yaxis.autorange = True

        fig.show()

    def get_operation_indexes_for_walking_operation_w(self, w):
        """Return a list off all indexes of Ww"""
        start_point = self.NUMBER_OF_OPERATIONS + w * self.NUMBER_OF_BOTS
        return list(range(start_point, start_point + self.NUMBER_OF_BOTS))

    def get_walking_operation_indexes_for_bot_b(self, b):
        """Return a list of all walking operation indexes for Bot b"""
        return np.arange(self.NUMBER_OF_OPERATIONS + b, len(self.FLATTENED_OPERATIONS), self.NUMBER_OF_BOTS).tolist()

    def get_walking_operations_indexes_for_standard_operation_x(self, x):
        current_big_w_passed = 0
        current_op_passed = 0
        for j in self.JOBS_DATA:
            if current_op_passed + len(j) <= x:
                current_op_passed += len(j)
                current_big_w_passed += len(j) - 1
            else:
                w = x - current_op_passed + current_big_w_passed - 1
                if w < current_big_w_passed:
                    return []
                return self.get_operation_indexes_for_walking_operation_w(w)

    def get_standard_operation_index_before_individual_walking_operation_w(self, w):
        w = self.__transform_individual_to_big_walking_operation(w)
        current_big_w_passed = 0
        for idx, j in enumerate(self.JOBS_DATA):
            if current_big_w_passed + len(j) - 1 <= w:
                current_big_w_passed += len(j) - 1
            else:
                return w + idx

    def print_operation_results(self, response):
        operation_results = self.convert_response_to_operation_results(response)
        op_count = 0
        print("Standard Operations")
        print("----------------------------------")
        for (k, v) in operation_results.items():
            if op_count == self.NUMBER_OF_OPERATIONS:
                print("\nBot Operations")
                print("----------------------------------")
            print(f"Operation {str(k)} starts at time {str(v)}")
            op_count += 1

    def plot_matrix(self):
        if not Flags.show_matrix:
            return
        x = []
        y = []
        for o in range(len(self.FLATTENED_OPERATIONS)):
            for t in range(self.UPPER_TIME_LIMIT):
                x.append("X " + str(o) + "," + str(t))
                y.append("X " + str(o) + "," + str(t))

        y = list(reversed(y))

        fig = ff.create_annotated_heatmap(z=np.flip(self.QUBO, 0).astype(int), x=x, y=y)
        fig.show(renderer="browser")

    def __transform_individual_to_big_walking_operation(self, w):
        return int((w - self.NUMBER_OF_OPERATIONS) / self.NUMBER_OF_BOTS)

    def __merge_operations(self):
        """Flatten out operations for easier access and add bot operations at the end"""
        merged_operations = []
        # Flatten the operations
        for j in self.JOBS_DATA:
            merged_operations += j
        # Add the bot operations
        for j in self.JOBS_DATA:
            for o in range(len(j) - 1):
                for b in range(self.NUMBER_OF_BOTS):
                    start_machine = j[o][0]
                    end_machine = j[o+1][0]
                    walking_time = self.WALKING_TIME[start_machine][end_machine]
                    merged_operations += [(b, walking_time, start_machine, end_machine)]
        return merged_operations

    def __get_number_of_operations(self):
        nbr_operations = 0
        for j in self.JOBS_DATA:
            nbr_operations += len(j)
        return nbr_operations

    def __get_number_of_walking_operations(self):
        nbr_bot_operations = 0
        for j in self.JOBS_DATA:
            nbr_bot_operations += len(j) - 1
        return nbr_bot_operations

    def __get_number_of_machines(self):
        machines = set()
        for j in self.JOBS_DATA:
            for o in j:
                machines.add(o[0])
        return len(machines)

    def __get_max_walk_time(self):
        max_walk_time = 0
        for w in self.WALKING_TIME:
            if max(w) > max_walk_time:
                max_walk_time = max(w)
        return max_walk_time

    def __convert_two_indices_to_one(self, i, j):
        return i * self.UPPER_TIME_LIMIT + j

    def convert_one_index_to_two(self, k):
        j = k % self.UPPER_TIME_LIMIT
        i = int((k - j) / self.UPPER_TIME_LIMIT)
        return [i, j]
