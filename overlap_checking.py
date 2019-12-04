import numpy as np
from seperated_axis import *
from scipy.spatial import ConvexHull
from copy import deepcopy
from itertools import combinations
from fight import fight
from check_strength import check_strength


def overlap(step, colonies, relationship, inner_step):
    '''
    Describe:
    Check if two colonies overlap with each other or not. If they overlap, synergistic colonies will merge into a big one. Otherwise,
    they will fight until they do not overlap.


    Positional arguments:
    -> self:                
    -> colonies:                a dictionary containing all colonies during the simulation
    -> relationship:            relationship between two colonies
    -> inner_step:              pseudo steps


    Return:
    None
    '''

    # EXIT. Only one colony left.
    if len(colonies.keys()) <= 1:

        check_strength(step, colonies)

        return inner_step
    
    # If fewer than three bacteria are in one colony, they cannot form a well-defiend convexhull.
    # Another algorithm will be applied.
    colonies_keys_1 = list(colonies.keys())
    colonies_keys_2 = deepcopy(colonies_keys_1)

    for colony in colonies_keys_2:

        if len(colonies[colony].points) <= 3 and len(colonies[colony].points) > 0:

            colonies_keys_1.remove(colony)
        
        elif len(colonies[colony].points) == 0:

            del colonies[colony]
            colonies_keys_1.remove(colony)

        else:

            pass

    # If the colony does not contain any bacteria, then delete it from the colonies

    # Combinations between two arbitrary colonies
    comb = list(combinations(colonies_keys_1, 2))
    
    vertices_set = dict()
    overlap_colony = list()
    

    # Generate vertices of the Convex hulls for each existing colony
    for index in colonies_keys_1:
        
        convexhull = ConvexHull(colonies[index].points)       # Get convex hull model for the colony
        points = deepcopy(colonies[index].points)
        condition = np.array([[True, True] if i in convexhull.vertices else [False, False] for i in range(len(colonies[index].points))])
        vertices = np.extract(condition, points)
        vertices = vertices.reshape(int(len(vertices) / 2), 2)
        vertices_set[index] = vertices               # five arrays of vertices for the convex hulls for each colony

    # Synergistic
    if relationship == 'Synergistic':

        # Check whether two colonies overlap with each other or not
        for pair in comb:

            check = separating_axis_theorem(vertices_set[pair[0]], vertices_set[pair[1]])
            
            if check:

                overlap_colony = pair       # tend to merge one combination of two colonies
                break

            else:

                pass
        
        
        # EXIT. Return when no colonies overlap
        if overlap_colony == list():

            check_strength(step, colonies)

            return inner_step

        else:

            colonies[overlap_colony[0]].merge(colonies[overlap_colony[1]])
            del colonies[overlap_colony[1]]

        inner_step = overlap(step, colonies, relationship, inner_step)

        return inner_step
    
    else:     # Competitive
        
        # Check whether two colonies overlap with each other or not
        for pair in comb:

            check = separating_axis_theorem(vertices_set[pair[0]], vertices_set[pair[1]])
            
            if check:

                overlap_colony.append(pair)       # Two colonies will fight
        
        # Return when no colonies overlap
        if overlap_colony == list():

            check_strength(step, colonies)

            return inner_step
        
        else:

            inner_step = fight(step, colonies, overlap_colony, inner_step)
    
    inner_step = overlap(step, colonies, relationship, inner_step)

    return inner_step


