#! /user/bin/Python

# MSR Hackathon Challange #2

# http://robotics.mech.northwestern.edu/~jarvis/hackathon_2016_site/public/docs/challenge2.pdf

n_lights = 20000

lights = [True] * n_lights

for i in range(2, n_lights):
    for j in range(i, n_lights, i):
        lights[j] = not lights[j]

for k in range(0, 100):
    print k, lights[k]
