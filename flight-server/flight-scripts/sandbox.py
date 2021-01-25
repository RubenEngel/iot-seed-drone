import subprocess

drop_height = 2.5
drop_spacing = 3.5
drop_columns = 3
drop_rows = 3

subprocess.run(['/usr/bin/python', '/home/dronedojo/iot-seed-drone/flight-server/flight-scripts/basic_mission.py', '--connect', '127.0.0.1:14550',\
        '--height', str(drop_height), '--spacing', str(drop_spacing), '--columns', str(drop_columns), '--rows', str(drop_rows)])