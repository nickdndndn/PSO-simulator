import functions
import pso


if __name__ == "__main__":

    # Initialise PSO parameter

    # Number of Particles
    particle_number = 100

    # Dimensions for each particle
    dimensions = 2

    # Objective Function and the parameters it takes
    # function = fn.rosenbrock  # fn.rastrigin for Rastrigin
    function = functions.rastrigin  # fn.rastrigin for Rastrigin

    # Rosenbrock takes 2 parameters. Rastrigin takes 1 (e.g [2])
    # function_parameters = [0, 10]
    function_parameters = [2]

    # Parameters a,b,c for PSO (a = inertia weight, b,c learning constants for particle best position and global best position)
    a = 0.5  # = 0 No influence from the previous velocity, = 1 full influence of the previous velocity
    b = 2  # = 0 No influence from the personal best position, = 1 full influence of the personal best position
    c = 2  # = 0 No influence from the global best position, = 1 full influence of the global best position

    # Limit for the randomisation of starting positions of particles [(]-boundary,+boundary]
    # boundary = 1  # Try 500 to spread them really apart
    boundary = 500  # Try 500 to spread them really apart

    # Limit for the randomisation of starting velocities of particles [(]-start_velocity_limit,+start_velocity_limit]
    start_velocity_limit = 1

    # Limit for min/max velocity a particle can have. Clipping occurs if it ends up outside the threshold [-velocity_limit,+velocity_limit]
    velocity_limit = 10000000

    # Number of PSO iterations
    iterations = 100

    # Run PSO
    pso.PSO(particle_number, dimensions, function, function_parameters,
            a, b, c, boundary, start_velocity_limit, velocity_limit, iterations)
