import random
import plot

# Class for the particles


class Particle():

    def __init__(self, start_pos_vec, start_vlimit):

        # Variables for  starting position/velocity, best position/velocity, error/best error, neighbourhood best position/error
        self.particle_pos = []
        self.particle_vel = []
        self.particle_bestPos = []
        self.particle_err = -1
        self.particle_bestErr = -1
        self.neighbourhood_bestPos = []
        self.neighbourhood_bestErr = -1

        # Initialise Starting position/velocity from parameters for each dimension
        for i in range(len(start_pos_vec)):
            self.particle_pos.append(start_pos_vec[i])
            # Set a random starting velocity that's within the parameter limits
            self.particle_vel.append(
                random.uniform(-start_vlimit, start_vlimit))

    # Evaluates the error of the function at the current position of the particle - essentially the distance from 0 since this is an optimisation problem
    def evaluate(self, function):

        # Returns the calculation of the function at the current position of the particle
        self.particle_err = function[0](self.particle_pos, function[1])

        # Check if the error at the current position is less than the particle best. If yes, update the particle best position and error
        if self.particle_err < self.particle_bestErr or self.particle_bestErr == -1:
            self.particle_bestErr = self.particle_err
            self.particle_bestPos = list(self.particle_pos)

    # Neighbourhood evaluation
    def evaluate_neighbourhood(self, swarm, neighbourhood_range):

        # Find which particles lie within the visibility range
        for i in range(len(swarm)):
            if swarm[i].particle_pos[0] < self.particle_pos[0]+neighbourhood_range and swarm[i].particle_pos[0] > self.particle_pos[0]-neighbourhood_range and swarm[i].particle_pos[1] < self.particle_pos[1]+neighbourhood_range and swarm[i].particle_pos[1] > self.particle_pos[1]-neighbourhood_range:
                # For those that are, check whether their personal error is better than the neighbourhood error. If yes update current particle's neighbourhood error and position
                if swarm[i].particle_bestErr < self.neighbourhood_bestErr or self.neighbourhood_bestErr == -1:
                    self.neighbourhood_bestErr = swarm[i].particle_bestErr
                    self.neighbourhood_bestPos = list(
                        swarm[i].particle_bestPos)

    # Updates the velocity and position of the particle

    def update(self, a, b, c, global_bestPos, vlimits, neighbourhood_toggle, slimits):

        global_bestPos_update = []
        if neighbourhood_toggle == True:
            global_bestPos_update = list(self.neighbourhood_bestPos)
        else:
            global_bestPos_update = list(global_bestPos)

        # Update each dimension
        for i in range(len(self.particle_pos)):

            # Retrieve the random variable component of the PSO function
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)

            # PSO function
            self.particle_vel[i] = a * self.particle_vel[i] + b * r1 * \
                (self.particle_bestPos[i] -
                 self.particle_pos[i]) + c * r2 * (global_bestPos_update[i] - self.particle_pos[i])

            # Clip velocity if it lies outside the thresholds
            if self.particle_vel[i] < -vlimits:
                self.particle_vel[i] = -vlimits
            elif self.particle_vel[i] > vlimits:
                self.particle_vel[i] = vlimits

        # Update position of each dimension
        for i in range(len(self.particle_pos)):
            self.particle_pos[i] = self.particle_pos[i] + self.particle_vel[i]
            # Clip position if it lies outside the thresholds
            if self.particle_pos[i] > slimits:
                self.particle_pos[i] = slimits
            elif self.particle_pos[i] < -slimits:
                self.particle_pos[i] = -slimits

 # Class that runs the main algorithm


class PSO():

    # Parameters are : Number of Particles, Dimensions of the function, The function itself and its parameters, The PSO parameters, Velocity limits and the Iteration number
    def __init__(self, particle_number, dimensions, function, a, b, c, dynamic_parameter_adjustment, boundary, neighbourhood_options,  start_vlimit, vlimits, slimits, max_iter, plot_range):

        # Set Variable to keep the filenames of each plotted graph
        filenames_graph = []

        # Global error over epoch
        global_error_plot = [[], []]

        # Variables for the global best position and the global best(lowest) error
        self.global_bestPos = []
        self.global_bestErr = -1

        # Initialise particles
        swarm = []
        for i in range(particle_number):
            start_pos_vec = []
            # Randomise initial particle position of each of its dimensions within the parameter limit
            for j in range(dimensions):
                start_pos_vec.append(random.uniform(boundary[0], boundary[1]))
            # Add the created particle to the eternal will of the swarm
            swarm.append(Particle(start_pos_vec, start_vlimit))

        # Iterate through the epochs.
        # For each iteration : 1. Evaluate each particle 2.Update Global best position / best error 3. Update Particle position / velocities (optional) 4. Plot a graph
        i = 0
        while i < max_iter:

            # Evaluate each particle
            for k in range(len(swarm)):
                swarm[k].evaluate(function)

                # Update global best position / error if a better one is found
                if swarm[k].particle_bestErr < self.global_bestErr or self.global_bestErr == -1:
                    self.global_bestErr = swarm[k].particle_bestErr
                    self.global_bestPos = list(swarm[k].particle_pos)

            # Save global error for loss plot
            global_error_plot[0].append(i)
            global_error_plot[1].append(self.global_bestErr)

            # Check whether neighbourhood options are activated

            # Check if neighbourhood topology must switch to global topology
            if (neighbourhood_options[5] == True):
                if (i > neighbourhood_options[6]):
                    neighbourhood_options[0] = False
                    neighbourhood_options[2] = False

            # Calculate neighbourhood best position / error per particle (If activated)
            if neighbourhood_options[0] == True:
                for l in range(len(swarm)):
                    swarm[l].evaluate_neighbourhood(
                        swarm, neighbourhood_options[1])

            # Check if neighbourhood adjustment is activated and apply
            if (neighbourhood_options[2] == True):
                if (i % 10 == neighbourhood_options[3]):
                    neighbourhood_options[1] = neighbourhood_options[1] + \
                        neighbourhood_options[4]

            # Adjust PSO Parameters
            for idx_parameter in range(len(dynamic_parameter_adjustment)):
                if idx_parameter == 0:
                    # Adjust a
                    a = adjust_parameters(
                        a, dynamic_parameter_adjustment[idx_parameter], i)
                elif idx_parameter == 1:
                    # Adjust b
                    b = adjust_parameters(b,
                                          dynamic_parameter_adjustment[idx_parameter], i)
                elif idx_parameter == 2:
                    # Adjust c
                    c = adjust_parameters(c,
                                          dynamic_parameter_adjustment[idx_parameter], i)

            # Update each particle
            for m in range(len(swarm)):
                swarm[m].update(a, b, c, self.global_bestPos,
                                vlimits, neighbourhood_options[0], slimits)

            # Plot a graph and append the filename of the gunpowder, treason and plot created
            filenames_graph.append(plot.plotGraphs(
                swarm, function, i, plot_range))

            # Continue
            i += 1

        # Plot the loss graph in relation to the global error
        plot.plotLoss(global_error_plot)

        # Create a Gif from all the graphs plotted
        plot.createGif(filenames_graph)


def adjust_parameters(parameter, options, iteration):
    if (options[0] > 0):
        if (iteration % 10 == options[1]):
            if (options[0] == 1 and parameter < options[3]):
                parameter = parameter + \
                    options[2]
            elif (options[0] == 2 and parameter > options[3]):
                parameter = parameter - \
                    options[2]
    return parameter
