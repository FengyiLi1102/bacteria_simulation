# Bacteria population on coated and non-coated strips (2D)

In this simulation, the bacteria are allocated into different colonies with a synergistic or competitive relationship in a fixed environment made of two types of materials. Bacteria can move, die, duplicate, eat and fight, and these actions depend on characterizations of the bacteria. The aim of this simulation is to find the best combination of two strips with their widths and numbers used.

## Environment

The environment of the simulation is made of two types of strips aligned one by one. 
1. **Coated strips** 
* Constrain the movement of bacteria only in the current coated region
* Have **d** as the width of the strip

2. **non-coated strips** 
* Bacteria can move to coated strips or stay in the current region. 
* Have **d2** as the width of the strip

The shape of the environment is a square in this simulation, but it can be flexibly changed by tuning the parameters.

  

## Colony

A colony is a group where bacteria live with the same relationship with others. The region of the colony is defined by the [Convex hull](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html) based on the bacteria at the outermost positions. There are two kinds of colonies:

1. **Synergistic**: Colonies merge into one integrity if their 
convex hulls overlap.

2. **Competitive**: Bacteria in the colonies fight following a way until the convex hulls do not overlap.

At the beginning of the simulation, all colonies can have a regular shape such as circle as the initial shape, and then the bacteria can be randomly generated in the colonies.

## Bacteria

Several properties are associated with the bacteria:

1. **Position**: A pair of coordinates that describes the position of the bacteria in the environment.

2. **Neighbours**: The number of neighrbours of a bacteria is equal to the number of [Voronoi cell](https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.spatial.Voronoi.html) around the it.

3. **Death_rate**: It is calculated by the equation

<p align="center">
  <img width="130" height="45" src="https://github.com/FengyiLi1102/bacteria_simulation/blob/master/death_rate.gif">
</p> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where 


## Problems

## Analysis
