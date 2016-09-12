#! /user/bin/Python

# MSR Hackathon Challange #2

# http://robotics.mech.northwestern.edu/~jarvis/hackathon_2016_site/public/docs/challenge2.pdf

import sys

def DO_IT():
    # n_lights = 100

    # input = raw_input("Please enter the number of lights: ")
    # n_lights = int(input)

    n_lights = int(sys.argv[1])

    lights = [True] * n_lights

    for i in range(2, n_lights):
        for j in range(i, n_lights):
            if j % i == 0:
                lights[j] = not lights[j]

    #for k in range(0, n_lights):
        #print k, lights[k]

if __name__ == "__main__":
    DO_IT()
