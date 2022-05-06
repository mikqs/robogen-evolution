"""
Bio-inspired Artificial Intelligence (BAI)
Prof. Dario Floreano

Genetic Algorithms Laboratory

plot_utils module
Written  by Joshua Auerbach
"""


from pylab import *
from matplotlib.animation import FuncAnimation
from queue import Queue, Empty, Full
from itertools import chain
import sys

def plot_1D(axis, problem, x_limits) :
    dx = (x_limits[1] - x_limits[0])/200.0
    x = arange(x_limits[0], x_limits[1]+dx, dx)
    x = x.reshape(len(x),1)
    y = problem.evaluator(x, None)
    axis.plot(x,y,'-b')


def plot_2D(axis, problem, x_limits) :
    dx = (x_limits[1] - x_limits[0])/50.0
    x = arange(x_limits[0], x_limits[1]+dx, dx)
    z = asarray( [problem.evaluator([[i,j] for i in x], None) for j in x])
    return axis.contourf(x, x, z, 64, cmap=cm.hot_r)
    
def plot_results_1D(problem, individuals_1, fitnesses_1, 
                    individuals_2, fitnesses_2, title_1, title_2) :
    fig = figure()
    ax1 = fig.add_subplot(2,1,1)
    ax1.plot(individuals_1, fitnesses_1, '.b', markersize=7)
    lim = max(map(abs,ax1.get_xlim()))
            

    ax2 = fig.add_subplot(2,1,2)
    ax2.plot(individuals_2, fitnesses_2, '.b', markersize=7)
    lim = max(chain([lim], map(abs, ax2.get_xlim())))

    ax1.set_xlim(-lim, lim)
    ax2.set_xlim(-lim, lim)

    plot_1D(ax1, problem, [-lim, lim])
    plot_1D(ax2, problem, [-lim, lim])
    
    ax1.set_ylabel('Fitness')
    ax2.set_ylabel('Fitness')
    ax1.set_title(title_1)
    ax2.set_title(title_2)

def plot_results_2D(problem, individuals_1, individuals_2, 
                    title_1, title_2) :
    fig = figure()
    ax1 = fig.add_subplot(2,1,1, aspect='equal')
    ax1.plot(individuals_1[:,0], individuals_1[:,1], '.b', markersize=7)
    lim = max(chain(map(abs,ax1.get_xlim()), map(abs,ax1.get_ylim())))

    ax2 = fig.add_subplot(2,1,2, aspect='equal')

    ax2.plot(individuals_2[:,0], individuals_2[:,1], '.b', markersize=7)
    lim = max(chain([lim],
              map(abs,ax2.get_xlim()),
              map(abs,ax2.get_ylim())))

    ax1.set_xlim(-lim, lim)
    ax1.set_ylim(-lim, lim)
    ax1.set_title(title_1) 
    ax1.locator_params(nbins=5)
    
    ax2.set_xlim(-lim, lim)
    ax2.set_ylim(-lim, lim)
    ax2.set_title(title_2)    
    ax2.set_xlabel('x0')
    ax2.set_ylabel('x1')
    ax2.locator_params(nbins=5)
    
    plot_2D(ax1, problem, [-lim, lim])
    c = plot_2D(ax2, problem, [-lim, lim])
    fig.subplots_adjust(right=0.8)
    cax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    colorbar_ = colorbar(c, cax=cax)
    colorbar_.ax.set_ylabel('Fitness')

class Animator(object):
    def __init__(self):
        self.queue = Queue(256)
        self.stopped = False
        self.x_data, self.best_data, self.mean_data = [], [], []
        
        ion()
        self.fig = figure() 
        self.ax = self.fig.gca()
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Fitness value")
        self.line, = self.ax.plot([], [], '.r', ms=10)
        self.line2, = self.ax.plot([], [], '.b', ms=10)
        self.title = self.ax.set_title("")
        legend([self.line, self.line2], ["Best fitness", "Mean fitness"])
        
        self.animation = FuncAnimation(self.fig, self.update, self.data_gen,
                                       blit=(sys.platform != "darwin"),
                                       interval=1,repeat=False)
        draw()
        pause(0.00001)
    
    def stop(self):
        # Wait for animation to pop queue if queue is full
        while self.queue.full(): pause(0.1)
        # Signal animation to stop
        self.queue.put(None)
        # Wait for animation to stop
        while not self.stopped: pause(0.1)
        # Redraw actors
        self.ax.plot(self.x_data, self.best_data, '.r', ms=10)
        self.ax.plot(self.x_data, self.mean_data, '.b', ms=10)
        self.title.set_text("Best: %4.4e, Mean: %4.4e" % (self.best_data[-1], self.mean_data[-1]))
        self.fig.canvas.draw()
     
    def data_gen(self):
        while not self.stopped:
            if self.queue.empty() :
                yield None
            else :
                data = self.queue.get()
                if data is None:
                    self.stopped = True
                    raise StopIteration()
                yield data

    def update(self,data):
        if data is not None :      
            if len(data) is 2 :
                #scale figure
                (max_gens, mean_fit) = data
                self.ax.set_xlim(0, max_gens)
                self.ax.set_ylim(0, mean_fit)
                self.ax.figure.canvas.draw()  
                pause(0.01)
            else :          
                (gen,best,mean) = data
                self.x_data.append(gen)
                self.best_data.append(best)
                self.mean_data.append(mean)         
                self.line.set_data(self.x_data, self.best_data)
                self.line2.set_data(self.x_data, self.mean_data) 
                self.title.set_text("Best: %4.4e, Mean: %4.4e" % (best, mean))
        return (self.line, self.line2, self.title)
    


def plotting_observer(population, num_generations, num_evaluations, args):
    mean_fit = mean([guy.fitness for guy in population])
    if num_generations == 0 :  
        # put in data to scale figure
        args["animator"].queue.put((args["max_generations"], mean_fit))    
    args["animator"].queue.put((num_generations,population[0].fitness,mean_fit))
