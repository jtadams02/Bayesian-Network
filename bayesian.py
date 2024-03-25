from collections import defaultdict, Counter
import itertools
import math
import random

# I do not know what the object tag is, however we are going to use it
# Figured it out, it designates the class as an object, therefore it will inherit all properties of an object
class BayesNet(object):

    def __init__(self) -> None:
        # Create graph
        self.variables = [] # List of variables, in parent-frist topolgical sort order, whatever that means
        self.lookup = {} # This maps variable_name: variable pairs I think

    #Names are strings, and each of the parent names needs to have already been added to the Network?
    def add(self,name,parent_names,cpt):
        parents = [self.lookup[name] for name in parent_names] # Variables that match teh parent names?
        var = Variable(name,cpt,parent_names)
        self.variables.append(var)
        self.lookup[name] = var
        return self

class Variable(object):

    # A variable has a name, a list of parent variables, and a conditional probibility table (THATS WHAT CPT IS!!!)
    def __init__(self,name,cpt,parents=()) -> None:
        self.__name__ = name # Why does the github use __  ? 
        self.parents = parents # Makes senses, sets the variable's parents
        self.cpt = CPTable(cpt,parents) # Assigns a CPT to this variable
        self.domain = set(itertools.chain(*self.cpt.values())) # "All the outcomes in the CPT" TODO: Figure out what this does

    def __repr__(self): return self.__name__

# So dict here signals that "Factor" is an object of dict? right?
class Factor(dict): "An {outcome: frequency} mapping."

# ProbDist inherits the properties of Factor, which inherits the properties of a dict
class ProbDist(Factor):
    """A Probability Distribution is an {outcome: probability} mapping. 
    The values are normalized to sum to 1.
    ProbDist(0.75) is an abbreviation for ProbDist({T: 0.75, F: 0.25})."""
    def __init__(self, mapping=(), **kwargs):
        if isinstance(mapping,float):
            mapping = {T: mapping, F: 1 - mapping} # Macros
        self.update(mapping, **kwargs)
        normalize(self) # WHAT DOES THIS DO

# Okay whats this purpose?
class Evidence(dict): 
    "A {variable: value} mapping, describing what we know for sure."

class CPTable(dict):
    "A mapping of {row: ProbDist, ...} where each row is a tuple of values of the parent variables."
    
    def __init__(self, mapping, parents=()):
        """Provides two shortcuts for writing a Conditional Probability Table. 
        With no parents, CPTable(dist) means CPTable({(): dist}).
        With one parent, CPTable({val: dist,...}) means CPTable({(val,): dist,...})."""
        if len(parents) == 0 and not (isinstance(mapping, dict) and set(mapping.keys()) == {()}):
            mapping = {(): mapping}
        for (row, dist) in mapping.items():
            if len(parents) == 1 and not isinstance(row, tuple): 
                row = (row,)
            self[row] = ProbDist(dist)

class Bool(int):
    "Just like `bool`, except values display as 'T' and 'F' instead of 'True' and 'False'"
    __str__ = __repr__ = lambda self: 'T' if self else 'F'

# These are kinda like macros i guess
T = Bool(True)
F = Bool(False)


def P(var, evidence={}):
    "The probability distribution for P(variable | evidence), when all parent variables are known (in evidence)."
    row = tuple(evidence[parent] for parent in var.parents)
    return var.cpt[row]

def normalize(dist):
    "Normalize a {key: value} distribution so values sum to 1.0. Mutates dist and returns it."
    total = sum(dist.values())
    for key in dist:
        dist[key] = dist[key] / total
        assert 0 <= dist[key] <= 1, "Probabilities must be between 0 and 1."
    return dist

def sample(probdist):
    "Randomly sample an outcome from a probability distribution."
    r = random.random() # r is a random point in the probability distribution
    c = 0.0             # c is the cumulative probability of outcomes seen so far
    for outcome in probdist:
        c += probdist[outcome]
        if r <= c:
            return outcome
        
def globalize(mapping):
    "Given a {name: value} mapping, export all the names to the `globals()` namespace."
    globals().update(mapping)

# Add in Joint Probability Distributions 
def joint_distribution(net):
    "Given a Bayes net, create the joint distribution over all variables."
    return ProbDist({row: prod(P_xi_given_parents(var, row, net)
                               for var in net.variables)
                     for row in all_rows(net)})

def all_rows(net): return itertools.product(*[var.domain for var in net.variables])

def P_xi_given_parents(var, row, net):
    "The probability that var = xi, given the values in this row."
    dist = P(var, Evidence(zip(net.variables, row)))
    xi = row[net.variables.index(var)]
    return dist[xi]

def prod(numbers):
    "The product of numbers: prod([2, 3, 5]) == 30. Analogous to `sum([2, 3, 5]) == 10`."
    result = 1
    for x in numbers:
        result *= x
    return result

def parseInput(inp):
    variables = inp.split(",")
    
    # Now handle each variable one by one
    mapping = {}
    for v in variables:
        n,val  = v.split("=")
        


battery = starts = gas = moves = radio = F # Set all variables equal to false

query = input("query: ")
# Handle the input 
parseInput(query)