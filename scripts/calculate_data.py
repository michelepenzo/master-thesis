#!/usr/bin/env python

import pandas as pd
import rospy
from utils_functions.collection_data import sample_rate

# file to read
path = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/'
filename_wrench_csv = path + rospy.get_param('mode') + '/' + rospy.get_param('task') + '/' + rospy.get_param('rep') + '/' + rospy.get_param('name') + '_wrench.csv'


def calculate_intro(s):
	n_values = s['wrench_x'].count()

	print(' = Number of sample: ' + str(n_values))

	m, sec = divmod(n_values * sample_rate, 60)
	h, m = divmod(m, 60)
	print(' = Task time: ' + ('{:.0f} min {:.0f} sec'.format(m, sec)))


# ---------------------------------------------------------------------------------------------


if __name__ == '__main__':
	print('\n = Calculating data of {' + rospy.get_param('name') + '} performing {' + rospy.get_param('task') + '} at {' + rospy.get_param('rep') + '} with {' + rospy.get_param('mode') + '} \n')

	# reading single csv_file
	single_file = pd.read_csv(filename_wrench_csv, squeeze=True)

	calculate_intro(single_file)
