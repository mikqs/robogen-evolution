"""
Bio-inspired Artificial Intelligence (BAI)
Prof. Dario Floreano

Genetic Algorithms Laboratory

ga module
Written  by Joshua Auerbach
"""


from pylab import *
import plot_utils
from inspyred import ec, benchmarks
from ann_benchmarks import NeuralNetworkBenchmark
from threading import Thread

def generate_offspring(random, x0, std_dev, num_offspring, display) :
    
    
    x0 = asarray(x0, dtype=float64)
    
    problem = benchmarks.Sphere(len(x0))
    
    parent_fitness = problem.evaluator([x0], None)[0]

    algorithm = ec.EvolutionaryComputation(random)
    algorithm.terminator = ec.terminators.generation_termination
    algorithm.replacer = ec.replacers.generational_replacement    
    algorithm.variator = ec.variators.gaussian_mutation
    
    final_pop = algorithm.evolve(generator=(lambda random, args: x0.copy()),
                          evaluator=problem.evaluator,
                          pop_size=num_offspring,
                          maximize=False,
                          max_generations=1,
                          mutation_rate=1.0,
                          gaussian_stdev=std_dev)
    
    offspring_fitnesses = asarray([guy.fitness for guy in final_pop])
    offspring = asarray([guy.candidate for guy in final_pop])
    
    if display :        
        # Plot the parent and the offspring on the fitness landscape 
        # (only for 1D or 2D functions)
        if len(x0) == 1 :
            plot_utils.plot_results_1D(problem, x0, parent_fitness, offspring, 
                                  offspring_fitnesses, 'Parent', 'Offspring')
    
        elif len(x0) == 2 :
            plot_utils.plot_results_2D(problem, asarray([x0]), offspring,
                                  'Parent', 'Offspring')
            
            
    
    return (parent_fitness, offspring_fitnesses)

def generator(random, args):
    return asarray([random.uniform(args["pop_init_range"][0],
                                   args["pop_init_range"][1]) 
                    for _ in range(args["num_vars"])])

def initial_pop_observer(population, num_generations, num_evaluations, 
                         args):
    if num_generations == 0 :
        args["initial_pop_storage"]["individuals"] = asarray([guy.candidate 
                                                 for guy in population]) 
        args["initial_pop_storage"]["fitnesses"] = asarray([guy.fitness 
                                          for guy in population]) 

def run_ga(random,display=False, num_vars=0, problem_class=benchmarks.Sphere, 
           maximize=False, use_bounder=False, **kwargs) :
    
    #create dictionaries to store data about initial population, and lines
    initial_pop_storage = {}
 
    
    algorithm = ec.EvolutionaryComputation(random)
    algorithm.terminator = ec.terminators.generation_termination
    algorithm.replacer = ec.replacers.generational_replacement    
    algorithm.variator = [ec.variators.uniform_crossover, 
                          ec.variators.gaussian_mutation]
    algorithm.selector = ec.selectors.tournament_selection
    if display :
        # don't like inspyred's plot observer, so use our custom one
        algorithm.observer = [plot_utils.plotting_observer,initial_pop_observer]
        animator = plot_utils.Animator()
    else :
        algorithm.observer = initial_pop_observer 
        animator = None
    
    kwargs["num_selected"]=kwargs["pop_size"]  
    
    # special stuff for ANN Benchmarks    
    if issubclass(problem_class, NeuralNetworkBenchmark) :
        if "num_hidden_units" not in kwargs :
            kwargs["num_hidden_units"] = 0
        if "recurrent" not in kwargs :
            kwargs["recurrent"] = False
        problem = problem_class(kwargs["num_hidden_units"], kwargs["recurrent"])
        num_vars = problem.dimensions
    else :
        problem = problem_class(num_vars)
        
        
    if use_bounder :
        kwargs["bounder"]=problem.bounder
    if "pop_init_range" in kwargs :
        kwargs["generator"]=generator
    else :
        kwargs["generator"]=problem.generator

    # Create a secondary thread for evolution. The main thread triggers rendering by calling pause.
    final_pop = []
    Thread(target=(lambda : final_pop.extend(algorithm.evolve(evaluator=problem.evaluator,
                            maximize=problem.maximize,
                            initial_pop_storage=initial_pop_storage,
                            num_vars=num_vars, animator=animator,
                            **kwargs))), daemon=True).start()
    while len(final_pop) == 0:
        pause(1)

    best_guy = final_pop[0].candidate
    best_fitness = final_pop[0].fitness
    final_pop_fitnesses = asarray([guy.fitness for guy in final_pop])
    final_pop = asarray([guy.candidate for guy in final_pop])
    
    
    if display : 
        animator.stop()
        # Plot the parent and the offspring on the fitness landscape 
        # (only for 1D or 2D functions)
        if num_vars == 1 :
            plot_utils.plot_results_1D(problem, initial_pop_storage["individuals"], 
                                  initial_pop_storage["fitnesses"], 
                                  final_pop, final_pop_fitnesses,
                                  'Initial Population', 'Final Population')
    
        elif num_vars == 2 :
            plot_utils.plot_results_2D(problem, initial_pop_storage["individuals"], 
                                  final_pop, 'Initial Population', 
                                  'Final Population')
    
    return best_guy, best_fitness

