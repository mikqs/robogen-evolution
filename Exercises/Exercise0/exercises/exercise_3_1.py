"""
Bio-inspired Artificial Intelligence (BAI)
Prof. Dario Floreano

Genetic Algorithms Laboratory
Exercise 3.1

Converted to Python by Joshua Auerbach
"""

from pylab import figure, ioff, show
from random import Random
from ga import run_ga
import sys

# parameters for the GA
args = {}
args["num_vars"] = 2 # Number of dimensions of the search space
args["gaussian_stdev"] = 1.0 # Standard deviation of the Gaussian mutations
args["tournament_size"] = 2 
args["num_elites"] = 1 # number of elite individuals to maintain in each gen
args["pop_size"] = 20 # population size
args["pop_init_range"] = [-10, 10] # Range for the initial population
args["max_generations"] = 50 # Number of generations of the GA

num_runs = 30 # Number of runs to be done for each condition
display = False # Plot initial and final populations

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        rng = Random(int(sys.argv[1]))
    else :
        rng = Random()
    
    # Only mutation, no crossover
    crossover_rate = 0 # Crossover fraction    
    mutation_rate = 1.0 # fraction of loci to perform mutation on
    # run the GA *num_runs* times and record the best fits
    best_fitnesses_mutation_only = [run_ga(rng, display=display, 
                                           crossover_rate=crossover_rate,
                                           mutation_rate=mutation_rate,
                                           **args)[1]
                                    for _ in range(num_runs)]
    
    
    # Only crossover, no mutation
    crossover_rate = 1.0 # Crossover fraction  
    mutation_rate = 0.0 # fraction of loci to perform mutation on
    # run the GA *num_runs* times and record the best fits
    best_fitnesses_crossover_only = [run_ga(rng, display=display, 
                                           crossover_rate=crossover_rate,
                                           mutation_rate=mutation_rate,
                                           **args)[1]
                                    for _ in range(num_runs)]

    fig = figure()
    ax = fig.gca()
    ax.boxplot([best_fitnesses_mutation_only, best_fitnesses_crossover_only], labels=['Mutation only', 'Crossover only'])
    ax.set_yscale('log')
    ax.set_ylabel('Best fitness')
    ioff()
    show()
