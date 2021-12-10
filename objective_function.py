import typing
import ioh

from implementation import RandomSearch

def ternary (n):
    if n == 0:
        return '0'
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))

class CellularAutomata:
    
    def __init__(self, rule_number: int):
        self.k = 2
        bitString = bin(rule_number)
        lastPart = bitString[2:len(bitString)]
        if rule_number > 500:
            self.k = 3
            lastPart = ternary(rule_number)
        self.rule = lastPart

    def __call__(self, c0: typing.List[int], t: int) -> typing.List[int]:
        '''Evaluate for T timesteps. Return Ct for a given C0.'''
        oldC0 = c0
        for _ in range(t):
            newC0 = []
            for index in range(len(oldC0)):
                prevCell = 0
                if index != 0:
                    prevCell = oldC0[index-1]
                nextCell = 0
                if index != len(oldC0) - 1:
                    nextCell = oldC0[index + 1]
                cellList = [prevCell, oldC0[index], nextCell]
                place = 0
                for cellIndex in range(len(cellList)):
                    place += cellList[2 - cellIndex] * (self.k**cellIndex)
                if place > len(self.rule):
                    newC0.append(0)
                else:
                    newC0.append(int(self.rule[len(self.rule)-1-place]))
            oldC0 = newC0
        return oldC0


def objective_function(c0_prime: typing.List[int]) -> float:
    '''Skeleton objective function. You should implement a method
    which computes a similarity measure between c0_prime a suggested by your
    GA, with the true c0 state for the ct state given in the sup. material. '''
    
    ct, rule, t = None, None, None # Given by the sup. material 

    ca = CellularAutomata(rule)
    ct_prime = ca(c0_prime, t)

    positives, negatives = 0, 0
    for bit in range(0, len(str(c0_prime))):
        if (str(c0_prime)[bit] == str(ct_prime)[bit]):
            positives += 1
        else:
            negatives += 1

    similarity = (positives / (negatives + positives)) * 100

    return similarity

def objective_function2(c0_prime: typing.List[int]) -> float:
    '''Skeleton objective function. You should implement a method
    which computes a similarity measure between c0_prime a suggested by your
    GA, with the true c0 state for the ct state given in the sup. material. '''
    
    ct, rule, t = None, None, None # Given by the sup. material 

    ca = CellularAutomata(rule)
    ct_prime = ca(c0_prime, t)

    #this objective function also takes in account how close both bits are
    #1-2 is closer than 0-2
    c0Str = str(c0_prime)
    ctStr = str(ct_prime)
    length = len(c0Str)
    totalDiff = 0
    for bit in range(0, length):
        totalDiff += (2-abs(int(c0Str[bit])-int(ctStr[bit])))*0.5

    #return similarity percentage
    return totalDiff / length * 100



        
def example():
    '''An example of wrapping a objective function in ioh and collecting data
    for inputting in the analyzer.'''
    
    #change id to determine (2 for 0,1) and (3 for 0,1,2)
    algorithm = RandomSearch()

    # Wrap objective_function as an ioh problem
    problem = ioh.problem.wrap_integer_problem(
            objective_function,
            "objective_function_ca_1",
            60, 
            ioh.OptimizationType.Maximization,
            ioh.IntegerConstraint([0]*60, [1]*60)
    )
    # Attach a logger to the problem
    logger = ioh.logger.Analyzer(store_positions=True)
    problem.attach_logger(logger)

    # run your algoritm on the problem
    algorithm(id, problem)



if __name__ == '__main__':
    #example()
    file1 = open('ca_input.csv','r')
    lines = file1.readlines()
    inputArray = []
    for index in range(len(lines)):
        if index != 0:
            newInput = []
            split1 = lines[index].split(",",1)
            k = int(split1[0])
            split2 = split1[1].split(",",1)
            rule = int(split2[0])
            split3 = split2[1].split(",",1)
            T = int(split3[0])
            CT = split3[1]
            CTArray = []
            CTSplit = CT.split("[")[1]
            CTSplit = CTSplit.split("]")[0]
            CTSplit = CTSplit.split(",")
            for number in CTSplit:
                CTArray.append(int(number))
            newInput.append(k)
            newInput.append(rule)
            newInput.append(T)
            newInput.append(CTArray)
            inputArray.append(newInput)
    cellularAutomata = CellularAutomata(inputArray[5][1])
    print(inputArray[5][3])
    print(cellularAutomata(inputArray[5][3], inputArray[5][2]))
    print(ternary(inputArray[5][1]))
    
    
    
