from jmetal.component import SequentialEvaluator, ProgressBarObserver, RankingAndCrowdingDistanceComparator, \
    VisualizerObserver
from jmetal.operator import BinaryTournamentSelection
from pymsa.core.score import SumOfPairs, PercentageOfTotallyConservedColumns

from pym2sa.algorithm import NSGA2MSA
from pym2sa.problem import BAliBASE
from pym2sa.operator import SPXMSA, ShiftClosedGapGroups
from pym2sa.util.graphic import MSAPlot


if __name__ == '__main__':
    # Creates the problem
    problem = BAliBASE(instance='BB12011', balibase_path='../resources',
                       score_list=[SumOfPairs(), PercentageOfTotallyConservedColumns()])
    problem.obj_labels = ['TC', 'SOP']

    # Creates the algorithm
    algorithm = NSGA2MSA(
        problem=problem,
        population_size=40,
        max_evaluations=300,
        mutation=ShiftClosedGapGroups(probability=0.2),
        crossover=SPXMSA(probability=0.8),
        selection=BinaryTournamentSelection(comparator=RankingAndCrowdingDistanceComparator()),
        evaluator=SequentialEvaluator()
    )

    #visualizer = VisualizerObserver()
    #algorithm.observable.register(observer=visualizer)

    progress_bar = ProgressBarObserver(step=100, maximum=300)
    algorithm.observable.register(progress_bar)

    algorithm.run()
    front = algorithm.get_result()

    # Plot the solution
    pareto_front = MSAPlot(plot_title='NSGAII for ' + problem.instance, axis_labels=problem.obj_labels)
    pareto_front.plot(front)
    pareto_front.to_html(filename='NSGAII-' + problem.instance)

    print('Computing time: ' + str(algorithm.total_computing_time))
