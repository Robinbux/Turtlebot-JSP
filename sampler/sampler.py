#
# Converting the QUBO to BQM and sample on D-Wave machine
#
import dimod
import neal

num_reads = 20  # Number of samples / quantum computations


def simulated_annealing(QUBO):
    bqm = dimod.BinaryQuadraticModel.from_numpy_matrix(QUBO)
    sampler = neal.SimulatedAnnealingSampler()

    return sampler.sample(bqm=bqm, num_reads=num_reads)
