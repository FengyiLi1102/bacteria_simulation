import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from main import main
from tqdm import trange, tqdm
import sys
from strip import strip
import matplotlib.pyplot as plt


def analysis(n_step, n_colony, n_bacteria, n_food,                                          
            x_low, x_high, y_low, y_high, radius,                                          
            eat_distance, k_die_0, k_duplicate, k_move, mu, std, born_radius,
            N_size, d_size, test_step,
            relationship='Synergistic'):

    # Increment
    increment = (y_high) / (N_size * d_size)

    # Set the recursion limit
    sys.setrecursionlimit(3000)

    # Give the coated and uncoated regions on the playground
    vertices_y = strip(N_size, d_size, y_high, increment)

    # ***********************************************************************************************************************************
    # *************************************************************TEST******************************************************************
    # ***********************************************************************************************************************************
    
    # Dataframe for T_1/2 storage
    col_N = np.asarray([[vertices_y[0][i][0]] for i in np.arange(len(vertices_y[0]))])          # column: N
    col_d = np.asarray([[vertices_y[0][i][1]] for i in np.arange(len(vertices_y[0]))])          # column: d
    col_d2 = np.asarray([[vertices_y[0][i][2]] for i in np.arange(len(vertices_y[0]))])         # column: d2
    half_life = ['step_T_1_2_{}'.format(i) for i in range(test_step)]                           # column: half lives data
    columns = ['N', 'd', 'd2'] + half_life                                                      # combine columns
    info = np.hstack([col_N, col_d, col_d2, np.zeros(((N_size * d_size), test_step))])          # generate pre-data
    half_life_df = pd.DataFrame(info, columns=columns)                                          # generate dataframe


    # One N, d and d2 combination for the simulation
    for strips in trange(len(vertices_y[1]), desc='Strip', unit='strip'):   # strips: a list containing y coordinates of strip vertices

        # Run for number of test_step times for valid half lifes
        for i in trange(test_step, desc='T_1_2', unit='unit'):

            # Simulation function
            step = main(n_step, n_colony, n_bacteria, n_food,                                          
                        x_low, x_high, y_low, y_high, radius,                                          
                        eat_distance, k_die_0, k_duplicate, k_move, mu, std, born_radius,
                        N_size, d_size, increment, vertices_y, strips, i,
                        relationship)

            # Add half life to the dataframe
            half_life_df.loc[strips, 'step_T_1_2_{}'.format(i)] = step
        

    return half_life_df


data = analysis(20, 5, 100, 2000,
                0, 10, 0, 10, 2, 
                1, 5, 5, 50, 0, 1, 0.001,
                5, 5, 1, 'Synergistic')

# CSV from data exported
data.to_csv(r'E:\Coding\bacteria\Data\Data_synergistic.csv', index=False)