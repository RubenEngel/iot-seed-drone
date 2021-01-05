###### Dependencies ######

from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time
import socket
import exceptions
import math
import argparse
from pymavlink import mavutil


##### Functions ######

def connectMyCopter():
	
	parser = argparse.ArgumentParser(description='commands')
	parser.add_argument('--connect')
	args = parser.parse_args()

	connection_string = args.connect

	if not connection_string:
		import dronekit_sitl
		sitl = dronekit_sitl.start_default()
		connection_string = sitl.connection_string()

	vehicle = connect(connection_string, wait_ready = True)

	return vehicle

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
	print("Virtual props are spinning!")

	vehicle.simple_takeoff(targetHeight) ## in metres

	while True:
		print("Current Altitude: %d" % vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt >= .95*targetHeight:
			break
		time.sleep(1)
	print("Target altitude reached")
	return None

def goto_position_target_local_ned(north, east, down):
    """	
    Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified 
    location in the North, East, Down frame.

    It is important to remember that in this frame, positive altitudes are entered as negative 
    "Down" values. So if down is "10", this will be 10 metres below the home altitude.

    Starting from AC3.3 the method respects the frame setting. Prior to that the frame was
    ignored. For more information see: 
    http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned

    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.

    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
        0b0000111111111000, # type_mask (only positions enabled)
        north, east, down, # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
        0, 0, 0, # x, y, z velocity in m/s  (not used)
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
    # send command to vehicle
    vehicle.send_mavlink(msg)

def velocity_magnitude():
	velocity_vector = vehicle.velocity
	magnitude = math.sqrt(velocity_vector[0]**2 + velocity_vector[1]**2 + velocity_vector[2]**2)
	return magnitude

def goto_relative_to_current_location(north, east, down):
	goto_position_target_local_ned(north, east, down)
	time.sleep(2)
	while velocity_magnitude() > 0.125:
		print 'Velocity: {}'.format(velocity_magnitude())
		print "{}".format(vehicle.location.local_frame)
		print "-----"
		time.sleep(1)
	print('destination reached')
	time.sleep(1)

def seed_planting_mission(rows, columns):
	for column in range(1, dropColumns+1): # range does not include last value, so +1

		for row in range(1, dropRows+1): # range does not include last value, so +1

			print('Column: %d, Row: %d' % (column, row)) # print what column and row currently at
			time.sleep(1)
			print('Dropping seeds.') # drop seeds
			time.sleep(3)

			print('-----')

			if column % 2 != 0 and column != 1 and row == 1 : # if column is odd & is not first column & first drop in that column, turn left. 
				print 'Moving Left {}m'.format(dropSpacing)
				goto_relative_to_current_location(0, -dropSpacing, 0)
				print('-----')
			elif column % 2 == 0 and row == 1: # if column is even & is first drop in that column turn right.
				print 'Moving Right {}m'.format(dropSpacing)
				goto_relative_to_current_location(0, +dropSpacing, 0)
				print('-----')	
			else: # otherwsie, move forward.
				print 'Moving Forward {}m'.format(dropSpacing)
				goto_relative_to_current_location(dropSpacing, 0, 0)
				print('-----')
			
		if column == dropColumns: # if last column, return to launch. (as the row loop for the last column has finished, the mission is complete.)
			vehicle.mode = VehicleMode("RTL")
			while vehicle.mode != "RTL": # waiting for the mode to change, the command is not instant.
				print("PREPARING DRONE TO RETURN HOME...")
				time.sleep(1)
			print("Vehicle in RETURN TO LAUNCH mode")
		else:
			if column % 2 != 0: # if column is odd, move right to get to new column.
				print 'Moving to new column.'
				goto_relative_to_current_location(0, +dropSpacing, 0)
			elif column % 2 == 0: # if column is even, move left to get to new column.
				print 'Moving to new column.'
				goto_relative_to_current_location(0,-dropSpacing, 0)
			else:
				print 'Problem Moving Column'
				

###### Main Excecutable ######
time.sleep(5)
# these will require limits
confirmation = 'no'
while confirmation != 'yes':
	dropHeight = input('What height would you like the seeds to be dropped from? (metres): ')
	dropSpacing = input('How far away do you want the drop locations to be from one another? (metres): ')
	dropColumns = input('How many columns of seeds?: ')
	dropRows = input('How many rows of seeds?: ')
	dropAreaLength = dropSpacing * (dropRows - 1)
	dropAreaWidth = dropSpacing * (dropColumns - 1)
	confirmation = raw_input('This gives you a total drop area length of %dm and a drop area width of %dm. If this is okay type "yes": ' % (dropAreaLength, dropAreaWidth) )

vehicle = connectMyCopter()

arm_and_takeoff(dropHeight)

seed_planting_mission(dropRows, dropColumns)

time.sleep(60)

