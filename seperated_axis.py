import numpy as np

def normalize(vect):
    '''
        --------------------------------------------------------Goal---------------------------------------------------------------------
        # normalises the input vector using pathagoras 

        --------------------------------------------------------Input--------------------------------------------------------------------
        -> vector in question 
        -> 
        
        --------------------------------------------------------Return-------------------------------------------------------------------
        Returns normalised vector
        '''
    
    from math import sqrt
    norm = sqrt(vect[0] ** 2 + vect[1] ** 2)

    return (vect[0] / norm, vect[1] / norm)




def edge_direction(vect0, vect1):
    '''
        --------------------------------------------------------Goal---------------------------------------------------------------------
        ## gives direction between two points by subtracting the associated vectors [direction given as a new vector]

        --------------------------------------------------------Input--------------------------------------------------------------------
        -> vector0 in question 
        -> vector1 in question
        
        --------------------------------------------------------Return-------------------------------------------------------------------
        Returns vector connecting the two input vectors
        '''

    return (vect1[0] - vect0[0], vect1[1] - vect0[1])


def orthogonal(v):
    '''
        --------------------------------------------------------Goal---------------------------------------------------------------------
        # Produces orthogonal vector

        --------------------------------------------------------Input--------------------------------------------------------------------
        -> vector
        
        --------------------------------------------------------Return-------------------------------------------------------------------
        Returns othogonal vector
        '''
    return (v[1], -v[0])

 
def vertices_to_edges(vertices):
    '''
        --------------------------------------------------------Goal---------------------------------------------------------------------
        #finds vector direction between all points of the convex shape
        --------------------------------------------------------Input--------------------------------------------------------------------
        -> vertex points
        
        --------------------------------------------------------Return-------------------------------------------------------------------
        edges
        '''
    
    return [edge_direction(vertices[i], vertices[(i + 1) % len(vertices)]) \

        for i in range(len(vertices))]


def project(vertices, axis):
    '''
        --------------------------------------------------------Goal---------------------------------------------------------------------
        # Projection onto vector using dot product

        --------------------------------------------------------Input--------------------------------------------------------------------
        -> verticies
        -> axis in question
        
        --------------------------------------------------------Return-------------------------------------------------------------------
        Returns othogonal vector
        '''

    dots = [np.dot(vertex, axis) for vertex in vertices]

    return [min(dots), max(dots)]


def contains(n, range_):

    '''
        --------------------------------------------------------Goal---------------------------------------------------------------------
        # Check if projected points from one shape lie within the line overlapping with points from other shape in question

        --------------------------------------------------------Input--------------------------------------------------------------------
        -> n
        -> range
        
        --------------------------------------------------------Return-------------------------------------------------------------------
        Returns points overlapping
        '''

    a = range_[0]
    b = range_[1]

    if b < a:
        a = range_[1]
        b = range_[0]

    return (n >= a) and (n <= b)


def overlap_(a, b):
    '''
        --------------------------------------------------------Goal---------------------------------------------------------------------
        # Check overlap

        --------------------------------------------------------Input--------------------------------------------------------------------
        -> two sets of points (a,b)
        
        --------------------------------------------------------Return-------------------------------------------------------------------
        Returns True for overlap, False for no overlap
        '''

    if contains(a[0], b):
        return True

    if contains(a[1], b):
        return True

    if contains(b[0], a):
        return True

    if contains(b[1], a):
        return True

    return False
 

def separating_axis_theorem(vertices_a, vertices_b):

    edges_a = vertices_to_edges(vertices_a);    #array of vectors representing all the edges on the convex shape a
    # print(edges_a)
    edges_b = vertices_to_edges(vertices_b);    #array of vectors representing all the edges on the convex shape b
    # print(edges_b)

    edges = edges_a + edges_b                  #sum of vector directions of whole shape
    '''
    print(edges)
    print(edges[1])
    print(edges[0])
    print(len(edges))
    '''

    axes = [normalize(orthogonal(edge)) for edge in edges]         #cyles through the edges. Finds the vectors othogonal to each 
    # print(axes)                                                  #edge vector and normalises it 

    for i in range(len(axes)):
        projection_a = project(vertices_a, axes[i])
        projection_b = project(vertices_b, axes[i])
        overlapping = overlap_(projection_a, projection_b)

        if not overlapping:
            return False

    return True