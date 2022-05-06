"""
Bio-inspired Artificial Intelligence (BAI)
Prof. Dario Floreano

Genetic Algorithms Laboratory
Exercise 5

Converted to Python by Joshua Auerbach
"""

from pylab import figure, ioff, show
from random import Random
from ga import run_ga
from inspyred import benchmarks
import sys

args = {}


"""   
-------------------------------------------------------------------------
Edit this part to do the exercises
"""

# parameters for the GA
args["num_vars"] = 1 # Number of dimensions of the search space
args["gaussian_stdev"] = 1.0 # Standard deviation of the Gaussian mutations
args["crossover_rate"]  = 0.8 # Crossover fraction
args["tournament_size"] = 2 
args["pop_size"] = 10 # population size

args["num_elites"] = 1 # number of elite individuals to maintain in each gen
args["mutation_rate"] = 0.5 # fraction of loci to perform mutation on


# by default will use the problem's defined init_range
# uncomment the following line to use a specific range instead
#args["pop_init_range"] = [-500, 500] # Range for the initial population

args["use_bounder"] = True # use the problem's bounder to restrict values
# comment out the previously line to run unbounded

args["max_generations"] = 100 # Number of generations of the GA
display = True # Plot initial and final populations

problem_class = benchmarks.Sphere

# other problems to try, 
# see  https://pythonhosted.org/inspyred/reference.html#module-inspyred.benchmarks

# unimodal 
#problem_class = benchmarks.Rosenbrock

# multimodal 
#problem_class = benchmarks.Griewank
#problem_class = benchmarks.Ackley
#problem_class = benchmarks.Rastrigin
#problem_class = benchmarks.Schwefel

"""
-------------------------------------------------------------------------
"""



if __name__ == "__main__":
    if len(sys.argv) > 1 :
        rng = Random(int(sys.argv[1]))
    else :
        rng = Random()
        
    best_individual, best_fitness = run_ga(rng, display=display,
                                           problem_class=problem_class,**args)
    print("Best Individual", best_individual)
    print("Best Fitness", best_fitness)
    
    if display :
        ioff()
        show()
