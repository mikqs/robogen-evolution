"""
Bio-inspired Artificial Intelligence (BAI)
Prof. Dario Floreano

Genetic Algorithms Laboratory
Exercise 4

Converted to Python by Joshua Auerbach
"""

from pylab import asarray, figure, show
from random import Random
from ga import run_ga
from inspyred import benchmarks
import sys

"""   
-------------------------------------------------------------------------
Edit this part to do the exercises
"""

tournament_sizes = [2, 10]

# choose problem
problem_class = benchmarks.Sphere
# problem_class = benchmarks.Rastrigin

"""
Questions:
 * Which tournament size gives better results for the fitness function sphere and why?
 * Which tournament size is better for the fitness function Rastrigin 6 and why?
-------------------------------------------------------------------------
"""

# parameters for the GA
args = {}
args["num_vars"] = 10 # Number of dimensions of the search space
args["gaussian_stdev"] = 0.2 # Standard deviation of the Gaussian mutations
args["crossover_rate"]  = 0.0 # Crossover fraction
args["mutation_rate"] = 1.0 # fraction of loci to perform mutation on
args["num_elites"] = 1 # number of elite individuals to maintain in each gen
args["pop_size"] = 25 # population size
args["pop_init_range"] = [-10, 10] # Range for the initial population
args["max_generations"] = 50 # Number of generations of the GA

num_runs = 30 # Number of runs to be done for each condition
display = False # Plot initial and final populations



if __name__ == "__main__":
    if len(sys.argv) > 1 :
        rng = Random(int(sys.argv[1]))
    else :
        rng = Random()
    
    # run the GA *num_runs* times for each crossover fraction 
    # and record results 
    results = asarray([[run_ga(rng, problem_class=problem_class,
                              display=display, 
                              tournament_size=tournament_size,**args)
                       for _ in range(num_runs)]
                      for tournament_size in tournament_sizes])

    best_fitnesses = [[run_result[1] for run_result in runs] 
                      for runs in results]
    distance_from_global_optimums = [[sum(asarray(run_result[0]) ** 2) 
                                      for run_result in runs] 
                      for runs in results]
    
    fig = figure()
    # Boxplot comparing the distance from the global optimum
    ax = fig.add_subplot(2,1,1)
    ax.boxplot(distance_from_global_optimums, labels=tournament_sizes)
    ax.set_xlabel('Tournament sizes')
    ax.set_ylabel('Distance from optimum')
    
    # Boxplot comparing the best fitnesses
    ax = fig.add_subplot(2,1,2)
    ax.boxplot(best_fitnesses, labels=tournament_sizes)
    ax.set_xlabel('Tournament sizes')
    ax.set_ylabel('Fitness')
    show()








  


  

