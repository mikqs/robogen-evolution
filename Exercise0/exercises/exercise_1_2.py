"""
Bio-inspired Artificial Intelligence (BAI)
Prof. Dario Floreano

Genetic Algorithms Laboratory
Exercise 1.2

Converted to Python by Joshua Auerbach
"""

from ga import generate_offspring
from pylab import figure, show, ones
from random import Random
import sys

""" 
-------------------------------------------------------------------------
Edit this part to do the exercises

Try different values for either:
    (1) the number of dimensions of the search space
    (2) how close the parent is to the global optimum
    (3) the mutation rate
 If you vary one of the three things, you may want to keep the other two
 at a constant value to better understand the effects (as shown in the
 example below).
"""

# (1) Vary the number of dimensions of the search space
num_vars_1 = 1
num_vars_2 = 10
num_vars_3 = 100

# (2) Vary how close the parent is to the optimum
value_1 = 1
value_2 = 1
value_3 = 1

# The parents are created for the three conditions
x0_1 = value_1*ones(num_vars_1)
x0_2 = value_2*ones(num_vars_2)
x0_3 = value_3*ones(num_vars_3)

# (3) Vary the standard deviation of the Gaussian mutations
std_dev_1 = 1
std_dev_2 = 1
std_dev_3 = 1

# Number of offspring to be generated
num_offspring = 200

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
    
    # Generate offspring for the three conditions
    parent_fitness_1, offspring_fitness_1 = generate_offspring(rng, x0_1, 
                                                               std_dev_1, 
                                                               num_offspring, 
                                                               False)
    parent_fitness_2, offspring_fitness_2 = generate_offspring(rng, x0_2, 
                                                               std_dev_2, 
                                                               num_offspring, 
                                                               False)
    parent_fitness_3, offspring_fitness_3 = generate_offspring(rng, x0_3,
                                                               std_dev_3, 
                                                               num_offspring, 
                                                               False)

    """
    Boxplot of the offspring fitnesses. The fitness of the parent is plotted as
    a dashed, green line.
    """
    fig = figure()
    ax = fig.gca()
    ax.boxplot([offspring_fitness_1, offspring_fitness_2, offspring_fitness_3])
    ax.plot([0.5, 1.5], [parent_fitness_1, parent_fitness_1], 'g--', label='Parent fitness')
    ax.plot([1.5, 2.5], [parent_fitness_2, parent_fitness_2], 'g--')
    ax.plot([2.5, 3.5], [parent_fitness_3, parent_fitness_3], 'g--')
    ax.set_ylabel('Fitness')
    ax.set_ylim(ymin=0)
    ax.set_title('Fitness of the offsprings for the three conditions')
    ax.legend(loc='best')
    show()
