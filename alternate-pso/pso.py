import random
import plot

# Class for the particles


class Particle():

    def __init__(self, start_pos_vec, start_vlimit):

        # Variables for  starting position/velocity, best position/velocity, error/best error
        self.particle_pos = []
        self.particle_vel = []
        self.particle_bestPos = []
        self.particle_err = -1
        self.particle_bestErr = -1

        # Initialise Starting position/velocity from parameters for each dimension
        for i in range(len(start_pos_vec)):
            self.particle_pos.append(start_pos_vec[i])
            # Set a random starting velocity that's within the parameter limits
            self.particle_vel.append(
                random.uniform(-start_vlimit, start_vlimit))

    # Evaluates the error of the function at the current position of the particle - essentially the distance from 0 since this is an optimisation problem
    def evaluate(self, function, parameters):

        # Returns the calculation of the function at the current position of the particle
        self.particle_err = function(self.particle_pos, parameters)

        # Check if the error at the current position is less than the particle best. If yes, update the particle best position and error
        if self.particle_err < self.particle_bestErr or self.particle_bestErr == -1:
            self.particle_bestErr = self.particle_err
            self.particle_bestPos = list(self.particle_pos)

    # Updates the velocity and position of the particle
    def update(self, a, b, c, global_bestPos, vlimits):

        # Update each dimension
        for i in range(len(self.particle_pos)):

            # Retrieve the random variable component of the PSO function
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)

            # PSO function
            self.particle_vel[i] = a * self.particle_vel[i] + b * r1 * \
                (self.particle_bestPos[i] -
                 self.particle_pos[i]) + c * r2 * (global_bestPos[i] - self.particle_pos[i])

            # Clip velocity if it lies outside the thresholds
            if self.particle_vel[i] < -vlimits:
                self.particle_vel[i] = -vlimits
            elif self.particle_vel[i] > vlimits:
                self.particle_vel[i] = vlimits

        # Update position of each dimension
        for i in range(len(self.particle_pos)):
            self.particle_pos[i] = self.particle_pos[i] + self.particle_vel[i]

# Class that runs the main algorithm


class PSO():

    # Parameters are : Number of Particles, Dimensions of the function, The function itself and its parameters, The PSO parameters, Velocity limits and the Iteration number
    def __init__(self, particle_number, dimensions, function, function_parameters, a, b, c, boundary,  start_vlimit, vlimits, max_iter):

        # Set Variable to keep the filenames of each plotted graph
        filenames = []

        # Variables for the global best position and the global best(lowest) error
        self.global_bestPos = []
        self.global_bestErr = -1

        # Initialise particles
        swarm = []
        for i in range(particle_number):
            start_pos_vec = []
            # Randomise initial particle position of each of its dimensions within the parameter limit
            for j in range(dimensions):
                start_pos_vec.append(random.uniform(-boundary, boundary))
            # Add the created particle to the eternal will of the swarm
            swarm.append(Particle(start_pos_vec, start_vlimit))

        # Iterate through the epochs.
        # For each iteration : 1. Evaluate each particle 2.Update Global best position / best error 3. Update Particle position / velocities (optional) 4. Plot a graph
        i = 0
        while i < max_iter:

            # Evaluate each particle
            for k in range(len(swarm)):
                swarm[k].evaluate(function, function_parameters)

                # Update global best position / error if a better one is found
                if swarm[k].particle_bestErr < self.global_bestErr or self.global_bestErr == -1:
                    self.global_bestErr = swarm[k].particle_bestErr
                    self.global_bestPos = list(swarm[k].particle_pos)

            # Update each particle
            for m in range(len(swarm)):
                swarm[m].update(a, b, c, self.global_bestPos, vlimits)

            # Plot a graph and append the filename of the gunpoweder, treason and plot created
            filenames.append(plot.plotGraphs(
                swarm, function, function_parameters, i))

            # Continue
            i += 1

        # Create a Gif from all the graphs plotted
        plot.createGif(filenames)
