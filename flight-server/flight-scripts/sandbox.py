#!/usr/bin/env python2
import subprocess
import re

suitable_ground = True

def analyse_ground(current_column, current_row):
	current_location_image = '/home/pi/images/Column-{}_Row-{}.jpeg'.format( current_column, current_row )
	compare_process = subprocess.Popen(['stdbuf', '-o0', '/usr/bin/python3', '/home/pi/iot-seed-drone/flight-server/flight-scripts/compare_colours.py', '--image1', '/home/pi/images/Column-1_Row-1.jpeg', '--image2', current_location_image], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	while compare_process.poll() is None:
		for line in iter(compare_process.stdout.readline, b''): # for each line of the output
			print(line.rstrip().decode('utf-8')) # print the output
			if re.search('(?<=Colour Difference: )[0-9]+.[0-9]+', line.rstrip().decode('utf-8')) is not None:
				colour_difference = float(re.search('(?<=Colour Difference: )[0-9]+.[0-9]+', line.rstrip().decode('utf-8')).group(0))
				global suitable_ground
				if colour_difference <= 25:
					suitable_ground = True
				else:
					suitable_ground = False

analyse_ground(1, 2)
print(suitable_ground)