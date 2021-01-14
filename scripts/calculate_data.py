#!/usr/bin/env python

import pandas as pd
import rospy, os, csv
from utils_functions.cartesian_wrench import sample_rate

# file to read
path = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/'
filename_wrench_csv = path + rospy.get_param('mode') + '/' + rospy.get_param('task') + '/' + rospy.get_param('name') + '_wrench.csv'

path_kt_wrench = path + 'kt/'
path_teleop_wrench = path + 'teleop/'


def calculate_intro(s):
	n_values = s['wrench_x'].count()

	print(' = Number of sample: ' + str(n_values))

	m, sec = divmod(n_values * sample_rate, 60)
	h, m = divmod(m, 60)
	print(' = Task time: ' + ('{:.0f} min {:.0f} sec'.format(m, sec)))


# calculate min, max, mean value on cartesian wrench (x, y, z)
def calculate_values(s):
	_min = '{:.4f},{:.4f},{:.4f}'.format(s['wrench_x'].min(), s['wrench_y'].min(), s['wrench_z'].min())
	_max = '{:.4f},{:.4f},{:.4f}'.format(s['wrench_x'].max(), s['wrench_y'].max(), s['wrench_z'].max())
	_mean = '{:.4f},{:.4f},{:.4f}'.format(s['wrench_x'].mean(), s['wrench_y'].mean(), s['wrench_z'].mean())

	return _min, _max, _mean


# for every *_wrench.csv in same task and mode file calculate min, max, mean and create a new file with values
def calculate_values_task_mode(file_path, task_n):
	clean_file(file_path + 'results/' + task_n + '.csv')
	print_on_csv(('name,mix_x,min_y,min_z,max_x,max_y,max_z,mean_x,mean_y,mean_z',), file_path + 'results/' + task_n + '.csv')

	for filename in os.listdir(file_path + task_n+ '/'):

		if '_wrench' in filename:
			ws = pd.read_csv(file_path + task_n + '/' + filename, squeeze=True)
			_min, _max, _mean = calculate_values(ws)
			print_on_csv((filename, _min, _max, _mean), file_path + 'results/' + task_n + '.csv')

	if 'kt' in file_path:
		return ' = KT ' + task_n + '.csv OK'
	else:
		return ' = Teleop ' + task_n + '.csv OK'


# print on csv file in results folder
def print_on_csv(data, filename):
	with open(filename, 'ab') as outfile:
		wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)#, delimiter=',', quotechar='', escapechar='\\')
		wr.writerow(data)


# clean file
def clean_file(filename):
	with open(filename, 'w') as _:
		pass

# ---------------------------------------------------------------------------------------------


if __name__ == '__main__':

	single_mode = True

	if single_mode:
		print('\n = Calculating data of {' + rospy.get_param('name') + '} performing {' + rospy.get_param('task') + '} with {' + rospy.get_param('mode') + '} \n')

		# reading single csv_file
		single_file = pd.read_csv(filename_wrench_csv, squeeze=True)

		calculate_intro(single_file)
		print calculate_values(single_file)

	else:
		print('\n = Calculating results for every task \n')
		print calculate_values_task_mode(path_kt_wrench, 'task_1')
		print calculate_values_task_mode(path_kt_wrench, 'task_2')
		print calculate_values_task_mode(path_kt_wrench, 'task_3')

		print calculate_values_task_mode(path_teleop_wrench, 'task_1')
		print calculate_values_task_mode(path_teleop_wrench, 'task_2')
		print calculate_values_task_mode(path_teleop_wrench, 'task_3')

