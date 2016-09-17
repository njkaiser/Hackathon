#!/bin/usr/python

# I have no idea what I'm doing

# http://robotics.mech.northwestern.edu/~jarvis/hackathon_2016_site/challenge_rrt.html

import numpy
import random
import math
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from scipy.misc import imread



def buffer_world(world):
    buffered_world = world.copy()
    #for x,y in world:
    for x in range(1, len(world)-1):
        for y in range(1, len(world[0])-1):
            # if x <= 1 or x >= 98 or y <= 1 or y >= 98:
            #     continue
            # else:
            if world[x][y] == 1:
                buffered_world[x-1][y+1] = 1
                buffered_world[x][y+1] = 1
                buffered_world[x+1][y+1] = 1
                buffered_world[x-1][y] = 1
                buffered_world[x][y] = 1
                buffered_world[x+1][y] = 1
                buffered_world[x-1][y-1] = 1
                buffered_world[x][y-1] = 1
                buffered_world[x+1][y-1] = 1
    return buffered_world


def Bresenham(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end

    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points


def endpoint_collision_detect(new_point):
    x = new_point[0]
    y = new_point[1]
    if x <= 1 or x >= 98:
        return True
    if y <= 1 or y >= 98:
        return True
    if buffered_world[y][x]: # reminder: world coordinates are flipped
    #if world[y][x]: # reminder: world coordinates are flipped
        return True
    else:
        return False


def calc_nearest_neighbor(new_point, points):
    min_dist = grid_size * 2
    min_dist_point_index = 0
    counter = 0
    for last_point in points:
        #print last_point[0], last_point[1], new_point[0], new_point[1]
        dist = math.sqrt(math.pow(abs(new_point[0] - last_point[0]), 2) + math.pow(abs(new_point[1] - last_point[1]), 2))
        #print dist
        if dist < min_dist:
            min_dist = dist
            min_dist_point = points[counter]
            min_dist_point_index = counter
        counter += 1
    #print min_dist
    return min_dist_point_index, min_dist


def line_collision_detection(new_point, nearest_point):
    #nearest_point_index = calc_nearest_neighbor(new_point, points)
    #nearest_point = points[nearest_point_index]
    line_pixels = Bresenham(new_point, nearest_point)
    for x, y in line_pixels:
        if buffered_world[y][x]: # reminder: world coordinates are flipped
        #if world[y][x]: # reminder: world coordinates are flipped
            return True
    return False


def generate_new_point(points, parents):
    while(1):
        #x = random.randrange(0, grid_size-1)
        x = int(numpy.random.rand() * 100)
        #y = random.randrange(0, grid_size-1)
        y = int(numpy.random.rand() * 100)
        new_point = x,y
        if new_point in points:
            #print "INFO: randomly generated point already exists, no point added"
            continue
        if endpoint_collision_detect(new_point):
            #print "INFO: new point collides with environment - point not created"
            continue

        nearest_neighbor_index, nearest_neighbor_dist = calc_nearest_neighbor(new_point, points)
        nearest_point = points[nearest_neighbor_index]
        if nearest_neighbor_dist >= 20:
            #print "INFO: distance greater than allowed - point not created"
            continue
        if line_collision_detection(new_point, nearest_point):
            #print "INFO: connecting line collides with environment - point not created"
            continue
        parents.append(calc_nearest_neighbor(new_point, points)[0])
        points.append(new_point)

        return new_point


def end_in_sight(new_point):
    # check if there is a clear line to endpoint, if so, path is complete!
    return not line_collision_detection(new_point, q_goal)


def plot_stuff(points, parents):
    counter = 0
    plot_points = []
    codes = []
    for point in points:
        plot_points.append(points[parents[counter]])
        plot_points.append(point)
        codes.append(Path.MOVETO)
        codes.append(Path.LINETO)
        counter = counter + 1
    fig = plt.gcf()
    path = Path(plot_points, codes)
    patch = patches.PathPatch(path, color='b')
    ax = fig.add_subplot(111)
    ax.add_patch(patch)
    ax.set_xlim([0,100])
    ax.set_ylim([0,100])

    # plot the route from start to end in thick red line:
    route_plot_points = []
    route_plot_points.append(points[parents[0]])
    route_codes = []
    route_codes.append(Path.MOVETO)
    for stuff in parents:
        route_plot_points.append(points[stuff])
        route_codes.append(Path.LINETO)
    route_fig = plt.gcf()
    route_path = Path(route_plot_points, route_codes)
    route_patch = patches.PathPatch(route_path, lw=10, color='r')
    route_ax = route_fig.add_subplot(111)
    route_ax.add_patch(patch)
    route_ax.set_xlim([0,100])
    route_ax.set_ylim([0,100])

    return plot_points



# initialize variables, 100 X 100 grid, initial elements
q_init = 40,40
q_goal = 60,60
max_iterations = 250
grid_size = 100

# set up 'N' logo in background
world = imread("N_map.png")
world = numpy.flipud(world)
buffered_world = buffer_world(world)
### why doesn't this flip work to fix my x y swap problem?
# for x in range(0, len(world[0])):
#     for y in range(0, len(world)):
#         world[x][y] = world[y][x]
### why doesn't this flip work to fix my x y swap problem?
plt.imshow(world, cmap=plt.cm.binary, interpolation='nearest', origin='lower', extent=[0, world.shape[0], 0, world.shape[1]])

# generate new random point (all interference checks done during point generation), then check if finished
points = [q_init]
parents = [0]
iterations = 1
for i in range(0, max_iterations):
    valid_point = generate_new_point(points, parents)
    if end_in_sight(valid_point):
        parents.append(len(points)-1)
        points.append(q_goal)
        print "COMPLETE - SOLUTION FOUND AFTER", iterations, "ITERATIONS"
        break
    iterations += 1
print "parent indices: ", parents

# time to plot some stuff, using magic I don't yet know about
plot_points = plot_stuff(points, parents)
plt.show()

