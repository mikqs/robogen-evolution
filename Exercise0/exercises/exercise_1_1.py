"""
Bio-inspired Artificial Intelligence (BAI)
Prof. Dario Floreano

Genetic Algorithms Laboratory
Exercise 1.1

Converted to Python by Joshua Auerbach
"""

from pylab import figure, show, ones
from ga import generate_offspring
from random import Random
import sys

"""
-------------------------------------------------------------------------
Edit this part to do the exercises

Choose the parent x0 that will be mutated. It can have an arbitrary 
number of dimensions, but plotting of the fitness landscape is only 
possible for the 1D or 2D case.
"""

# Set the parent x0. Try different values and dimensions. Here are some examples:
x0 = [10]               # 1 dimension
# x0 = [10, 10]          # 2 dimension
# x0 = 10*ones(100);      # 50 dimensions

# Set the standard deviation of the Gaussian mutations. Try different values.
std_dev = 1

# Set number of offspring to be generated.
num_offspring = 25

"""
Questions:
 * Do the mutations tend to improve or worsen the fitness of the parent?
 * Are low or high mutation magnitudes best for improving the finess? How
 does this depend on the initial value of the parent and on the number of
 dimensions of the search space?
-------------------------------------------------------------------------
"""

if __name__ == "__main__":
    if len(sys.argv) > 1 :
        rng = Random(int(sys.argv[1]))
    else :
        rng = Random()
    plot_fitness_landscape = True # Set to False to disable the plots
    parent_fitness, offspring_fitnesses = generate_offspring(rng, x0, std_dev, 
                                                    num_offspring, 
                                                    plot_fitness_landscape)
    
    """
    Boxplot of the offspring fitnesses. The fitness of the parent is plotted as
    a dashed, green line.
    """
    fig = figure()
    ax = fig.gca()
    ax.boxplot(offspring_fitnesses)
    ax.plot([0,2], [parent_fitness,parent_fitness], 'g--', label='Parent fitness')
    ax.set_ylabel('Fitness')
    ax.set_ylim(ymin=0)
    ax.set_title('Fitness of the offsprings')
    ax.legend(loc='best')
    show()
