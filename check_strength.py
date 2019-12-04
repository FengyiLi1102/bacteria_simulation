import numpy as np


def check_strength(step, colonies):
    '''
    Describe:
    check the strengh of each colony based on number of colonies, age of the bacteria and the steps_eat.

    
    Positional arguments:
    -> step:                step in simulation
    -> colonies:            colony dictionary
    

    Return:
    None
    '''
    # Calculate strength for each bacteria
    for i in colonies.keys():

        ages = step - colonies[i].birth_date

        colonies[i].ages = ages

        strength = (10 / colonies[i].ages) + np.sqrt(len(colonies)) + (10 / (step - colonies[i].steps_eat))

        colonies[i].strengths = strength

    return 