import typing
import ioh


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
    
    ct, rule, t = [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 34, 5

    ca = CellularAutomata(rule)
    ct_prime = ca(c0_prime, t)

    positives, negatives = 0, 0
    for bit in range(0, len(str(ct))):
        if (str(ct)[bit] == str(ct_prime)[bit]):
            positives += 1
        else:
            negatives += 1

    similarity = (positives / (negatives + positives)) * 100

    return similarity

def objective_function2(c0_prime: typing.List[int]) -> float:
    '''Skeleton objective function. You should implement a method
    which computes a similarity measure between c0_prime a suggested by your
    GA, with the true c0 state for the ct state given in the sup. material. '''
    
    ct, rule, t = [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 34, 5

    ca = CellularAutomata(rule)
    ct_prime = ca(c0_prime, t)

    #this objective function also takes in account how close both bits are
    #1-2 is closer than 0-2
    c0Str = str(ct)
    ctStr = str(ct_prime)
    length = len(c0Str)
    totalDiff = 0
    for bit in range(0, length):
        totalDiff += (2-abs(int(c0Str[bit])-int(ctStr[bit])))*0.5

    #return similarity percentage
    return totalDiff / length * 100