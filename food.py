import numpy as np

def drop_food(n_food, x_low, x_high, y_low, y_high):
    '''
    Describe:
    Randomly drop food on the surface.


    Positional arguments:
    -> n_food: the number of the food
    -> x_low: start point of the playground along the x-axis
    -> x_high: end point of the playground along the x-axis
    -> y_low: start point of the playground along the y-axis
    -> y_high: end point of the playground along the y-axis


    Return:
    -> positions: a n_food x 2 array with positions of the food
    '''

    # Set the position of the food
    x_positions = np.random.uniform(x_low, x_high, (n_food, 1)) 
    y_positions = np.random.uniform(y_low, y_high, (n_food, 1))
    positions = np.hstack([x_positions, y_positions])

    return positions