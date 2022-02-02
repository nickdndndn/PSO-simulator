from matplotlib import pyplot as plt
from pso import PSO, Particle

import numpy as np

def rosenbrock(x,y):
    a  = 0
    b = 0
    return (a - x) ** 2 + b(y-x**2)**2

def rastrigin(x):
    n = 0 
    return 10 * n + (x**2 - 10 * np.cos(2*np.pi *x))

