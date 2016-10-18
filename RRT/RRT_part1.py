#!/bin/usr/python

# I have no idea what I'm doing

# http://robotics.mech.northwestern.edu/~jarvis/hackathon_2016_site/challenge_rrt.html

import numpy
import random
import math
import matplotlib.pyplot as mp
from matplotlib.path import Path
import matplotlib.patches as patches


def generate_random_point(points):
    #x = random.randrange(0, grid_size-1)
    x = numpy.random.rand() * 100
    #y = random.randrange(0, grid_size-1)
    y = numpy.random.rand() * 100
    new_point = x,y
    if not new_point in points:
        points.append(new_point)
        grid[new_point] = 1
        #print new_point, '\t', grid[new_point]
    else:
        print "INFO: randomly generated point already exists, no point added"
    return new_point

def calc_nearest_neighbor(new_point, points):
    min_dist = grid_size * 2
    counter = 0
    for last_point in points[:-1]:
        #print last_point[0], last_point[1], new_point[0], new_point[1]
        dist = math.sqrt(abs(new_point[0] - last_point[0]) + abs(new_point[1] - last_point[1]))
        #print dist
        if dist < min_dist:
            min_dist = dist
            min_dist_point = points[counter]
            min_dist_point_index = counter
        counter += 1
    #print min_dist
    return min_dist_point_index

def plot_stuff(points, parents):
    counter = 0
    plot_points = []
    codes = []
    for point in points:
        plot_points.append(points[parents[counter]])
        plot_points.append(point)
        codes.append(Path.MOVETO)
        codes.append(Path.LINETO)
        counter += 1
    fig = mp.figure()
    path = Path(plot_points, codes)
    patch = patches.PathPatch(path)
    ax = fig.add_subplot(111)
    ax.add_patch(patch)
    ax.set_xlim([0,100])
    ax.set_ylim([0,100])
    mp.show()

    return plot_points


# initial variables
q_init = 50,50
d_q = 1
n_iterations = 500

# initialize 100 X 100 state space grid, with middle element initialized to 1
grid_size = 100
grid = numpy.zeros((grid_size, grid_size), dtype = numpy.int8)
grid[q_init] = 1

# generate new random point, check for nearest neighbor, store these as indexes in list called "parent"
points = [q_init]
parents = [0]
for i in range(0,n_iterations):
    new_point = generate_random_point(points)
    nearest_neighbor = calc_nearest_neighbor(new_point, points)
    parents.append(nearest_neighbor)
    #print ">>>>>>>>>>>>>>>>>>>>>>"
#print parents

# time to plot some stuff, using magic I don't yet know about
plot_points = plot_stuff(points, parents)
counter = False
for pairs in plot_points:
    if counter == False:
        word = "from"
    else:
        word = "to  "
    print word, pairs
    counter = not counter




# print out grid to see what it looks like, because humans aren't computers
#for y in range(0,100):
#    for x in range(0,100):
#        print grid[x,y],
#    print ""
