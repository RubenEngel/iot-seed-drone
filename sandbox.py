import math

x = [3, 4, 5]

def velocity_magnitude():
	velocity_vector = x
	y = math.sqrt(velocity_vector[0]**2 + velocity_vector[1]**2 + velocity_vector[2]**2)
	return y

print '{}'.format(velocity_magnitude())