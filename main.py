# libraries used during the simulation
import numpy as np
import sys
from Colony import *
from food import drop_food
from strip import strip
from EvenOrOdd import even
from overlap_checking import *
from tqdm import trange
from tqdm import tqdm
from seperated_axis import *
import matplotlib.pyplot as plt
from copy import deepcopy
import pandas as pd
from print_info import print_info
import time
from scipy.spatial import ConvexHull, convex_hull_plot_2d


def main(n_step, n_colony, n_bacteria, n_food,                                          
         x_low, x_high, y_low, y_high, radius,                                          
         eat_distance, k_die_0, k_duplicate, k_move, mu, std, born_radius,
         N_size, d_size, increment, vertices_y, strips, test_step,
         relationship='Synergistic'):
    """
    This programme simulates the population of bacteria on a surface with two different strips: coated and uncoated. Further
    details can be checked in README file.

    Main function to test the model. Tune the parameters to obtain the most optimistic combination of N (number of coated strips),
    d (width of coated region) and d2 (width of uncoated region).



    ******************************************************************************************************************************
    ***********************************Deep recursions are applied in this simulation on purpose**********************************
    ******************************Therefore, please set the recursion limit to 3000 to avoid any errors***************************
    ******************************************************************************************************************************



    Positional arguments:
    -> n_step:                  number of steps to run with each combination of N, d and d2
    -> n_colony:                number of colonies for the model
    -> n_bacteria:              number of bacteria for each colony
    -> n_food:                  number of food for bacteria to take
    -> x_low:                   lower X limit of the dimension of the surface
    -> x_high:                  higher X limit of the dimension of the surface
    -> y_low:                   lower Y limit of the dimension of the surface
    -> y_high:                  higher Y limit of the dimension of the surface
    -> radius:                  initial radius of the colony
    -> eat_distance:            prey distance for bacteria to eat
    -> k_die_0:                 death rate when no bacteria from the same colony surround
    -> k_duplicate:             duplicate rate for each bacteria as two
    -> k_move:                  move rate for bacteria
    -> born_radius:             region where new duplicated bacteria can be placed
    -> mu:                      mean of the normal distribution for bacteria movement
    -> std:                     standard deviation of the normal distribution for bacteria movement
    -> N_size:                  range of number of coated strips for finding the best combination
    -> d_size:                  range of coated strip width for finding the best combination
    -> increment:               increment of coated strip width


    Keyward arguments:
    -> relationship:            relationship between colonies
    """

    # Visualization
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    ax.set_xlim([x_low, x_high])
    ax.set_ylim([y_low, y_high])

    # Get initial positions of all the food
    food_positions = drop_food(n_food, x_low, x_high, y_low, y_high)    # (n_food, 2) array

    # A dictionary to manage all colonies
    colonies = dict()

    # ***********************************************************************************************************************************
    # **********************************************************Initiation***************************************************************
    # ***********************************************************************************************************************************

    # Initiation of colonies
    for i in range(n_colony):

        # Set the colony class
        colonies[i] = Colony()

        # Set the inital dimension and position of the colony
        # Attr: relationship, inital x and y positions, radius
        index = i + 1     # index for competitive relationship
        colonies[i].create_colony(x_low, x_high, y_low, y_high, n_bacteria, radius, index, relationship)

        # Set the initial position of the bacteria in the colony
        # Attr: initial number of bacteria with their positions
        #       k_duplicate, k_move
        colonies[i].bacteria_preparation(n_bacteria, k_duplicate, k_move, k_die_0)

        # Check the region for each bacteria
        # Attr: regions
        colonies[i].region_check(vertices_y[1][strips])

        # Check the number of the neighbours for each bacteria
        colonies[i].calNeighbours()

        # Record the initial step for the bacteria
        # Attr: age
        colonies[i].birth_date = np.zeros((n_bacteria, 1), dtype=np.int8)

        # Eat food
        # Attr: steps_eat
        food_positions = colonies[i].eat(0, food_positions, eat_distance)

        # Set the strength based on the age, number_colony and steps_eat
        # Attr: bacteria_positions, neighbours, steps_eat, death_rate, actions, birth_date, strength
        colonies[i].strength_check(1, colonies)

        # Add actions
        colonies[i].actions = np.zeros((n_bacteria, 1), dtype=np.int8)

        # Add death rate
        colonies[i].death_rate = np.zeros((n_bacteria, 1), dtype=np.int8)

        # Plot the initial state of the bacteria and food
        # ax.scatter(colonies[i].points[:, 0], colonies[i].points[:, 1], s=8)
        
    

    # Plot the food position
    # ax.scatter(food_positions[:, 0], food_positions[:, 1], s=2, color='red')
    #plt.savefig(r'E:\Coding\bacteria\Figure\strip_initial_{}'.format(strips))
    #plt.cla()

    # plt.show()

    # ***********************************************************************************************************************************
    # ************************************************************SIMULATION*************************************************************
    # ***********************************************************************************************************************************

    # Step through the simulation
    for step in tqdm(range(1, n_step + 1), desc='Step', unit='step'):

        # Plot food
        ax.scatter(food_positions[:, 0], food_positions[:, 1], s=2, color='red')
        
        # Check overlapping situation
        inner_step = overlap(step, colonies, relationship, step)

        # The total number of bacteria in each colony
        total_bacteria = 0

        # Through all colonies
        for i in colonies.keys():

            # Check region for bacteria
            colonies[i].region_check(vertices_y[1][strips])

            # Calculate the inital neighbour of each bacteria
            # Attr: bacteria_positions, neighbours, birth_date
            colonies[i].calNeighbours()

            # Bacteria eat the food around them. The positions of the left food are returned.
            # Attr: bacteria_positions, neighbours, steps_eat, birth_date
            food_positions = colonies[i].eat(step, food_positions, eat_distance)

            # Calculate the death rate of each bacteria
            # Attr: bacteria_positions, neighbours, steps_eat, death_rate, birth_date
            colonies[i].k_die(step)

            # Choose action for each bacteria
            # Attr: bacteria_positions, neighbours, steps_eat, death_rate, actions, birth_date
            colonies[i].action()


        # Start to behave what action implies
        # All three actions in the same step
        delete_index = list()

        for i in colonies.keys():
            
            # Displacement
            colonies[i].displacement(mu, std, vertices_y[1][i], x_low, x_high, y_low, y_high)

            # Duplicate
            food_positions = colonies[i].duplicate(food_positions, eat_distance, step, vertices_y[1][strips], 
                                                   born_radius, x_low, x_high, y_low, y_high, colonies)

            # Die
            colonies[i].die()

            # If all bacteria in the colony die out, remove the colony from colonies
            if len(colonies[i].points) == 0:

                delete_index.append(i)
            
            else:

                pass


            # Find the half life of the bacteria
            total_bacteria += len(colonies[i].points)

            """# Plot the bacteria
            ax.scatter(colonies[i].points[:, 0], colonies[i].points[:, 1], s=8)"""
            

        for index in delete_index:

            del colonies[index]
            

        print('')

        # Negative number for population drop. Positive for growth.
        print('Die: {}'.format(total_bacteria - (n_bacteria * n_colony)))

        # If the bacteria all die, end the simulation and get to the next strip combination.
        if len(colonies) == 0:

            break

        """elif step == n_step:    # No half life and run to the end of the evolution
            
            # print_info(colonies, step)
            return 'N/A'"""


        if relationship == 'Competitive':

            if total_bacteria <= int(0.5 * n_colony * n_bacteria):    # Have half life
            
                # print_info(colonies, step)
                for i in colonies.keys():
                    
                    if len(colonies[i].points) >= 3:

                        hull = ConvexHull(colonies[i].points)

                        for simplex in hull.simplices:

                            plt.plot(colonies[i].points[simplex, 0], colonies[i].points[simplex, 1], 'k-')

                    else:

                        continue 

                # plt.show()

                plt.savefig(r'E:\Coding\bacteria\Figure_convexhull\fig_final_{}.png'.format(strips))

                return step

            elif len(colonies) == 1:
            
            # print_info(colonies, step)
                return 'N/A'

            elif len(colonies) == 2:

                # The difference between two only colonies
                colony_keys = list(colonies.keys())
                difference = abs(len(colonies[colony_keys[0]].points) 
                                - len(colonies[colony_keys[1]].points))

                if len(colonies) == 2 and difference >= (2 * n_bacteria * n_colony):
                    
                    # print_info(colonies, step)
                    return 'N/A'

        else:

            pass
    

    for i in colonies.keys():

         ax.scatter(colonies[i].points[:, 0], colonies[i].points[:, 1], s=8)


    ax.scatter(food_positions[:, 0], food_positions[:, 1], s=2, color='red')

    for i in colonies.keys():

        hull = ConvexHull(colonies[i].points)

        for simplex in hull.simplices:

            plt.plot(colonies[i].points[simplex, 0], colonies[i].points[simplex, 1], 'k-')

    plt.savefig(r'E:\Coding\bacteria\Synergistic\Synergistic_figure\fig_final_{}.png'.format(strips))


    return 
