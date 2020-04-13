import numpy as np
import plotly.figure_factory as ff

from Flags.Flags import Flags


class JSPSolver:
    """Manually set jobs for testing purposes"""

    QUBO = np.zeros((0, 0))
    qubo_initialized = False

    def __init__(self):
        # Jobs
        self.JOBS_DATA = [  # task = (machine_id, processing_time).
            [(0, 2), (1, 1)],  # Job0
            [(1, 3), (0, 1)],  # Job1
        ]

        # Machine walking times
        self.WALKING_TIME = [
            [0, 1],
            [1, 0]
        ]

        self.NUMBER_OF_OPERATIONS = self.__get_number_of_operations()
        self.NUMBER_OF_MACHINES = self.__get_number_of_machines()
        self.NUMBER_OF_BOTS = 1
        self.NUMBER_OF_BOT_OPERATIONS = self.__get_number_of_bot_operations()
        self.UPPER_TIME_LIMIT = 5

        if not JSPSolver.qubo_initialized:
            QUBO_LENGTH = self.NUMBER_OF_OPERATIONS * self.UPPER_TIME_LIMIT
            JSPSolver.QUBO = np.zeros((QUBO_LENGTH, QUBO_LENGTH))
            JSPSolver.qubo_initialized = True

    def get_operation_x(self, x):
        op_idx = 0
        for j in self.JOBS_DATA:
            for o in j:
                if op_idx == x:
                    return o
                op_idx += 1

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

    def convert_response_to_operation_results(self, response):
        operation_results = {}
        for k, v in response.first[0].items():
            if v == 1:
                res = self.__convert_one_index_to_two(k)
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

    def print_operation_results(self, response):
        operation_results = self.convert_response_to_operation_results(response)
        for (k, v) in operation_results.items():
            print(f"Operation {str(k)} starts at time {str(v)}")

    def __get_number_of_operations(self):
        nbr_operations = 0
        for j in self.JOBS_DATA:
            nbr_operations += len(j)
        return nbr_operations

    def __get_number_of_bot_operations(self):
        nbr_bot_operations = 0
        for j in self.JOBS_DATA:
            nbr_bot_operations += len(j) - 1
        nbr_bot_operations *= self.NUMBER_OF_BOTS
        return nbr_bot_operations

    def __get_number_of_machines(self):
        machines = set()
        for j in self.JOBS_DATA:
            for o in j:
                machines.add(o[0])
        return len(machines)

    def __convert_two_indices_to_one(self, i, j):
        return i * self.UPPER_TIME_LIMIT + j

    def __convert_one_index_to_two(self, k):
        j = k % self.UPPER_TIME_LIMIT
        i = int((k - j) / self.UPPER_TIME_LIMIT)
        return [i, j]
