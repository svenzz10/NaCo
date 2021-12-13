import typing
import ioh

from implementation import RandomSearch, GeneticAlgorithm
from seperateFunction import *
        
def analyzeProblem():
    '''An example of wrapping a objective function in ioh and collecting data
    for inputting in the analyzer.'''
    
    #change id to determine (2 for 0,1) and (3 for 0,1,2)
    id = 2
    algorithm = GeneticAlgorithm()

    # Wrap objective_function as an ioh problem
    ioh.problem.wrap_integer_problem(
            objective_function2,
            "objective_function_ca_1",
            ioh.OptimizationType.Maximization,
            0,
            1
    )
    problem = ioh.get_problem("objective_function_ca_1", dimension=60, problem_type='Integer')
    print(type(problem))
    # Attach a logger to the problem
    logger = ioh.logger.Analyzer(store_positions=True)
    problem.attach_logger(logger)

    # run your algoritm on the problem
    algorithm(id, problem)
    print(problem.state.current_best.x)



if __name__ == '__main__':
    analyzeProblem()
    
    
    
