# Libraries, class and functions required to use
import numpy as np
import numpy.ma as ma
import matplotlib
import collections
import matplotlib.pyplot as plt
import math
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from scipy.spatial import Voronoi, voronoi_plot_2d
from collections import Counter
from copy import deepcopy
from EvenOrOdd import even
from tqdm import trange


class Colony():
    '''
    Description:
    A class containing a range  of attributes related to the bacteria and their actions. Initially, the colony will be defiend as a 
    circle with a given radius. Then it will change its shape due to the positional change of the associated bacteria making up the 
    colony. If the convex hulls of different colonies,  defined by the outermost bacteria, overlap with each other they will fight or 
    merge  depending on the conditions of the simulation.
    Synergistic: merge;    Competitive: fight


    Attributes:
    -> points:                                  Coordinates of bacteria positions.
    -> relationship:                            The nature of the simulation dictating the interactions between colonies. 
                                                Default value is 0 that means synergistic. 
                                                Different numbers mean they are competitive.
    -> x_position:                              The inital x coordinate of the center of the colony.
    -> y_position:                              The intial y coordinate of the center of the colony.
    -> radius:                                  the inital radius of the colony
    -> neighbours:                              an array with pairs of the point indices and the number of the neighbours
    -> death_rate:                              an array with pairs of the point indices and the death rate
    -> k_duplicate:                             rate of duplication
    -> k_move:                                  rate of move
    -> k_die_0:                                 rate of death
    -> birth_date:                              current step when the bacteria was born
    -> age:                                     step passing since bron for each bacteria
    -> strength:                                strenth of each bacteria based on the age, food and colony
    -> actions:                                 a n_bacteria x 1 array for the action that the bacteria will take
    -> steps_eat:                               the steps passing after eating the food
    -> regions:                                 describes which region (coated / uncoated) the bacteria are in


    Buit-in methods:
    --- create_colony:                          colony initiation
    --- bacteria_preparation:                   bacteria initiation for one colony
    --- calNeighbours:                          calculate neighbours for each bacteria
    --- action:                                 assign actions for each bacteria
    --- k_die:                                  calculate death rate based on neighbours for bacteria
    --- duplicate:                              generate duplicated bacteria from orginial bacteria
    --- displacement:                           assign new positions for bacteria
    --- eat:                                    bacteria eat food
    --- die:                                    bacteria die and removed from the colony
    --- region_check:                           check in which region the bacteria are
    --- merge:                                  merge two synergistic colonies when they overlap
    --- strength_check:                         calculate the strength of each bacteria   
    '''


    def create_colony(self, x_low, x_high, y_low, y_high, n_bacteria, radius, colony_index, relationship=0):
        '''
        Description: 
        Create the intial round colony with a random position in the playground.


        Positional arguments:
        -> self:
        -> x_low:                               start point of the playground along the x-axis
        -> x_high:                              end point of the playground along the x-axis
        -> y_low:                               start point of the playground along the y-axis
        -> y_high:                              end point of the playground along the y-axis
        -> n_bacteria:                          number of the bacteria in the colony
        -> raidus:                              the intial radius of the colony
        -> colony_index:                        the index of the colony in the dictionary


        Keyward arguments:
        -> relationship:                        0 (default)--- Synergistic; otherwise competitive


        Return:
        None
        '''
        # set the region where the center of the colony is
        # Make sure the bacteria will not be initially placed
        # out of the playground
        xl = x_low + radius
        xh = x_high - radius
        yl = y_low + radius
        yh = x_high - radius

        # set the position of the colony
        x_colony = np.random.uniform(xl, xh)                # x coordinate of the colony center
        y_colony = np.random.uniform(yl, yh)                # y coordinate of the colony center
        position_colony = np.hstack([x_colony, y_colony])

        # Add attributes to Colony class
        if relationship == 0:               # Synergistic

            self.relationship = relationship

        else:                               # Competitive

            self.relationship = colony_index
        

        self.x_position = position_colony[0]
        self.y_position = position_colony[1]
        self.radius = radius

        return
    

    def bacteria_preparation(self, n_bacteria, k_duplicate, k_move, k_die_0):
        '''
        Description:
        Set the duplicate rate for the bacteria as the attribute.
        Set the move rate for the bacteria as the attribute.
        Create all the intial coordinates for the bacteria in a colony.
        Set Inf if none of the bacteria has eaten anything yet.


        Positional arguments:
        -> self:
        -> n_bacteria:                  number of the bacteria in the colony
        -> k_duplicate:                 duplicate rate
        -> k_move:                      move rate
        -> k_die_0:                     death rate when there are no neighbours


        Return:
        -> bacteria_positions:          An array with all the intial positions of the bacteria
        '''

        # Creat the duplicate rate, move rate and death rate attributes.
        self.k_duplicate = k_duplicate
        self.k_move = k_move
        self.k_die_0 = k_die_0

        # Create all the position coordinates for the bacteria in the colony in polar form
        angle = 2*math.pi * np.random.random((n_bacteria, 1))
        r = self.radius * np.random.random((n_bacteria, 1))
        bacteria_x_positions = r * np.cos(angle) + self.x_position
        bacteria_y_positions = r * np.sin(angle) + self.y_position
        bacteria_positions = np.hstack([bacteria_x_positions, bacteria_y_positions])
        
        # Add attributes
        self.steps_eat = np.array([[np.inf] for i in range(n_bacteria)])
        self.points = bacteria_positions
        
        return bacteria_positions


    def calNeighbours(self):
        '''
        Describe:
        Calculate the number of neighbours for the given bacteria.
        

        Positional arguments:
        -> self:


        Return
        None
        '''
        # If the number of bacteria in the colony is more than 2:
        if len(self.points) > 2:

            vor = Voronoi(self.points)
            neighbour_combin = vor.ridge_points   # Array containing paired point indices as neighbouring relationship
            for_count = neighbour_combin.flatten().tolist()  # prepare for Counter
            neighbours = Counter(for_count).items()   # count number of ocurrences as the neighbours
            
            # Sort the neighbours in the form of an array
            neighbours = np.asarray(list(collections.OrderedDict(sorted(neighbours)).values()))
            neighbours = neighbours.reshape(len(neighbours), 1)

            self.neighbours = neighbours
        
        # fewer than 3
        elif len(self.points) == 2:
            
            self.neighbours = np.ones((2, 1), dtype=np.int8)
        
        # only one bacteria
        else:

            self.neighbours = np.array([1], dtype=np.int8)


        return

        
    def action(self):
        '''
        Describe:
        1: die; 2: duplicate; 3: move


        Positional arguments:
        -> self:


        Return:
        None
        '''

        # Denominator of the probability
        sum_p = self.k_duplicate + self.k_move + self.death_rate

        # Probability for each action
        die_p = (self.death_rate / sum_p).reshape(len(self.points), 1)
        duplicate_p = (self.k_duplicate / sum_p).reshape(len(self.points), 1)
        move_p = (self.k_move / sum_p).reshape(len(self.points), 1)

        # Pack three as a masked array    
        mask_p = np.hstack([die_p, duplicate_p, move_p])

        # Action list for all the bacteria in a colony
        # 1: die; 2: duplicate; 3: move
        actions = np.array([[np.random.choice([1, 2, 3], p=mask_p[i])] for i in range(len(mask_p))])

        self.actions = actions

        return 


    def k_die(self, step):
        '''
        Describe:
        Assigh each bacteria in the colony a death rate based on the neighbours of it.

        Positional arguments:
        -> self:
        -> step:    the current step

        Return
        -> death_rate: an array with pairs of the point indice and the deat rate
        '''

        # Create an empty list for death rate
        death_rate = list()

        # Steps after last eating
        steps_pass = step - self.steps_eat

        # First: if the bacteria never eats (nan), then logical_or returns False; 
        # Second: if the steps passing from the last eating are more than 10 steps, then return True
        # True: normal; False: 0
        condition = np.logical_or(np.isinf(steps_pass), steps_pass > 10)

        # k_die(x) for all the bacteria
        k_die_x = self.k_die_0 / self.neighbours

        # This is a small modification for solving neighour problem.
        # Place duplicated bacteria closely beside their original bacteria
        if len(k_die_x) != len(condition):

            dimension = len(condition) - len(k_die_x)

            modification = np.array([
                [k_die_x[int(np.random.choice(list(range(len(k_die_x))), 1))]] 
                for i in range(dimension)]).reshape(dimension, 1)
            k_die_x = np.vstack([k_die_x, modification])
        
        else:

            pass

        # Set the k_die_x as zero for the bacteria that has eaten something
        die_0 = np.zeros((len(condition), 1))
        death_rate = np.where(condition, k_die_x, die_0)
        
        self.death_rate = death_rate

        return


    def duplicate(self, food_positions, eat_distance, step, vertices_y, 
                  born_radius, x_low, x_high, y_low, y_high, colonies
                  ):
        '''
        Describe:
        Bacteria that require to duplicate will generate another bacteria around its born region. The duplicated bacteria will have death
        rate, birth data, age, strength, neighbours and pseudo action.


        Positional arguments:
        -> self:
        -> food_position:                       position of food
        -> eat_distance:                        distance in which bacteria can eat food
        -> step:                                current step
        -> vertices_y:                          playground information
        -> born_radius:                         distance in which duplicated bacteria are
        -> x_low:                               lowest limit of x-dimension of the playground
        -> x_high:                              highest limit of x-dimension of the playground
        -> y_low:                               lowest limit of y-dimension of the playground
        -> y_high:                              highest limit of y-dimension of the playground
        -> colonies:                            colony dictionary
        

        Return
        None
        '''
        # preparation
        old_n_bacteria = len(self.points)           # current number of bacteria
        old_points = deepcopy(self.points)          # current bacteria positions
        positions = deepcopy(self.points)           # a deepcopy of current bacteria positions

        # Find the positions for the new bacteria
        condition_2D = np.array([[True, True] if self.actions[i] == 2 else [False, False] for i in np.arange(len(self.actions))])
        condition_1D = np.array([[True] if self.actions[i] == 2 else [False] for i in np.arange(len(self.actions))])

        # If some bacteria require to duplicate
        if True in condition_1D:

            positions = np.extract(condition_2D, positions)
            positions = positions.reshape(int(len(positions) / 2), 2)

            # Place duplicated bacteria around the parent one
            check = True

            while(check):
                
                # Positions of duplicated points
                angle = 2*math.pi * np.random.random((len(positions), 1))
                r = born_radius * np.random.random((len(positions), 1))
                bacteria_x_positions = r * np.cos(angle) + positions[:, 0].reshape(len(positions), 1)
                bacteria_y_positions = r * np.sin(angle) + positions[:, 1].reshape(len(positions), 1)
                new_positions = np.hstack([bacteria_x_positions, bacteria_y_positions])
                points_temp = np.vstack([old_points, new_positions])

                self.points = points_temp

                # get regions of duplicated bacteria
                old_regions = np.extract(condition_1D, self.regions)
                old_regions = old_regions.reshape((len(old_regions), 1))
                new_regions = self.region_check(vertices_y)[old_n_bacteria:]

                displacement = new_regions - old_regions

                # If the bacteria move more than one regions or it is in the coated region but moved out, return False. (Based on y coordinates)
                condition_region_y = np.asarray([
                    False if np.logical_or(abs(displacement[i]) > 1, np.logical_and(even(new_regions[i]), abs(displacement[i]) >= 1)) else True 
                    for i in np.arange(len(displacement))
                ]).reshape(len(displacement), 1)

                # If the bacteria move out of strips horizontally, return false
                condition_region_edge = np.asarray([
                    False if np.logical_or(
                                    np.logical_or(new_positions[i][0] < x_low, new_positions[i][0] > x_high),
                                    np.logical_or(new_positions[i][1] < y_low, new_positions[i][1] > y_high)
                                    )
                    else True
                    for i in np.arange(len(displacement))
                ]).reshape(len(displacement), 1)

                # Combine two conditions
                condition_region = np.where(np.logical_and(condition_region_edge, condition_region_y), True, False)

                if False in condition_region:      # duplicated bacteria cannot be in the uncoated regions if it is in coated ones.
                                                   # also they cannot be out of the playground

                    pass

                else:

                    check = False
            

            # Add birth date
            new_birth_date = np.zeros((len(new_positions), 1))
            new_birth_date.fill(step)
            self.birth_date = np.vstack([self.birth_date, new_birth_date])

            # Add neighbours
            self.calNeighbours()

            # Add steps passing after eating
            steps_eat_new = np.array([[np.inf] for i in np.arange(len(positions))])
            self.steps_eat = np.vstack([self.steps_eat, steps_eat_new])

            # Add strength
            self.strength_check(step, colonies)

            # Add a action state for new born bacteria
            new_actions = np.zeros((len(positions), 1))
            self.actions = np.vstack([self.actions, new_actions])

            # Add death rate
            self.death_rate = np.vstack([self.death_rate, np.zeros((len(positions), 1))])

            # The new born bacteria will eat food
            if len(food_positions) == 0:

                return food_positions

            else:
            
                for i in np.arange(len(new_positions)):
                    
                    # position of bacteria that needs to eat 
                    target_bacteria = new_positions[i]
                    n_food = food_positions.shape[0]

                    # Calculate the distance between the chosen bacteria and all the food pieces
                    distance = np.linalg.norm(target_bacteria - food_positions, axis=1)

                    # Get an array of the food that the bacteria can eat   
                    mask = [True if distance[i] > eat_distance else False for i in np.arange(n_food)]
                    meun = distance[mask,...]

                    # If there is avaiable food:
                    if len(meun) != 0:

                        # Randomly choose one to eat and this piece food will be removed from the food_positions
                        food_eaten = np.random.choice(meun)

                        # Remove the eaten piece food from the food_positions
                        index = np.argwhere(distance == food_eaten)[0][0]
                        food_positions = np.delete(food_positions, index, 0)

                        # Record the step when the bacteria eats the food
                        self.steps_eat[i + old_n_bacteria] = int(step)

                    else:

                        pass
            
                return food_positions

        else:

            return food_positions
        

    def displacement(self, mu, std, vertices_y, x_low, x_high, y_low, y_high):
        '''
        Describe:
        Give the displacement of the bacteria for each step if it requires to move.
        If the bacteria in the coated region, then it cannot move out of the coated region.
        The bacteria cannot move out of the boundary of the playgound.


        Positional arguments:
        -> self:
        -> mu:              the mean of the Gaussian distribution
        -> std:             the standard deviation of the Gaussian distribution
        -> vertices_y:      y coordinates of the strip vertices
        -> x_low:           lowest limit of x-dimension of the playground
        -> x_high:          highest limit of x-dimension of the playground
        -> y_low:           lowest limit of y-dimension of the playground
        -> y_high:          highest limit of y-dimension of the playground

        
        None
        '''
        # preparation
        positions = deepcopy(self.points)

        # Find the bacteria that is required to move
        condition_action = np.array([[True if self.actions[i] == 3 else False] for i in range(len(self.points))])

        # If some bacteria is required to move:
        if True in condition_action:

            # Add the movement to the bacteria that is required to move and keep the rest as the previous positions
            # Displacement is based on the Gaussian distribution
            # dy and dx are taken independently

            new_position = np.where(condition_action, 
                                    positions + np.hstack([np.random.normal(mu, std, 1) * np.cos(2*math.pi * np.random.random(1)), 
                                                           np.random.normal(mu, std, 1) * np.sin(2*math.pi * np.random.random(1))
                                                          ]), positions
                                    )

            # Get present regions for each bacteria:
            old_regions = deepcopy(self.regions)

            # Check if the movement is allowed based on the following principle:
            # Bacteria in the coated region cannot move out the region 
            # Bacteria in the uncoated region can move into other regions
            # Get new regions of each bacteria after moving
            new_regions = self.region_check(vertices_y)

            displacement = new_regions - old_regions    # Check the movement between strips

            # If the bacteria move more than one regions or it is in the coated region but moved out, return False. (Based on y coordinates)
            condition_region_y = np.asarray([
                False if np.logical_or(abs(displacement[i]) > 1, np.logical_and(even(new_regions[i]), abs(displacement[i]) >= 1)) else True 
                for i in np.arange(len(displacement))
            ]).reshape(len(self.points), 1)

            # If the bacteria move out of strips horizontally, return false
            condition_region_edge = np.asarray([
                False if np.logical_or(
                                np.logical_or(new_position[i][0] < x_low, new_position[i][0] > x_high),
                                np.logical_or(new_position[i][1] < y_low, new_position[i][1] > y_high)
                                )
                else True
                for i in np.arange(len(displacement))
            ]).reshape(len(self.points), 1)

            # Combine two conditions
            condition_region = np.where(np.logical_and(condition_region_edge, condition_region_y), True, False)

            # Reject unallowed movement and keep the rest.
            final_position = np.where(condition_region, new_position, self.points)

            # Obtain the final correct regions for bacteria
            final_regions = np.where(condition_region, new_regions, old_regions)

            self.points = final_position
            self.regions = final_regions

        else:

            pass

        return


    def eat(self, step, food_positions, eat_distance):
        '''
        Describe:
        The bacteria eat the food in the eat distance and the current step is recorded.


        Positional arguments:
        -> self:
        -> step:              the present step of the simulation
        -> food_positions:    an array containing food piece positions
        -> eat_distance:      the prey region of the bacteria (radius)

        Return:
        -> food_positions: the updated food_positions array is required for other colonies
        '''
        # If there is no food
        if type(food_positions) == None:
            return
        
        for i in np.arange(len(self.points)):

            target_bacteria = self.points[i]
            n_food = food_positions.shape[0]

            # Calculate the distance between the chosen bacteria and all the food pieces
            distance = np.linalg.norm(target_bacteria - food_positions, axis=1)

            # Get an array of food that the bacteria can eat   
            mask = [True if distance[i] > eat_distance else False for i in np.arange(n_food)]
            meun = distance[mask,...]

            # If there is avaiable food:
            if len(meun) != 0:
                # Randomly choose one to eat and this piece of food will be removed from the food_positions
                food_eaten = np.random.choice(meun)

                # Remove the eaten piece of food from the food_positions
                index = np.argwhere(distance == food_eaten)[0][0]
                food_positions = np.delete(food_positions, index, 0)

                # Record the step when the bacteria eats the food
                self.steps_eat[i] = int(step)
            else:
                pass


        return food_positions


    def die(self):
        '''
        Describe:
        Remove the dead bacteria from the colony and also delete their information.

        
        Positional arguments:
        -> self:

        Return:
        None
        '''
        
        positions = deepcopy(self.points)

        # Find the bacteria that will die
        condition_die_2D = np.array([[False, False] if self.actions[i] == 1 else [True, True] for i in range(len(self.points))])
        condition_die_1D = np.array([[False] if self.actions[i] == 1 else [True] for i in np.arange(len(self.points))])
        condition_copy_1D = condition_die_1D.copy()

        # If some bacteria require to die:
        if False in condition_die_1D:

            if self.relationship == 'Compeitive':

                # Remove the dead bacteria from the colony with their information
                positions = np.extract(condition_die_2D, positions)
                positions = positions.reshape(int(positions.shape[0] / 2), 2)
                self.points = positions

                self.actions = np.extract(condition_copy_1D, self.actions)
                self.actions.resize(len(condition_copy_1D), 1)
                self.ages = np.extract(condition_copy_1D, self.ages)
                self.ages.resize(len(condition_copy_1D), 1)
                self.birth_date = np.extract(condition_copy_1D, self.birth_date)
                self.birth_date.resize(len(condition_copy_1D), 1)
                self.death_rate = np.extract(condition_copy_1D, self.death_rate)
                self.death_rate.resize(len(condition_copy_1D), 1)
                self.neighbours = np.extract(condition_copy_1D, self.neighbours)
                self.neighbours.resize(len(condition_copy_1D), 1)
                self.regions = np.extract(condition_copy_1D, self.regions)
                self.regions.resize(len(condition_copy_1D), 1)
                self.steps_eat = np.extract(condition_copy_1D, self.steps_eat)
                self.steps_eat.resize(len(condition_copy_1D), 1)
                self.strengths = np.extract(condition_copy_1D, self.strengths)
                self.strengths.resize(len(condition_copy_1D), 1)

        else:

            for i in np.arange(len(condition_die_1D)):

                if condition_die_1D[i] == False:

                    self.actions = np.delete(self.actions, i, 0)
                    self.death_rate = np.delete(self.death_rate, i, 0)
                    self.neighbours = np.delete(self.neighbours, i, 0)
                    self.regions = np.delete(self.regions, i, 0)
                    self.steps_eat = np.delete(self.steps_eat, i, 0)
                    self.strengths = np.delete(self.strengths, i ,0)
                    self.birth_date = np.delete(self.birth_date, i, 0)
                    self.ages = np.delete(self.ages, i, 0)
        

        return
    

    def region_check(self, y_coordinates):
        '''
        Describe:
        Calculate the region of each bacteria. Regions can be classified into coated and uncoated.


        Positional arguments:
        -> self:
        -> y_coordinates:    list containing y coordinates of the strip vertices


        Return:
        None
        '''
        # preparation
        y_range = deepcopy(self.points)
        region_array = np.zeros((len(y_range), 1))
        
        # Determine the region where the bacteria is
        # Odd number: uncoated; Even number: coated
        # Start from 1 (0, d2)
        for i in range(len(y_range)):

            y = y_range[i, 1]
            y_copy = y_coordinates.copy()
            y_copy.append(y)
            index = sorted(y_copy).index(y)
            region_array[i, 0] = index

        self.regions = region_array
        
        return region_array

    
    def merge(self, colony):
        '''
        Describe:
        Merge two colonies if they are in synergistic relationship.

        Positional arguments:
        -> self:
        -> colony:      the colony that will be merged to the base colony, and then it disappears.

        Return:
        None
        '''

        self.points = np.vstack([self.points, colony.points])               # concatenate positions of points to the base target colony
        self.steps_eat = np.vstack([self.steps_eat, colony.steps_eat])
        self.regions = np.vstack([self.regions, colony.regions])
        self.neighbours = np.vstack([self.neighbours, colony.neighbours])
        self.ages = np.vstack([self.ages, colony.ages])
        self.strengths = np.vstack([self.strengths, colony.strengths])
        self.birth_date = np.vstack([self.birth_date, colony.birth_date])

        return

    
    def strength_check(self, step, colonies):
        '''
        Describe:
        Calculate the strength for bacteria based on their age, number of colonies and steps_eat.


        Positional arguments:
        -> self:
        -> step:            current step
        -> colonies:        colony dictionary


        Return:
        None
        '''
        # Steps passing since the bacteria was generated
        ages = step - self.birth_date

        # strength function
        strength = (10 / ages) + np.sqrt(len(colonies)) + (10 / (step - self.steps_eat))

        self.strengths = strength
        self.ages = ages

        return
        
