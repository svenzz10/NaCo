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
            objective_function,
            "objective_function_ca_1",
            ioh.OptimizationType.Maximization,
            60
    )
    problem = ioh.get_problem("objective_function_ca_1", dimension=60, problem_type='Integer')
    
    # Attach a logger to the problem
    logger = ioh.logger.Analyzer(store_positions=True)
    problem.attach_logger(logger)

    # run your algoritm on the problem
    algorithm(id, problem)



if __name__ == '__main__':
    # file1 = open('ca_input.csv','r')
    # lines = file1.readlines()
    # #Create array for each test case
    # inputArray = []
    # for index in range(len(lines)):
        # if index != 0:
            # #Create array for the variables of the test case
            # newInput = []
            # split1 = lines[index].split(",",1)
            # #Get K out of line
            # k = int(split1[0])
            # split2 = split1[1].split(",",1)
            # #Get the rule number out of the line
            # rule = int(split2[0])
            # split3 = split2[1].split(",",1)
            # #Get the T out of the line
            # T = int(split3[0])
            # #Get the CT out of the line
            # CT = split3[1]
            # CTArray = []
            # #Trim the brackets of it
            # CTSplit = CT.split("[")[1]
            # CTSplit = CTSplit.split("]")[0]
            # #Delimit this trimmed CT on a comma
            # CTSplit = CTSplit.split(",")
            # #Convert this list with strings to a list with integers
            # for number in CTSplit:
                # CTArray.append(int(number))
            # #Append all these variables to the test case
            # newInput.append(k)
            # newInput.append(rule)
            # newInput.append(T)
            # newInput.append(CTArray)
            # #finally append this test case to the list of test cases
            # inputArray.append(newInput)
    
    # k = inputArray[0][0]
    # rule = inputArray[0][1]
    # T = inputArray[0][2]
    # CTArray = inputArray[0][3]
    analyzeProblem()
    
    
    
