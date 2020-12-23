# !/usr/bin/env python

import csv, rospkg, rospy, os

from services import *

filename_csv = rospkg.RosPack().get_path('teach_play') + '/actions.csv'


# print on csv file
def print_on_csv(data):
	with open(filename_csv, 'ab') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
		wr.writerow(data)


# return an array [x, y, z, x, y, z, w, status, redundancy]
def get_cartesian_pose(data):
	return float(data[0]), float(data[1]), float(data[2]), float(data[3]), float(data[4]), \
		   float(data[5]), float(data[6]), int(data[7]), float(data[8])


# return action gripper as boolean
def get_action_gripper(data):
	return bool(int(data))


# clean file
def clean_file():
	with open(filename_csv, 'w') as _:
		pass


# wait until paying
def init_play(led_srv):
	configure_led(led_srv, True, 1, False)
	rospy.sleep(0.5)
	configure_led(led_srv, True, 2, False)
	rospy.sleep(0.5)


# home position
def get_home_pose():
	return 0.31899, -0.39, 0.5, 0.0, 1.0, 0.0, 0.0, 2, -0.944866252106

# check if file is empy
def is_empty():
	return os.stat(filename_csv).st_size == 0
