import matplotlib

matplotlib.use('TkAgg')

from math import sqrt

from dask.distributed import Client
from jmetal.operator.crossover import SBXCrossover
from jmetal.operator.mutation import PolynomialMutation
from jmetal.problem import ZDT1
from jmetal.util.observer import ProgressBarObserver, VisualizerObserver
from jmetal.util.termination_criterion import StoppingByEvaluations

from sequoya.algorithm.multiobjective.nsgaii import DistributedNSGAII


class ZDT1Modified(ZDT1):
    """
    Problem ZDT1.

    .. note:: Version including a loop for increasing the computing time of the evaluation functions.
    """

    def evaluate(self, solution):
        g = self.__eval_g(solution)
        h = self.__eval_h(solution.variables[0], g)

        solution.objectives[0] = solution.variables[0]
        solution.objectives[1] = h * g

        s: float = 0.0
        for i in range(50000000):
            s += i * 0.235 / 1.234

        return solution

    def __eval_g(self, solution):
        g = sum(solution.variables) - solution.variables[0]

        constant = 9.0 / (solution.number_of_variables - 1)
        g = constant * g
        g = g + 1.0

        return g

    def __eval_h(self, f: float, g: float) -> float:
        return 1.0 - sqrt(f / g)

    def get_name(self):
        return 'ZDT1m'


if __name__ == '__main__':
    # setup Dask client
    client = Client('192.168.213.3:8786')

    ncores = sum(client.ncores().values())
    print(f'{ncores} cores available on cluster')

    # creates the problem
    problem = ZDT1()

    # creates the algorithm
    max_evaluations = 25000

    algorithm = DistributedNSGAII(
        problem=problem,
        population_size=100,
        mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
        crossover=SBXCrossover(probability=1.0, distribution_index=20),
        termination_criterion=StoppingByEvaluations(max_evaluations=max_evaluations),
        number_of_cores=ncores,
        client=client
    )

    algorithm.observable.register(observer=ProgressBarObserver(max=max_evaluations))
    algorithm.observable.register(observer=VisualizerObserver())

    algorithm.run()
    front = algorithm.get_result()

    print('Computing time: ' + str(algorithm.total_computing_time))
