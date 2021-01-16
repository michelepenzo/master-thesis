#!/usr/bin/python3

import pandas as pd
import csv
import matplotlib.pyplot as plt

#root_path = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/'
root_path = '/home/michele/Documents/robotica/csv_files/'

'''
# plot test wrench with position control
filename = root_path + 'calibration_tests/test_wrench_position.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(211)
plt.plot(infile['wrench_z'][2500:] * -1)
plt.title('Position wrench on z')
#plt.grid(True)

# plot test wrench with impendance control
filename = root_path + 'calibration_tests/test_wrench_impedance.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(212)
plt.plot(infile['wrench_z'][2500:] * -1)
plt.title('Impedance wrench on z')

# show first plot
plt.show()

# plot trajectory in teleop
scale = 100
filename = root_path + 'teleop/test_user/michele_penzo_2_pose.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(211)
plt.scatter(infile['pose_x'][2:]*scale, infile['pose_y'][2:]*scale)
plt.title('Cartesian pose - teleop')

# plot trajectory in kt
filename = root_path + 'kt/test_user/michele_penzo_2_pose.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(212)
plt.scatter(infile['pose_x'][2:]*scale, infile['pose_y'][2:]*scale)
plt.title('Cartesian pose - kt')

# show second plot
plt.show()

x0, x1, y0, y1 = 0, 1400, -20, 20

# wrench on EE in teleop
filename = root_path + 'teleop/test_user/eros_2_wrench.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(211)
plt.plot(infile['wrench_z'][0:])
plt.axis([x0, x1, y0, y1])
plt.title('Wrench on EE - teleop')

# wrench on EE in kt
filename = root_path + 'kt/test_user/eros_2_wrench.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(212)
plt.plot(infile['wrench_z'][0:])
plt.axis([x0, x1, y0, y1])
plt.title('Wrench on EE - kt')

# show third plot
plt.show()
'''

# waypoints michele in teleop
scale = 100
filename = root_path + 'teleop/test_user/michele_penzo_3_points.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(221)
plt.scatter(infile['x'][2:]*scale, infile['y'][2:]*scale)
plt.title('Waypoints Michele - teleop')

# waypoints michele in kt
filename = root_path + 'kt/test_user/michele_penzo_3_points.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(222)
plt.scatter(infile['x'][2:]*scale, infile['y'][2:]*scale)
plt.title('Waypoints Michele - kt')

# waypoints eros in teleop
scale = 100
filename = root_path + 'teleop/test_user/eros_2_points.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(223)
plt.scatter(infile['x'][2:]*scale, infile['y'][2:]*scale)
plt.title('Waypoints Eros - teleop')

# waypoints eros in kt
filename = root_path + 'kt/test_user/eros_2_points.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(224)
plt.scatter(infile['x'][2:]*scale, infile['y'][2:]*scale)
plt.title('Waypoints Eros - kt')

# show second plot
plt.show()
