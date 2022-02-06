import functions
import pso
import sgd


if __name__ == "__main__":

    # Initialise PSO parameter

    # Number of Particles
    particle_number = 100

    # Dimensions for each particle
    dimensions = 2

    # Objective Function and the parameters it takes
    # function = [functions.rosenbrock, [0, 10]]
    function = [functions.rastrigin, [10]]

    # Parameters a,b,c for PSO (a = inertia weight, b,c learning constants for particle best position and global best position)
    a = 0.5  # = 0 No influence from the previous velocity, = 1 full influence of the previous velocity
    b = 2  # = 0 No influence from the personal best position, = 1 full influence of the personal best position
    c = 2  # = 0 No influence from the global best position, = 1 full influence of the global best position

    # Initialise/Activate a parameter adjustment
    # For each index(0=a,1=b,2=c) ->
    # (subindex 0 -> value=0 activates adjustment, value=1 increases parameter, value=2 decreases parameter)
    # (subindex 1 -> Adjustment  application rate - after how many epochs)
    # (subindex 2 -> Adjustment rate - amount of reduction/increase)
    # (subindex 3 -> stop value)
    dynamic_parameter_adjustment = [
        [2, 9, 0.1, 0.1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    # Range for the randomisation of starting positions of particles
    # Try a difference of 1000 or more to spread them really apart / try placeing them away from 0 which is a global min for both objective functions that are being measured by default
    # boundary = [-100, 100]
    boundary = [-8000, -4000]

    # Neighbourhood range and adjustment.
    # First parameter activates/deactivates neighbourhood topology
    # Second parameter initialises the visibility range for each particle
    # Third parameter activates/deactivates visibility increase
    # Fourth parameter sets the application rate - after how many epochs
    # Fifth parameter sets the amount of increase
    # Sixth parameter activates/deactivates neighbourhood switch to global
    # Seventh parameter sets the threshold over which the neighbourhood becomes global
    neighbourhood_options = [True, 250, True, 9, 500, True, 50]

    # Limit for the randomisation of starting velocities of particles [(]-start_velocity_limit,+start_velocity_limit]
    start_velocity_limit = 1

    # Limit for min/max velocity a particle can have. Clipping occurs if it ends up outside the threshold [-velocity_limit,+velocity_limit]
    velocity_limit = 10000000

    # Limit the space the particles can occupy. (x,y : [-space_limit,+space_limit]
    space_limit = 10000  # For Rastrigin [-10000,10000] for x,y

    # Number of PSO iterations
    iterations = 100

    # Plot Range
    plot_range = [[-10000, 10000], [-10000, 10000]]  # Better for Rastrigin
    # plot_range = [[-2, 2], [-1, 3]]  # Better for Rosenbrock

    # Run PSO
    pso.PSO(particle_number, dimensions, function,
            a, b, c, dynamic_parameter_adjustment, boundary, neighbourhood_options, start_velocity_limit, velocity_limit, space_limit, iterations, plot_range)

    # sgd.sgd(function[1], func_name="rosenbrock", iterations=50, lr=0.001)
