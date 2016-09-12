# hackathon_python_challenge_1

# http://robotics.mech.northwestern.edu/~jarvis/hackathon_2016_site/public/docs/challenge1.pdf

import sys

max_sequence_length = 0
max_sequence_index = 0

range_max = 1000000

for i in range(1,range_max):
    n = i
    sequence_length = 1
    while n > 1:
        #print n
        if n%2 == 0:
            n = n/2
        else:
            n = 3*n +1
        sequence_length = sequence_length + 1
        #print '    ', n, sequence_length
        if sequence_length > max_sequence_length:
            max_sequence_length = sequence_length
            max_sequence_index = i
    if i%1000 == 0:
        #str = string(i), max_sequence_length, sequence_length
        sys.stdout.write('%d %d %d\r' % (i, max_sequence_length, sequence_length))
        sys.stdout.flush()



print "max index and length: ", max_sequence_index, max_sequence_length


