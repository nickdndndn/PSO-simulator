from matplotlib import pyplot as plt
from pso import *
import numpy as np

def rosenbrock(x,y):
    a = 0
    b = 10
    return np.add(np.square(np.subtract(a,x)),np.square(np.multiply(b,(y-np.square(x)))))

def rastrigin(x,y):
    n = 0 
    return 10 * n + (x**2 - 10 * np.cos(2*np.pi * x)) #np.sum might be needed here


if __name__ == '__main__':
    #np.random.seed(2)

    #Hyparameters
    N = 10
    c1 = 2
    c2 = 2
    w = 0.5
    MaxIter = 20

    #initialize algorithm
    ps = PSO(N)
    ps.train(c1, c2, w, MaxIter)


# plot
'''
    xlist = np.linspace(-2., 2., 100)
    ylist = np.linspace(-1., 3., 100)
    X, Y = np.meshgrid(xlist, ylist)
    Z = main.rosenbrock(X, Y)
    fig, ax = plt.subplots(1, 1)
    cp = ax.contour(X, Y, Z, 100)
    fig.colorbar(cp)
    ax.set_title('Rosenbrock space')
    ax.set_xlabel('Longtitude')
    ax.set_ylabel('Langtitude')
    for particle in ps.particles:
        plt.scatter(particle.pos[0], particle.pos[1], marker='o', color='red')
    plt.show()

'''