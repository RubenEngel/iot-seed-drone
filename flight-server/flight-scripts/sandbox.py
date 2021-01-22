import re
from math import sqrt

location = 'LocationLocal:north=-4.83638954163,east=10.803645134,down=-3.01426243782'

north_position = float(re.search('(?<=north=)-?[0-9]+.[0-9]+', location).group(0))
east_position = float(re.search('(?<=east=)-?[0-9]+.[0-9]+', location).group(0))

def distance_moved(initial, current):
	sqrt((current-initial)**2 + (current-initial)**2)

print(distance_moved)