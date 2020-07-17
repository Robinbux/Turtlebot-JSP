#
# Converting the QUBO to BQM and sample on D-Wave machine
#
import timeit

import dimod
import neal
import time
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from dwave.system import LeapHybridSampler
from dwave_qbsolv import QBSolv
import hybrid
import dwave.inspector

num_reads = 1000  # Number of samples / quantum computations
chain_strength = 350  # Implementation parameter on the DWave QPU

anneal_time = 1000.0
pause_duration = 500.0  # Must be greater than 0
pause_start = 0.4  # Must be between 0 and 1

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        original_return_val = func(*args, **kwargs)
        end = time.time()
        print("time elapsed in ", func.__name__, ": ", end - start, sep='')
        return original_return_val

    return wrapper

@timing_decorator
def sim_sample(sampler, bqm):
    return sampler.sample(bqm=bqm, num_reads=num_reads)

@timing_decorator
def real_sample(sampler, bqm):
    return hybrid.KerberosSampler().sample(bqm)

def simulated_annealing(QUBO):
    bqm = dimod.BQM.from_qubo(QUBO)
    sampler = neal.SimulatedAnnealingSampler()


    #response = sim_sample(sampler, bqm)
    response = real_sample(sampler, bqm)


    return response

    #bqm = dimod.BinaryQuadraticModel.from_numpy_matrix(QUBO)
    #sampler = neal.SimulatedAnnealingSampler()
    #sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))
    #return QBSolv().sample_qubo(QUBO)
    #return sampler.sample(bqm=bqm, chain_strength=chain_strength)
    #return sampler.sample(bqm=bqm, num_reads=num_reads)
