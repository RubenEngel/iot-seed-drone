###### Dependencies ######
from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket
import exceptions
import math
import re
import argparse
from pymavlink import mavutil
import serial

##### Functions ######

parser = argparse.ArgumentParser(description='Drone commands')

parser.add_argument('--connect')
parser.add_argument('--height')
parser.add_argument('--spacing')
parser.add_argument('--rows')
parser.add_argument('--columns')

args = parser.parse_args()

drop_height = float(args.height)
drop_spacing = float(args.spacing)
drop_columns = int(args.columns)
drop_rows = int(args.rows)

def connectMyCopter():

	connection_string = args.connect

	# if not connection_string:
	# 	import dronekit_sitl
	# 	sitl = dronekit_sitl.start_default()
	# 	connection_string = sitl.connection_string()

	vehicle = connect(connection_string, wait_ready = True)

	return vehicle

def drop_seeds():	
	try:	
		ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
		def open_motor():
			ser.flush()
			ser.write(b'1')
		def close_motor():
			ser.flush()
			ser.write(b'0')
		open_motor()
		print('Dropping seeds..')
		time.sleep(3)
		close_motor()
		time.sleep(1)
	except:
		print('Error actuating.')

def arm_and_takeoff(targetHeight):
	while vehicle.is_armable != True:
		print("Waiting for vehicle to become armable")
		time.sleep(1)
	print("Vehicle is now armable")

	vehicle.mode = VehicleMode("GUIDED")

	while vehicle.mode!='GUIDED':
		print("Waiting for drone to enter GUIDED flight mode")
		time.sleep(1)
	print("Vehicle now in GUIDED MODE")

	vehicle.armed = True  # time delay in this request. While loop waits for success.
	while vehicle.armed==False:
		print("Waiting for vehicle to become armed")
		time.sleep(1)
	print("Props are spinning!")

	vehicle.simple_takeoff(targetHeight) ## in metres

	while True:
		print("Current Altitude: %d" % vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt >= .96*targetHeight:
			break
		time.sleep(1)
	print("Target altitude reached")
	print('----')
	return None

def north_position(location): 
	return float(re.search('(?<=north=)-?[0-9]+.[0-9]+', location).group(0))

def east_position(location):
	return float(re.search('(?<=east=)-?[0-9]+.[0-9]+', location).group(0))

def distance_magnitude(initial_n, initial_e, current_n, current_e):
	return math.sqrt((current_n-initial_n)**2 + (current_e-initial_e)**2)

def goto_relative_to_current_location(north, east, down):	
	# Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified location in the North, East, Down frame.
	msg = vehicle.message_factory.set_position_target_local_ned_encode(
		0,       # time_boot_ms (not used)
		0, 0,    # target system, target component
		mavutil.mavlink.MAV_FRAME_BODY_NED, # frame - body frame relative to current vehicle location
		0b0000111111111000, # type_mask (only positions enabled)
		north, east, down, # North, East, Down in the MAV_FRAME_BODY_NED frame
		0, 0, 0, # x, y, z velocity in m/s  (not used)
		0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
		0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
	# send command to vehicle
	vehicle.send_mavlink(msg)
	initial_location = str(vehicle.location.local_frame) # Get initial location in string format
	# initial_north = north_position(initial_location) # Use north position function to get number format of relative north pos
	# initial_east = east_position(initial_location) # Use east position function to get number format of relative east pos
	distance_moved = 0 # initialise distance moved
	print('-----')
	while distance_moved < drop_spacing*0.96: # While distance moved is not close to user specified drop spacing
		# Calculate distance moved every 0.5 seconds
		distance_moved = distance_magnitude(north_position(initial_location), east_position(initial_location), north_position(str(vehicle.location.local_frame)), east_position(str(vehicle.location.local_frame)))
		print('Distance to destination: {}'.format(drop_spacing - distance_moved))
		time.sleep(0.5)
	print('Destination reached')
	print('-----')

def move_forward(drop_spacing):
	goto_relative_to_current_location(drop_spacing, 0, 0)

def set_yaw(heading, clockwise, relative=True):
	if relative:
		is_relative=1 #yaw relative to direction of travel
	else:
		is_relative=0 #yaw is an absolute angle
	# create the CONDITION_YAW command using command_long_encode()
	msg = vehicle.message_factory.command_long_encode(
		0, 0,    # target system, target component
		mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
		0, #confirmation
		heading,    # param 1, yaw in degrees
		0,          # param 2, yaw speed deg/s
		clockwise,	# param 3, direction -1 ccw, 1 cw
		is_relative, # param 4, relative offset 1, absolute angle 0
		0, 0, 0)    # param 5 ~ 7 not used
	# send command to vehicle
	vehicle.send_mavlink(msg)
	time.sleep(3)

def turn_right():
	set_yaw(90, 1)

def turn_left():
	set_yaw(90, -1)

def return_home():
	vehicle.parameters['RTL_ALT'] = 0 # Stay at current altitude when returning home
	vehicle.mode = VehicleMode("RTL") # Enter return to launch mode.
	while vehicle.mode != "RTL": # wait for the mode to change.
		time.sleep(1)
		print("Drone is returning home.")

def seed_planting_mission(rows, columns):
	for column in range(1, drop_columns+1): 

		for row in range(1, drop_rows):
			print('Column: %d, Row: %d' % (column, row)) # print what column and row currently at
			drop_seeds()

			if column % 2 != 0 and column != 1 and row == 1 : # if column is odd & is not first column & first drop in that column, turn left. 
				print('Moving Left {}m'.format(drop_spacing))
				turn_left()
				move_forward(drop_spacing)
			elif column % 2 == 0 and row == 1: # if column is even & is first drop in that column turn right.
				print('Moving Right {}m'.format(drop_spacing))
				turn_right()
				move_forward(drop_spacing)
			else: # otherwise, move forward.
				print('Moving Forward {}m'.format(drop_spacing))
				move_forward(drop_spacing)
			
		if column == drop_columns: # if last column, return to launch. (as the row loop for the last column has finished, the mission is complete.)
			print('Last drop') # print what column and row currently at
			drop_seeds()
			return_home()
		else:
			if column % 2 != 0: # if column is odd, move right to get to new column.
				print('Column: %d, Row: %d' % (column, row)) # print what column and row currently at
				drop_seeds()
				print('Moving to new column.')
				turn_right()
				move_forward(drop_spacing)
			elif column % 2 == 0: # if column is even, move left to get to new column.
				print('Column: %d, Row: %d' % (column, row)) # print what column and row currently at
				drop_seeds()
				print('Moving to new column.')
				turn_left()
				move_forward(drop_spacing)
			else:
				print('Problem Moving Column')
				

###### Main Excecutable ######

# Connect to drone on specified port
vehicle = connectMyCopter()

# Take off to specified drop height
arm_and_takeoff(drop_height)

# Start seed planting mission
seed_planting_mission(drop_rows, drop_columns)



# While vehicle is still armed, wait 1 second loop
while vehicle.armed == True:
	time.sleep(1)