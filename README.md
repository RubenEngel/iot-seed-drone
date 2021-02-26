# A Python and Linux based autonomous drone with a control web application developed using React and Flask

The drone can go on a seed planting mission using arguments submitted to the mission flight script - column, row, height, spacing. It sends a drop signal to an arduino based system with a Raspberry Pi USB connection and pyserial. It will be able to avoid obstacles (simulated with gazebo and ROS) and verify that the drop location is suitable using image colour comparison. 

The control web application is served with nginx on the drone's Raspberry Pi. Serves React frontend app and Flask backend. A RTMP live video server is to be implemented.

## Key files
basic-mission.py - python flight script in flight-server/flight-scripts/ - Connects to the drone on port 14550. The drone flight script is programmed with Dronekit, a python API for the flight control software ArduPilot. Takes column, row, height, spacing, and connection address as arguments.

flight-stats.py - python flight stats script in flight-server/flight-scripts/ - Connects to the drone on port 14551 and returns critical data until the drone becomes unarmed.

server.py - flask file in flight-scripts/venv/bin/ (Rapberry Pi virtual environement. flight-scripts/lnx-venv is development pc virtual environment) - 
A flask server that is able to call subprocesses for the flight scripts (required due to dronekit being Python2.7 and web server dependencies being Python3). Flight mission subprocess PIPE output sends mission log to frontend web application using web sockets. Uses gunicorn and eventlet to allow for flask-socketio connection to the frontend for real time communication. Flight stats subprocess sends flight statistics using flight-stats.py subprocess output.

App.js - in src - React control frontend, mobile centred styled with tailwindCSS and uses socket.io and REST API to communicate with backend. Shows a mission log using the output from the flight script subprocess. Shows flight statistics using the output from the flight stats subprocess. Live video feed to be implemented.
