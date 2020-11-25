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



###### Main Excecutable ######

# while confirmation != 'yes':
    # these will require limits
    dropHeight = input('What height would you like the seeds to be dropped from? (metres): ')
    # dropSpacing = input('How far away do you want the drop locations to be from one another? (metres): ')
    # dropColumns = input('How many columns of seeds?: ')
    # dropRows = input('How many rows of seeds?: ')
    # dropAreaLength = dropSpacing * (dropRows - 1)
    # dropAreaWidth = dropSpacing * (dropColumns - 1)
    # confirmation = raw_input('This gives you a total drop area length of %dm and a drop area width of %dm. If this is okay type "yes": ' % (dropAreaLength, dropAreaWidth) )

vehicle = connectMyCopter()

arm_and_takeoff(dropHeight)