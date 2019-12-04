import numpy as np


def die_fight(colony, victim):
    '''
    Describe:
    calculate the fight results.


    Positional arguments:
    -> vcivtim:                     victim of fight
    -> colony:                      colony of bacteria
    
    Return:
    -> colony
    '''
    # Delete the dead bacteria information
    colony.points = np.delete(colony.points, victim, 0)
    colony.actions = np.delete(colony.actions, victim, 0)
    colony.death_rate = np.delete(colony.death_rate, victim, 0)
    colony.neighbours = np.delete(colony.neighbours, victim, 0)
    colony.regions = np.delete(colony.regions, victim, 0)
    colony.steps_eat = np.delete(colony.steps_eat, victim, 0)
    colony.strengths = np.delete(colony.steps_eat, victim ,0)
    colony.birth_date = np.delete(colony.birth_date, victim, 0)

    return colony