import numpy as np
from overlap_checking import *
from check_strength import check_strength
from die_in_fight import die_fight
from collections import Counter
import collections
from itertools import combinations


def fight(step, colonies, comb, inner_step):
    '''
    Describe:
    Bacteria from each colony involved in the fight will be picked out and fight. The survivor will be based on the strengths of each
    bacteria in the fight.


    Positional arguments:
    -> step:                current step
    -> colonies:            colony dictionary
    -> comb:                combinations of colonies involved in the fight
    -> inner_step:          pseudo evolution step


    Return:
    step
    '''

    # Get strength of each bacteria
    check_strength(step, colonies)

    # Indexes of bacteria in each colony
    colonies_index = dict()

    # Colony required to fight
    colonies_fight = list(set(np.asarray(comb).flatten()))

    

    # Generate indexes of each colony that need to fight
    for index in colonies_fight:

        colonies_index[index] = [i for i in np.arange(len(colonies[index].points))]


    # Choose all fighters with the same probability
    check = True

    while(check):

        # Bacteria chosen from each colony
        colony_bacteria = list()

        # fighters
        fighters = list()

        #loop through fighting process
        for pair in comb:
            
            # colony list with bacteria indexes
            colony_0 = colonies_index[pair[0]]
            colony_1 = colonies_index[pair[1]]

            # randomly choose two bacteria in the fight
            bacteria_0_index = np.random.choice(colony_0, 1)[0]
            bacteria_1_index = np.random.choice(colony_1, 1)[0]

            # positions for two bacteria
            bacteria_0_position = colonies[pair[0]].points[bacteria_0_index]
            bacteria_1_position = colonies[pair[1]].points[bacteria_1_index]

            # strengths for two bacteria
            strength_0 = float(colonies[pair[0]].strengths[bacteria_0_index])
            strength_1 = float(colonies[pair[1]].strengths[bacteria_1_index])

            # probability to survive for two bacteria
            p_bacteria_0 = strength_0 / (strength_0 + strength_1)
            p_bacteria_1 = 1 - p_bacteria_0

            # Append two bacteria positions and their survival probability
            fighters.append([
                np.array([bacteria_0_index, p_bacteria_0]),
                np.array([bacteria_1_index, p_bacteria_1])
            ])

            # Add posiitons
            colony_bacteria.append(bacteria_0_position)
            colony_bacteria.append(bacteria_1_position)
            
        
        counter = 0

        # Check if one baceria was chosen two times
        comb_fighters = list(combinations(list(range(len(colony_bacteria))), 2))

        for cb in comb_fighters:

            if np.array_equal(colony_bacteria[cb[0]], colony_bacteria[cb[1]]):

                break

            else:

                counter += 1
        

        if counter == len(comb_fighters):

            check = False

        else:

            pass
                

    # Fight
    for i in range(len(fighters)):

        survivor = int(np.random.choice([fighters[i][0][0], fighters[i][1][0]], 
                                         p=[fighters[i][0][1], fighters[i][1][1]]))

        # Pop the chosen bacteria index 
        if survivor == fighters[i][0][0]:

            colony = die_fight(colonies[comb[i][1]], fighters[i][1][0])

            if len(colony.points) == 0:

                del colonies[comb[i][1]]
        
        else:

            colony = die_fight(colonies[comb[i][0]], fighters[i][0][0])

            if len(colony.points) == 0:

                del colonies[comb[i][0]]
        
        inner_step += 1
    

    return inner_step

