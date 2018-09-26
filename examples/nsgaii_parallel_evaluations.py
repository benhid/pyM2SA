from jmetal.component import ProgressBarObserver, RankingAndCrowdingDistanceComparator, VisualizerObserver
from jmetal.operator import BinaryTournamentSelection
from pymsa.core.score import SumOfPairs, PercentageOfTotallyConservedColumns

from pym2sa.algorithm import NSGA2BAliBASE
from pym2sa.component.evaluator import MultithreadedEvaluator
from pym2sa.problem import BAliBASE
from pym2sa.operator import SPXMSA, TwoRandomAdjacentGapGroup
from pym2sa.util.graphic import MSAPlot


if __name__ == '__main__':
    # Creates the problem
    problem = BAliBASE(instance='BB12010', balibase_path='../resources',
                       score_list=[SumOfPairs(), PercentageOfTotallyConservedColumns()])
    problem.obj_labels = ['SOP', '%TC']

    # Creates the algorithm
    algorithm = NSGA2BAliBASE(
        problem=problem,
        population_size=100,
        max_evaluations=10000,
        mutation=TwoRandomAdjacentGapGroup(probability=0.2),
        crossover=SPXMSA(probability=0.8),
        selection=BinaryTournamentSelection(comparator=RankingAndCrowdingDistanceComparator()),
        evaluator=MultithreadedEvaluator(n_workers=4)
    )

    visualizer = VisualizerObserver()
    algorithm.observable.register(observer=visualizer)

    progress_bar = ProgressBarObserver(step=1, maximum=10000)
    algorithm.observable.register(progress_bar)

    algorithm.run()
    front = algorithm.get_result()

    # Plot the solution
    pareto_front = MSAPlot(plot_title='NSGAII for ' + problem.instance, axis_labels=problem.obj_labels)
    pareto_front.plot(front)
    pareto_front.to_html(filename='NSGAII-' + problem.instance)

    print('Computing time: ' + str(algorithm.total_computing_time))
