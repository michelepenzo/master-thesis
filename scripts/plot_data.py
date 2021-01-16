#!/usr/bin/python3

import pandas as pd
import csv
import matplotlib.pyplot as plt

#root_path = '/home/ice-admin/iiwa_stack_ws/src/iiwa_stack/pkgs_mp/csv_files/'
root_path = '/home/michele/Documents/robotica/csv_files/'

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
plt.show()

# plot trajectory in teleop
scale = 100
filename = root_path + 'teleop/test_user/michele_penzo_2_pose.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(211)
plt.scatter(infile['pose_x'][2:]*scale, infile['pose_y'][2:]*scale)
plt.title('Cartesian pose teleop')

# plot trajectory in kt
filename = root_path + 'kt/test_user/michele_penzo_2_pose.csv'
infile = pd.read_csv(filename, squeeze=True)
plt.subplot(212)
plt.scatter(infile['pose_x'][2:]*scale, infile['pose_y'][2:]*scale)
plt.title('Cartesian pose kt')

# show plot
plt.show()
