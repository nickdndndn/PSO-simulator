import os

import imageio
import numpy as np
import main
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

class PSO:
    def __init__(self, N):
        #init population of N parameters
        self.particles = [Particle((np.random.uniform(-4, 4),np.random.uniform(-4, 4)), (np.random.uniform(-1, 1),np.random.uniform(-1, 1))) for i in range(N)]
        self.gbest = self.particles[np.array([particle.pbest_obj for particle in self.particles]).argmin()].pbest
        self.gbest_obj = min(np.array([particle.pbest_obj for particle in self.particles]))
        return

    def train(self, c1, c2, w, MaxIter):
        filenames= []


        for index in range(MaxIter):
            for i in range(len(self.particles)):
                r1, r2 = np.random.random_sample(2)
                ''' if i ==1 :
                                    print('pos', self.particles[i].pos)
                                    print('vel', self.particles[i].vel)
                                    print('pbest', self.particles[i].pbest)
                                    print('bbest_g', self.particles[i].pbest_obj)
                                    print('g', main.rosenbrock(self.particles[i].pos[0], self.particles[i].pos[1]))
                                    print('gbest', self.gbest)
                                    print('gbest_obj', self.gbest_obj)'''

                self.particles[i].vel = w * self.particles[i].vel + c1 * r1 * (
                            self.particles[i].pbest - self.particles[i].pos) * c2 * r2 * (
                                                        self.gbest - self.particles[i].pos)
                self.particles[i].pos = self.particles[i].pos + self.particles[i].vel
                obj = main.rosenbrock(self.particles[i].pos[0], self.particles[i].pos[1])

                #print(obj, self.particles[i].pbest_obj)
                if (np.less(obj,self.particles[i].pbest_obj)):
                    #print('true')
                    self.particles[i].pbest_obj = obj
                    self.particles[i].pbest = self.particles[i].pos
                    if (np.less(obj, self.gbest_obj)):
                        self.gbest_obj = obj
                        self.gbest = self.particles[i].pos



            xlist = np.linspace(-4., 4., 100)
            ylist = np.linspace(-4., 4., 100)
            X, Y = np.meshgrid(xlist, ylist)
            Z = main.rosenbrock(X, Y)
            fig, ax = plt.subplots(1, 1)
            cp = ax.contour(X, Y, Z, 100)
            fig.colorbar(cp)
            ax.set_title('Rosenbrock space')
            ax.set_xlabel('Longtitude')
            ax.set_ylabel('Langtitude')
            ax.set_xlim([-4, 4])
            ax.set_ylim([-4, 4])
            plt.scatter([particle.pos[0] for particle in self.particles], [particle.pos[1] for particle in self.particles], marker='o', color='red')

            #plt.plot()
            #plt.show()
            filename = f'images/Epoch_{index}_.png'
            filenames.append(filename)

            # save img
            plt.savefig(filename, dpi=96)
            plt.close()

        # Build GIF
        print('creating gif\n')
        with imageio.get_writer('mygif.gif', mode='I') as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)
        print('gif complete\n')
        print('Removing Images\n')
        # Remove files
        for filename in set(filenames):
            os.remove(filename)

        return




    def plot(self):
        # save plots somehow
        pass

    def predict(self):
        #will we need this? probably not
        pass


class Particle:
    def __init__(self,pos, vel):
        self.pos = np.array(pos)
        self.vel = np.array(vel) * 0.1
        self.pbest = pos
        self.pbest_obj = main.rosenbrock(pos[0],pos[1])
        # particle position, velocity
        # best position & error (individual)
        return

    def evaluate(self):
        # check if current position is best
        pass

    def next(self):
        # compute next position
        # next velocity
        pass

