# practice for Monday

# what is this
# this is a comment
# comment all of this


a = 2
#a,b,c = 1,2,3

def add_two_numbers(a,b):
    """
    This function takes 2 params, either floats, ints, or strings, and adds them together using the appropriate function blah blah blah
    """
    return a+b


if a == 2:
    print "a=2"
elif a == 3:
    print "a=3"
else:
    print "not"

print 1 == 1 and 2 == 3
print 1 == 1 or 2 == 3

a = 2
b = 3
c = add_two_numbers(a,b)
print c

def do_math():
    print a+b
    print "wow, math!"

if __name__ == '__main__':
    do_math()
