## A Python and Linux based autonomous drone with a control web application developed using React and Flask

The drone can go on a seed planting mission using arguments submitted to the mission flight script - column, row, height, spacing. It will be able to avoid obstacles (simulated with gazebo and ROS) and verify that the drop location is suitable using image colour comparison. 

The control web application is served with nginx on the drone's Raspberry Pi. Serves React frontend app and Flask backend. A RTMP live video server is to be implemented.

# Key files
basic-mission.py - python flight script in flight-server/flight-scripts/
The drone flight script is programmed with Dronekit, a python API for the flight control software ArduPilot.

Server.py - flask file in flight-scripts/venv/bin/ (Rapberry Pi virtual environement. flight-scripts/lnx-venv is development pc virtual environment)
A flask server that is able to call subprocesses for flying the drone (required due to dronekit being python 2.7 and web server dependencies being python 3.7).
Uses gunicorn and eventlet to allow for flask-socketio connection to the frotnend for real time communication.

