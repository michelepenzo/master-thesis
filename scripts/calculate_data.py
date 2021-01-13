#!/usr/bin/env python

import pandas as pd
import rospy
from utils_functions.cartesian_wrench import sample_rate

filename_wrench_csv = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/' + rospy.get_param('mode') \
					  + '/' + rospy.get_param('task') + '/' + rospy.get_param('name') + '_wrench.csv'


# https://www.geeksforgeeks.org/python-math-operations-for-data-analysis/

print('================================================================')
print('= Calculating data of {'  + rospy.get_param('name') + '} performing {' + rospy.get_param('task') + '} with {' + rospy.get_param('mode') + '} =')
print('================================================================\n')


# reading csv file
s = pd.read_csv(filename_wrench_csv, squeeze=True)

n_values = s['wrench_x'].count()
print('Number of sample: ' + str(n_values))

if n_values * sample_rate < 60:
	print('Task time: ' + "{:.2f}".format(n_values * sample_rate) + ' sec')
else:
	print('Task time: ' + "{:.2f}".format(n_values * sample_rate / 60) + ' min')

'''
print(s[['wrench_x', 'wrench_y', 'wrench_z']].min())
print(s[['wrench_x', 'wrench_y', 'wrench_z']].max())
print(s[['wrench_x', 'wrench_y', 'wrench_z']].mean())
'''


