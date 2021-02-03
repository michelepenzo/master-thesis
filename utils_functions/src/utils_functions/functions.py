# !/usr/bin/env python

import csv, rospy, os
from services import *


dir_path = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/'
path = dir_path + rospy.get_param('mode') + '/' + rospy.get_param('task') + '/' + rospy.get_param('rep') + '/' + rospy.get_param('name')
filename_actions_csv = path + '.csv'


# print on csv file
def print_on_csv(data):
	with open(filename_actions_csv, 'ab') as outfile:
		wr = csv.writer(outfile, quoting=csv.QUOTE_NONE)
		wr.writerow(data)


# print on csv file
def print_on_csv_datas(data, filename):
	with open(filename, 'ab') as outfile:
		wr = csv.writer(outfile, quoting=csv.QUOTE_NONE)
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
	with open(filename_actions_csv, 'w') as _:
		pass


# clean file
def clean_file_datas(filename):
	with open(filename, 'w') as _:
		pass


# wait until paying
def init_play(led_srv):
	configure_led(led_srv, True, 1, False)
	rospy.sleep(0.5)
	configure_led(led_srv, True, 2, False)
	rospy.sleep(0.5)


# home position
def get_home_pose():
	# return 0.31899, -0.39, 0.5, 0.0, 1.0, 0.0, 0.0, 2, -0.944866252106
    return 0.475230482595, 0.00725217682308, 0.639615310969, -0.0343624410389, 0.999096035957, 0.0237426253335, 0.0079124402363, 2, 0.0214605709914


# starting pose
def get_start_pose():
	return -0.0451755022258, -0.484645335609, 0.214371466279, 0.746687173843, 0.664549816178, 0.0198237207844, 0.0209475648803, 2, 0.331987717383


# check if file is empty
def is_empty():
	return os.stat(filename_actions_csv).st_size == 0


# turn on and off led
def blink(led_srv, color):
	configure_led(led_srv, True, color, False)
	rospy.sleep(0.6)
	configure_led(led_srv, False, color, False)
