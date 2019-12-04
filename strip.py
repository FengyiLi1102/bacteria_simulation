import numpy as np


def strip(N_size, d_size, L, increment):
    '''
    Describe:
    Given four parameters to generate different combinations between number of strips, width of coated region and width of uncoated
    region. Generate coated and uncoated strips with their y coordinates of vertices.


    Positional arguments:
    -> N_size:            the number of the coated strips (from 0 coated strips)
    -> d_size:            the number of d values for one simulation
    -> L:                 the dimension of the playground (square shape)
    -> increment:         the increasing rate of the strip width d
    
    
    Return:
    -> N_d_d2_y:          tuple with [0]: (N_size * d_size, 1) array with (N, d, d2)  <-- array 
                                     [1]: (N_size * d_size, 1) array with (y coordinates from 0 to 10)  <-- list
    '''

    # Create the combination of N and d.
    # Calculate the value of the d2 based on N*d + (N + 1)*d2 = L
    N_values = np.array([[i] for i in range(1, N_size + 1)])                       # Size of the N from 0 to N_size
    d_values = np.array([[increment * i] for i in range(1, d_size + 1)])        # increment * (d + 1) <= L

    N_d_d2_total = list()                # list containing arrays of different combinations of N, d and d2
    vertices_y_total = list()            # list containing lists of y coordinates of vertices of different combinations

    for value in N_values:

        N_d_d2 = np.zeros((d_size, 3))     # Set the dimension

        # Fixed N and changing d, obtaining different d2
        for index in range(d_values.shape[0]):

            N_d_d2[index][0] = value[0]
            N_d_d2[index][1] = d_values[index]
            N_d_d2[index][2] = (L - value * d_values[index]) / (value + 1)

            # Generate y coordinates of one combination of N, d and d2
            n_vertices_y = 2 * value[0] + 1       # number of vertices
            d_temp = np.full((n_vertices_y, 1), d_values[index])       
            d2_temp = np.full((n_vertices_y, 1), N_d_d2[index][2])
            d_d2 = np.hstack([d2_temp, d_temp])
            d_d2 = d_d2.flatten()

            points_y = [0]        # the first y coordinate is always 0
            y = 0

            # Iterate to generate the rest y coordinates from 0 to the dimension
            for n in np.arange(n_vertices_y):

                y += d_d2[n]
                points_y.append(y)

            vertices_y_total.append(points_y)

        N_d_d2_total.append(N_d_d2)

    N_d_d2_total = np.asarray(N_d_d2_total).reshape((N_size) * d_size, 3)
    
    
    return (N_d_d2_total, vertices_y_total)

