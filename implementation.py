'''This file contains a skeleton implementation for the practical assignment 
for the NACO 21/22 course. 

Your Genetic Algorithm should be callable like so:
    >>> problem = ioh.get_problem(...)
    >>> ga = GeneticAlgorithm(...)
    >>> ga(problem)

In order to ensure this, please inherit from the provided Algorithm interface,
in a similar fashion as the RandomSearch Example:
    >>> class GeneticAlgorithm(Algorithm):
    >>>     ...

Please be sure to use don't change this name (GeneticAlgorithm) for your implementation.

If you override the constructor in your algoritm code, please be sure to 
call super().__init__, in order to correctly setup the interface. 

Only use keyword arguments for your __init__ method. This is a requirement for the
test script to properly evaluate your algoritm.
'''

from math import perm
import ioh
import random
from algorithm import Algorithm
from objective_function import *

class RandomSearch(Algorithm):
    '''An example of Random Search.'''

    def __call__(self, id, problem: ioh.problem.Integer) -> None:
        self.y_best: float = float("-inf")
        for iteration in range(self.max_iterations):
            # Generate a random bit string
            if id == 2: x: list[int] = [random.randint(0, 1) for _ in range(problem.meta_data.n_variables)]
            else: x: list[int] = [random.randint(0, 2) for _ in range(problem.meta_data.n_variables)]
            # Call the problem in order to get the y value    
            y: float = problem(x)
            # update the current state
            self.y_best = max(self.y_best, y)
            
            
class GeneticAlgorithm(Algorithm):
    '''A skeleton (minimal) implementation of your Genetic Algorithm.'''

    def __call__(self, id, problem: ioh.problem.Integer) -> None: 
        #parameters for algorithms
        toBeSelected, populationSize, chanceToFlip = 8, 20, 4
    
        population = []
        for x in range(populationSize):
            if (id == 2):
                population.append([random.randint(0, 1) for _ in range(problem.meta_data.n_variables)])
            else:
                population.append([random.randint(0, 2) for _ in range(problem.meta_data.n_variables)])
        for iteration in range(self.max_iterations):
            bestOfPopulation = selectionVariant2(population, problem, toBeSelected)
            nextGen = recombinationVariant1(id, bestOfPopulation, problem, populationSize)
            mutationVariant1(id, nextGen, chanceToFlip)
            population = nextGen
            
    
#roulette wheel selection
def selectionVariant1(currentGen, problem, toBeSelected):
    #parameter for selection
    bestOfPopulation = []
    #creates array for fitnessScores
    totalFitness = 0
    fitnessArray = []
    for individual in currentGen:
        fitnessArray.append(totalFitness)
        totalFitness += problem(individual)
        
    #selects individuasls based on scores
    for _ in range(toBeSelected):
        fitnessScore = random.uniform(0, totalFitness)
        searchIndex = len(currentGen) - 1
        fitnessSearch = fitnessArray[searchIndex]
        while fitnessScore <= fitnessSearch and searchIndex >= 1:
            searchIndex -= 1
            fitnessSearch = fitnessArray[searchIndex]
        bestOfPopulation.append(currentGen[searchIndex])
    return bestOfPopulation
    
#Simply select the best (risk local maximum)
def selectionVariant2(currentGen, problem, toBeSelected):
    currentGen.sort(key=problem, reverse=True)
    nextGen = []
    for i in range(toBeSelected):
        nextGen.append(currentGen[i])
    return nextGen
            


def recombinationVariant1(id, bestOfPopulation, problem, populationSize):
    nextGen = []
    for i in range(populationSize):
        #choosing parents
        father = bestOfPopulation[random.randint(0, len(bestOfPopulation) - 1)]
        mother = bestOfPopulation[random.randint(0, len(bestOfPopulation) - 1)]
        
        #adding random genes of parents
        crossover_mask = [random.randint(0, 1) for _ in range(problem.meta_data.n_variables)]
        child = []
        index = 0
        for gene in crossover_mask:
            if gene == 1:
                child.append(father[index])
            else:
                child.append(mother[index])
            index += 1
        #adding child
        nextGen.append(child)
    return nextGen
        
def mutationVariant1(id, population, chanceToFlip):
    for individual in population:
        chance = random.randint(0, chanceToFlip-1)
        if chance < 1:
            if (id == 2):
                chromosomeToFlip = random.randint(0, len(individual)-1)
                individual[chromosomeToFlip] = not individual[chromosomeToFlip]
            else:
                chromosomeToFlip = random.randint(0, len(individual)-1)
                if (individual[chromosomeToFlip] == 0): individual[chromosomeToFlip] = 1
                elif (individual[chromosomeToFlip] == 1): individual[chromosomeToFlip] = 2
                elif (individual[chromosomeToFlip] == 2): individual[chromosomeToFlip] = 0

    
    
def main():
    # Set a random seed in order to get reproducible results
    random.seed(42)

    #change id to determine (2 for 0,1) and (3 for 0,1,2)
    id = 2
    algorithm = GeneticAlgorithm()

    # Wrap objective_function as an ioh problem
    ioh.problem.wrap_integer_problem(
            objective_function,
            "objective_function_ca_1",
            ioh.OptimizationType.Maximization,
            0,
            1
    )
    problem = ioh.get_problem("objective_function_ca_1", dimension=60, problem_type='Integer')
    # Attach a logger to the problem
    logger = ioh.logger.Analyzer(store_positions=True)
    problem.attach_logger(logger)

    # run your algoritm on the problem
    algorithm(id, problem)
    
    print(problem.state.current_best.x)


if __name__ == '__main__':
    main()
