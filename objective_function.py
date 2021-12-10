import typing
import ioh

from implementation import RandomSearch, GeneticAlgorithm

#Used to convert decimal to base3 strings (Not created by us)
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
        #Defaults the k to 2
        self.k = 2
        bitString = bin(rule_number)
        #Makes the rule into a fitting binary string
        lastPart = bitString[2:len(bitString)] #Cut first part of as that is unnecessary clutter
        if rule_number > 500:
            #If the rule_number is > 500 (actually 256) it must be of type base 3
            #Therefore set k to 3 and change the rule from a binary to a ternary form
            self.k = 3
            lastPart = ternary(rule_number)
        #Make it a class variable
        self.rule = lastPart

    def __call__(self, c0: typing.List[int], t: int) -> typing.List[int]:
        '''Evaluate for T timesteps. Return Ct for a given C0.'''
        #copy into reusable more readable variable name
        oldC0 = c0
        for _ in range(t):
            newC0 = [] #create new list to append items to
            for index in range(len(oldC0)):
                #cell previous of current is by default 0
                prevCell = 0
                if index != 0:
                    #If it is not the first cell, check previous cell and assign
                    prevCell = oldC0[index-1]
                #next cell of current is by default 0
                nextCell = 0
                if index != len(oldC0) - 1:
                    #If it is not the last cell, check next cell and assign
                    nextCell = oldC0[index + 1]
                #Now put previous, current and next cell in a list
                cellList = [prevCell, oldC0[index], nextCell]
                #Place refers to where this cellList should refer to in the binary or ternary string
                place = 0
                for cellIndex in range(len(cellList)):
                    #Some wizard math, but it checks out
                    place += cellList[2 - cellIndex] * (self.k**cellIndex)
                if place > len(self.rule):
                    #If the place is more than the rule even refers to, it is automatically a 0
                    newC0.append(0)
                else:
                    #Else check the digit that corresponds to the place, reading from right to left
                    newC0.append(int(self.rule[len(self.rule)-1-place]))
            #The old C0 should become the new one (C0 become C1, then C2 but this is easier to write)
            oldC0 = newC0
        #Once T-cycles are done, return it
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
    #Create array for each test case
    inputArray = []
    for index in range(len(lines)):
        if index != 0:
            #Create array for the variables of the test case
            newInput = []
            split1 = lines[index].split(",",1)
            #Get K out of line
            k = int(split1[0])
            split2 = split1[1].split(",",1)
            #Get the rule number out of the line
            rule = int(split2[0])
            split3 = split2[1].split(",",1)
            #Get the T out of the line
            T = int(split3[0])
            #Get the CT out of the line
            CT = split3[1]
            CTArray = []
            #Trim the brackets of it
            CTSplit = CT.split("[")[1]
            CTSplit = CTSplit.split("]")[0]
            #Delimit this trimmed CT on a comma
            CTSplit = CTSplit.split(",")
            #Convert this list with strings to a list with integers
            for number in CTSplit:
                CTArray.append(int(number))
            #Append all these variables to the test case
            newInput.append(k)
            newInput.append(rule)
            newInput.append(T)
            newInput.append(CTArray)
            #finally append this test case to the list of test cases
            inputArray.append(newInput)
    
    #Creates an instance of cellularAutomata with the rule number as its parameter
    cellularAutomata = CellularAutomata(inputArray[5][1])
    #Print the CT of a test case
    print(inputArray[6][3])
    
    #Run the CT, T times through the rule
    #!!!!!!!!!!!!!!!!NOTE!!!!!!!!!!!!!!!!!!!!
    #CT should never be run through the rule, because CT is the endpoint of C0 after T times
    #However, this is useful for demonstration and testing purposes
    print(cellularAutomata(inputArray[6][3], inputArray[6][2]))
    #                     CT of test case 6, T of test case 6
    
    
    
